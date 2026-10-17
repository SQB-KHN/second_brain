#!/usr/bin/env python3
"""
SecondSelf ask CLI — RAG Q&A over your personal knowledge base.

Phase 7 — Integration (Ask module).

Usage:
  python ask.py "What do I know about PARA?"
  python ask.py "What projects am I working on?" --top-k 5
  ./ask.sh "your question"
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from typing import Any

import numpy as np

try:
    from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
except ImportError:
    print(
        "Missing dependencies. Run:\n"
        "  pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)

from config import (
    XAI_API_KEY,
    XAI_LLM_MODEL,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_LLM_MODEL,
    LLM_MODEL,
    MIN_RETRIEVAL_SCORE,
    EMBEDDINGS_DIR,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    PIPELINE_LOG,
    RAG_MAX_CONTEXT_CHARS,
    RAG_MAX_EXCERPT_CHARS,
    RAG_TOP_K,
    ensure_directories,
)
from link import (
    WikiNote,
    cosine_similarity,
    load_embedding_index,
    scan_wiki_notes,
)

from tools.verified_vectors import select_verified_vectors

MAX_LLM_RETRIES = 3

SYSTEM_PROMPT = """You are SecondSelf, a personal knowledge assistant.
Answer ONLY from the provided context (the user's own notes).
If the context does not contain enough information, say so explicitly.
Cite sources by note title. Do not hallucinate facts not in the context."""


@dataclass(frozen=True)
class SourceCitation:
    id: str
    title: str
    score: float
    para: str
    summary: str
    path: str


@dataclass
class AskResult:
    question: str
    answer: str
    sources: list[SourceCitation]
    tokens_used: int | None = None


class AskError(Exception):
    """Raised when ask() cannot proceed."""


def setup_logging() -> logging.Logger:
    ensure_directories()
    logger = logging.getLogger("secondself.ask")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(PIPELINE_LOG, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


LOGGER = setup_logging()


def get_llm_client() -> tuple[OpenAI, str]:
    """Return an LLM client for RAG synthesis."""
    if XAI_API_KEY:
        return OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1"), XAI_LLM_MODEL
    if OPENAI_API_KEY:
        return OpenAI(api_key=OPENAI_API_KEY), LLM_MODEL
    if GROQ_API_KEY:
        LOGGER.info("Using Groq API for RAG synthesis")
        return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL), GROQ_LLM_MODEL
    raise AskError("API key not configured. Set XAI_API_KEY, OPENAI_API_KEY or GROQ_API_KEY in .env.")


def embed(question: str) -> np.ndarray:
    """Embed a question with the same provider and model as transactional refresh."""
    from tools.embedding_provider import create_embedder
    try:
        return create_embedder()(question.strip())
    except (ValueError, OSError, APIConnectionError, APIStatusError) as exc:
        raise AskError(str(exc)) from exc


def retrieve_top_k(
    question_vector: np.ndarray,
    notes: list[WikiNote],
    vectors: dict[str, np.ndarray],
    *,
    top_k: int = RAG_TOP_K,
) -> list[tuple[WikiNote, float]]:
    """Retrieve the most similar wiki notes by cosine similarity (Phase 7.2)."""
    note_lookup = {note.id: note for note in notes}
    scored: list[tuple[WikiNote, float]] = []

    for note_id, vector in vectors.items():
        note = note_lookup.get(note_id)
        if note is None:
            continue
        score = cosine_similarity(question_vector, vector)
        scored.append((note, score))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[: max(1, top_k)]


def format_context(candidates: list[tuple[WikiNote, float]]) -> str:
    """Format retrieved notes into an LLM context window (Phase 7.3)."""
    blocks: list[str] = []
    total_chars = 0

    for note, score in candidates:
        excerpt = note.body.strip()
        if len(excerpt) > RAG_MAX_EXCERPT_CHARS:
            excerpt = excerpt[: RAG_MAX_EXCERPT_CHARS - 1].rstrip() + "…"

        block = (
            f"### {note.title}\n"
            f"ID: {note.id}\n"
            f"PARA: {note.para}\n"
            f"Summary: {note.summary}\n"
            f"Tags: {', '.join(note.tags) or '(none)'}\n"
            f"Relevance: {score:.3f}\n\n"
            f"{excerpt or '(empty body)'}"
        )

        if total_chars + len(block) > RAG_MAX_CONTEXT_CHARS:
            remaining = RAG_MAX_CONTEXT_CHARS - total_chars
            if remaining > 200:
                blocks.append(block[: remaining - 1].rstrip() + "…")
            break

        blocks.append(block)
        total_chars += len(block)

    return "\n\n---\n\n".join(blocks)


def build_rag_prompt(question: str, context: str) -> list[dict[str, str]]:
    """Build chat messages for RAG synthesis (Phase 7.4)."""
    user_content = (
        f"Question:\n{question.strip()}\n\n"
        f"Context from the user's notes:\n\n{context}\n\n"
        "Answer the question using only the context above. "
        "Cite note titles when referencing specific information."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def call_rag_llm(client: OpenAI, model: str, messages: list[dict[str, str]]) -> tuple[str, int | None]:
    """Call the LLM and return answer text plus token usage (Phase 7.5)."""
    last_error: Exception | None = None

    for attempt in range(1, MAX_LLM_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
            )
            answer = (response.choices[0].message.content or "").strip()
            tokens_used = None
            if response.usage is not None:
                tokens_used = int(response.usage.total_tokens)
            return answer or "I could not generate an answer from your notes.", tokens_used
        except (APIConnectionError, RateLimitError, APIStatusError) as exc:
            last_error = exc
            LOGGER.warning("RAG LLM error (attempt %d/%d): %s", attempt, MAX_LLM_RETRIES, exc)

    raise AskError(f"LLM request failed after {MAX_LLM_RETRIES} attempts: {last_error}")


def to_sources(candidates: list[tuple[WikiNote, float]]) -> list[SourceCitation]:
    return [
        SourceCitation(
            id=note.id,
            title=note.title,
            score=round(score, 4),
            para=note.para,
            summary=note.summary,
            path=note.wiki_path,
        )
        for note, score in candidates
    ]


def ask(
    question: str,
    *,
    top_k: int = RAG_TOP_K,
    min_score: float = MIN_RETRIEVAL_SCORE,
) -> AskResult:
    """
    Answer a natural-language question using RAG over wiki notes.

    Handles empty corpus, missing embeddings, and low retrieval scores.
    """
    cleaned = question.strip()
    if not cleaned:
        raise AskError("Question cannot be empty.")

    from refresh import current, verified_active_vectors
    from config import DATA_DIR
    try:
        generation = current(DATA_DIR)
        if generation:
            notes, vectors, excluded = verified_active_vectors(DATA_DIR)
        else:
            index = load_embedding_index()
            if not index:
                return AskResult(
                    question=cleaned,
                    answer="Brain not indexed yet. Run refresh.py dry-run first.",
                    sources=[],
                )

            notes = scan_wiki_notes()
            if not notes:
                return AskResult(
                    question=cleaned,
                    answer="No notes in your knowledge base.",
                    sources=[],
                )

            # Fail closed: never retrieve from legacy, stale, corrupted, or unmatched
            # vectors. This read-only selector does not call link.py's destructive
            # validate_embedding_file implementation.
            vectors, excluded = select_verified_vectors(
                notes, index, EMBEDDINGS_DIR, EMBEDDING_MODEL
            )
            # Provenance alone cannot establish a complete Ask/Graph generation.
            if vectors:
                vectors, excluded = {}, {"missing_generation": len(notes)}
    except (ValueError, OSError, KeyError, TypeError):
        return AskResult(cleaned, "Knowledge artifacts failed verification. Run refresh.py status and recover or refresh.", [])
    if not vectors:
        LOGGER.warning("No verified embeddings available; exclusion counts: %s", excluded)
        return AskResult(
            question=cleaned,
            answer=("No verified embeddings available. Existing embeddings may "
                    "lack provenance metadata or be stale. Ask is unavailable "
                    "until refresh.py refresh completes."),
            sources=[],
        )

    question_vector = embed(cleaned)
    if (question_vector.ndim != 1 or not np.isfinite(question_vector).all()
            or not np.linalg.norm(question_vector)
            or any(vector.shape != question_vector.shape for vector in vectors.values())):
        raise AskError("Query embedding dimensions differ from the verified generation. Check the model and refresh.")
    candidates = retrieve_top_k(question_vector, notes, vectors, top_k=top_k)
    relevant = [(note, score) for note, score in candidates if score >= min_score]

    if not relevant:
        best_score = candidates[0][1] if candidates else 0.0
        LOGGER.info(
            "No notes above retrieval threshold %.2f (best score %.3f)",
            min_score,
            best_score,
        )
        return AskResult(
            question=cleaned,
            answer="No relevant notes found in your knowledge base for that question.",
            sources=to_sources(candidates[:1]) if candidates else [],
        )

    context = format_context(relevant)
    if not context.strip():
        return AskResult(
            question=cleaned,
            answer="No relevant notes found in your knowledge base for that question.",
            sources=to_sources(relevant),
        )

    try:
        client, model = get_llm_client()
    except AskError as exc:
        return AskResult(question=cleaned, answer=str(exc), sources=to_sources(relevant))

    LOGGER.warning("Answer synthesis sends your question and retrieved note excerpts off this Mac to %s", model)
    messages = build_rag_prompt(cleaned, context)
    answer, tokens_used = call_rag_llm(client, model, messages)

    LOGGER.info(
        "Ask complete: question=%r sources=%d tokens=%s",
        cleaned,
        len(relevant),
        tokens_used,
    )
    return AskResult(
        question=cleaned,
        answer=answer,
        sources=to_sources(relevant),
        tokens_used=tokens_used,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask questions over your SecondSelf knowledge base.")
    parser.add_argument(
        "question",
        nargs="?",
        help='Question to ask, e.g. "What do I know about PARA?"',
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=RAG_TOP_K,
        metavar="N",
        help=f"Number of notes to retrieve (default: {RAG_TOP_K}).",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=MIN_RETRIEVAL_SCORE,
        metavar="SCORE",
        help=f"Minimum cosine similarity to include a note (default: {MIN_RETRIEVAL_SCORE}).",
    )
    return parser.parse_args(argv)


def print_result(result: AskResult) -> None:
    print(result.answer)
    if result.sources:
        print("\nSources:")
        for source in result.sources:
            print(f"  - {source.title} [{source.para}] score={source.score:.3f}")
    if result.tokens_used is not None:
        print(f"\nTokens used: {result.tokens_used}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.question or not args.question.strip():
        print("Error: Question cannot be empty.", file=sys.stderr)
        print('Usage: python ask.py "What do I know about PARA?"', file=sys.stderr)
        return 1

    if args.top_k < 1:
        print("Error: --top-k must be at least 1.", file=sys.stderr)
        return 1

    if args.min_score < 0 or args.min_score > 1:
        print("Error: --min-score must be between 0 and 1.", file=sys.stderr)
        return 1

    try:
        result = ask(
            args.question,
            top_k=args.top_k,
            min_score=args.min_score,
        )
    except AskError as exc:
        LOGGER.error("%s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
