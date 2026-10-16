#!/usr/bin/env python3
"""
SecondSelf graph renderer — generate interactive graph.html from graph.json.

Phase 5 — Graph Visualization (vis-network).

Usage:
  python render_graph.py
  python render_graph.py --output graph.html
  ./render_graph.sh

For Streamlit (Phase 7):
  from render_graph import render_graph_html
  st.components.v1.html(render_graph_html(), height=600)
"""

from __future__ import annotations

import argparse
import html
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import GRAPH_FILE, GRAPH_HTML, PARA_COLORS, PARA_FOLDERS, PIPELINE_LOG, ROOT, ensure_directories

VIS_NETWORK_VERSION = "9.1.9"
VIS_NETWORK_CDN = (
    f"https://unpkg.com/vis-network@{VIS_NETWORK_VERSION}/"
    "standalone/umd/vis-network.min.js"
)
VIS_NETWORK_CSS = (
    f"https://unpkg.com/vis-network@{VIS_NETWORK_VERSION}/styles/vis-network.min.css"
)
DEFAULT_PARA_COLOR = "#9ca3af"
HOVER_SUMMARY_MAX_LEN = 300
RECENT_NODE_DAYS = 7
MAX_DISPLAY_NODES = 200


def setup_logging() -> logging.Logger:
    ensure_directories()
    logger = logging.getLogger("secondself.render_graph")
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


def load_graph(graph_file: Path) -> dict[str, Any]:
    """Load graph.json or return an empty graph payload."""
    from config import DATA_DIR, DEPLOY_MODE
    if not DEPLOY_MODE and graph_file == GRAPH_FILE:
        from refresh import active_graph
        try:
            graph = active_graph(DATA_DIR)
            if graph is not None:
                return graph
        except (ValueError, OSError, KeyError, TypeError):
            return {"nodes": [], "edges": [], "meta": {"error": "verification_failed"}}
    if not graph_file.is_file():
        LOGGER.warning("Graph file not found: %s", graph_file)
        return {
            "nodes": [],
            "edges": [],
            "meta": {"error": "missing", "message": "No graph yet. Run build_graph.py."},
        }

    try:
        data = json.loads(graph_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        LOGGER.error("Could not read graph file %s (%s)", graph_file, exc)
        return {
            "nodes": [],
            "edges": [],
            "meta": {
                "error": "invalid_json",
                "message": "graph.json is invalid. Re-run build_graph.py.",
            },
        }

    if not isinstance(data, dict):
        return {"nodes": [], "edges": [], "meta": {"error": "invalid_format"}}

    data.setdefault("nodes", [])
    data.setdefault("edges", [])
    data.setdefault("meta", {})
    return data


def truncate_text(text: str, max_len: int = HOVER_SUMMARY_MAX_LEN) -> str:
    value = (text or "").strip()
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"


def is_recent_node(created: str, days: int = RECENT_NODE_DAYS) -> bool:
    if not created:
        return False
    try:
        normalized = created.replace("Z", "+00:00")
        created_at = datetime.fromisoformat(normalized)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        age = datetime.now(timezone.utc) - created_at.astimezone(timezone.utc)
        return age.days < days
    except (TypeError, ValueError):
        return False


def para_color(para: str) -> str:
    return PARA_COLORS.get(para, DEFAULT_PARA_COLOR)


def map_node_to_vis(node: dict[str, Any]) -> dict[str, Any]:
    """Map one graph.json node to vis-network format (Phase 5.2–5.5, 5.7)."""
    degree = int(node.get("degree") or 0)
    tags = node.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]

    summary = str(node.get("summary") or "")
    label = str(node.get("label") or node.get("slug") or node.get("id") or "Note")
    para = str(node.get("para") or "resources")
    color = para_color(para)
    recent = is_recent_node(str(node.get("created") or ""))

    hover_summary = truncate_text(summary, HOVER_SUMMARY_MAX_LEN)
    tag_text = ", ".join(str(tag) for tag in tags) or "(none)"
    hover = f"{label}\n\n{hover_summary}\n\nTags: {tag_text}"

    return {
        "id": node["id"],
        "label": label,
        "title": html.escape(hover),
        "para": para,
        "color": {
            "background": color,
            "border": "#fbbf24" if recent else color,
            "highlight": {
                "background": color,
                "border": "#f8fafc",
            },
        },
        "size": 10 + degree * 2,
        "font": {"color": "#f8fafc", "size": 14},
        "borderWidth": 3 if recent else 1,
        "recent": recent,
        "raw": {
            "id": node.get("id"),
            "label": label,
            "para": para,
            "tags": tags,
            "summary": summary,
            "path": node.get("path", ""),
            "created": node.get("created", ""),
            "slug": node.get("slug", ""),
            "degree": degree,
        },
    }


def map_edge_to_vis(edge: dict[str, Any]) -> dict[str, Any]:
    """Map one graph.json edge to vis-network format."""
    edge_type = str(edge.get("type") or "explicit")
    title = edge_type
    weight = edge.get("weight")
    if weight is not None:
        title = f"{edge_type} ({weight})"

    line_color = "#94a3b8" if edge_type == "semantic" else "#64748b"
    return {
        "from": edge["source"],
        "to": edge["target"],
        "title": html.escape(title),
        "arrows": {"to": {"enabled": True, "scaleFactor": 0.45}},
        "color": {"color": line_color, "opacity": 0.75, "highlight": "#f8fafc"},
        "smooth": {"type": "dynamic"},
    }


def prepare_vis_payload(graph: dict[str, Any]) -> dict[str, Any]:
    """Convert graph.json into vis-network nodes/edges plus metadata."""
    nodes = [map_node_to_vis(node) for node in graph.get("nodes", []) if node.get("id")]
    node_ids = {node["id"] for node in nodes}
    edges = [
        map_edge_to_vis(edge)
        for edge in graph.get("edges", [])
        if edge.get("source") in node_ids and edge.get("target") in node_ids
    ]
    return {
        "nodes": nodes,
        "edges": edges,
        "meta": graph.get("meta", {}),
        "para_colors": PARA_COLORS,
        "para_folders": PARA_FOLDERS,
        "max_display_nodes": MAX_DISPLAY_NODES,
    }


def render_graph_html(
    graph: dict[str, Any] | None = None,
    *,
    graph_file: Path | None = None,
) -> str:
    """Return a self-contained HTML document for vis-network (Phase 5.9)."""
    if graph is None:
        graph = load_graph(graph_file or GRAPH_FILE)

    payload = prepare_vis_payload(graph)
    # JSON quoting alone does not protect an HTML script raw-text context.
    # Escape HTML delimiters and JS line separators without changing the data.
    graph_json = json.dumps(payload, ensure_ascii=False)
    for char, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                          ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        graph_json = graph_json.replace(char, escaped)
    meta = payload.get("meta") or {}
    generated_at = html.escape(str(meta.get("generated_at", "unknown")))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SecondSelf — Knowledge Graph</title>
  <link rel="stylesheet" href="{VIS_NETWORK_CSS}" />
  <style>
    :root {{
      --bg: #0f172a;
      --panel: #1e293b;
      --text: #f8fafc;
      --muted: #94a3b8;
      --accent: #3b82f6;
      --warn: #f59e0b;
      --border: #334155;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      padding: 1rem 1.25rem 0.75rem;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
    }}
    header h1 {{
      margin: 0 0 0.25rem;
      font-size: 1.25rem;
      font-weight: 600;
    }}
    header p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.875rem;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: center;
      padding: 0.75rem 1.25rem;
      border-bottom: 1px solid var(--border);
      background: #111827;
    }}
    .toolbar label {{
      color: var(--muted);
      font-size: 0.875rem;
      margin-right: 0.25rem;
    }}
    .filter-btn {{
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--text);
      border-radius: 999px;
      padding: 0.35rem 0.8rem;
      font-size: 0.8rem;
      cursor: pointer;
    }}
    .filter-btn.active {{
      border-color: var(--accent);
      background: rgba(59, 130, 246, 0.2);
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-left: auto;
      font-size: 0.75rem;
      color: var(--muted);
    }}
    .legend span::before {{
      content: "";
      display: inline-block;
      width: 0.65rem;
      height: 0.65rem;
      border-radius: 50%;
      margin-right: 0.35rem;
      vertical-align: middle;
      background: var(--dot);
    }}
    #banner {{
      display: none;
      padding: 0.65rem 1.25rem;
      background: rgba(245, 158, 11, 0.15);
      color: #fcd34d;
      border-bottom: 1px solid rgba(245, 158, 11, 0.35);
      font-size: 0.875rem;
    }}
    #error-panel {{
      display: none;
      margin: 1.25rem;
      padding: 1rem;
      border: 1px solid #7f1d1d;
      background: rgba(127, 29, 29, 0.25);
      border-radius: 0.5rem;
      color: #fecaca;
    }}
    #empty-panel {{
      display: none;
      margin: 2rem auto;
      text-align: center;
      color: var(--muted);
      max-width: 28rem;
      line-height: 1.5;
    }}
    #layout {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 320px;
      min-height: 0;
    }}
    #network {{
      min-height: 500px;
      height: calc(100vh - 160px);
      background: radial-gradient(circle at top, #1e293b 0%, #0f172a 55%);
      border-right: 1px solid var(--border);
    }}
    #detail-panel {{
      padding: 1rem 1.1rem;
      overflow-y: auto;
      background: var(--panel);
    }}
    #detail-panel h2 {{
      margin: 0 0 0.5rem;
      font-size: 1.05rem;
      line-height: 1.35;
    }}
    #detail-panel .meta {{
      color: var(--muted);
      font-size: 0.8rem;
      margin-bottom: 0.75rem;
    }}
    #detail-panel .summary {{
      white-space: pre-wrap;
      line-height: 1.5;
      font-size: 0.9rem;
    }}
    #detail-panel .tags {{
      margin-top: 0.75rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }}
    .tag {{
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #bfdbfe;
      border-radius: 999px;
      padding: 0.15rem 0.55rem;
      font-size: 0.75rem;
    }}
    #detail-placeholder {{
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.5;
    }}
    @media (max-width: 900px) {{
      #layout {{ grid-template-columns: 1fr; }}
      #network {{ height: 55vh; border-right: none; border-bottom: 1px solid var(--border); }}
    }}
    @keyframes pulse-border {{
      0%, 100% {{ box-shadow: 0 0 0 0 rgba(251, 191, 36, 0.45); }}
      50% {{ box-shadow: 0 0 0 8px rgba(251, 191, 36, 0); }}
    }}
    .pulse-hint {{
      font-size: 0.75rem;
      color: #fbbf24;
      margin-top: 0.5rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>SecondSelf Knowledge Graph</h1>
    <p id="graph-meta">Generated: {generated_at}</p>
  </header>

  <div class="toolbar">
    <label>Filter</label>
    <button class="filter-btn active" data-para="all">All</button>
    <button class="filter-btn" data-para="projects">Projects</button>
    <button class="filter-btn" data-para="areas">Areas</button>
    <button class="filter-btn" data-para="resources">Resources</button>
    <button class="filter-btn" data-para="archives">Archives</button>
    <div class="legend">
      <span style="--dot:{PARA_COLORS['projects']}">Projects</span>
      <span style="--dot:{PARA_COLORS['areas']}">Areas</span>
      <span style="--dot:{PARA_COLORS['resources']}">Resources</span>
      <span style="--dot:{PARA_COLORS['archives']}">Archives</span>
    </div>
  </div>

  <div id="banner"></div>
  <div id="error-panel"></div>
  <div id="empty-panel">
    <h2>Your brain is empty</h2>
    <p>Capture and classify notes to see your knowledge graph.<br />
    Run <code>python capture.py</code> then <code>python classify.py</code> and <code>python build_graph.py</code>.</p>
  </div>

  <div id="layout">
    <div id="network"></div>
    <aside id="detail-panel">
      <div id="detail-placeholder">
        Click a node to see its summary, tags, and file path.
        <div class="pulse-hint">Gold borders pulse on notes added in the last 7 days.</div>
      </div>
      <div id="detail-content" style="display:none;"></div>
    </aside>
  </div>

  <script>
    window.__SECONDSELF_GRAPH__ = {graph_json};
  </script>
  <script src="{VIS_NETWORK_CDN}"></script>
  <script>
    (function () {{
      const payload = window.__SECONDSELF_GRAPH__ || {{ nodes: [], edges: [], meta: {{}} }};
      const allNodes = payload.nodes || [];
      const allEdges = payload.edges || [];
      const meta = payload.meta || {{}};
      const maxDisplay = payload.max_display_nodes || {MAX_DISPLAY_NODES};

      const networkEl = document.getElementById("network");
      const errorPanel = document.getElementById("error-panel");
      const emptyPanel = document.getElementById("empty-panel");
      const banner = document.getElementById("banner");
      const detailPlaceholder = document.getElementById("detail-placeholder");
      const detailContent = document.getElementById("detail-content");
      const graphMeta = document.getElementById("graph-meta");

      function showError(message) {{
        errorPanel.style.display = "block";
        errorPanel.textContent = message;
        networkEl.style.display = "none";
        document.getElementById("layout").style.display = "none";
      }}

      if (typeof vis === "undefined") {{
        showError("Graph library failed to load. Check your network connection and reload.");
        return;
      }}

      if (meta.error === "missing") {{
        showError(meta.message || "No graph yet. Run build_graph.py.");
        return;
      }}

      if (meta.error === "invalid_json") {{
        showError(meta.message || "graph.json is invalid. Re-run build_graph.py.");
        return;
      }}

      if (!allNodes.length) {{
        emptyPanel.style.display = "block";
        networkEl.style.display = "none";
        document.getElementById("layout").style.gridTemplateColumns = "1fr";
        detailPlaceholder.textContent = "No nodes to display yet.";
        return;
      }}

      const nodeCount = meta.node_count ?? allNodes.length;
      const edgeCount = meta.edge_count ?? allEdges.length;
      graphMeta.textContent = `Generated: ${{meta.generated_at || "unknown"}} · ${{nodeCount}} notes · ${{edgeCount}} links`;

      let activePara = "all";
      let network = null;
      let pulseTimer = null;
      let pulseOn = true;
      const recentIds = new Set(allNodes.filter(n => n.recent).map(n => n.id));

      function edgesForNodes(nodeIds) {{
        const idSet = new Set(nodeIds);
        return allEdges.filter(e => idSet.has(e.from) && idSet.has(e.to));
      }}

      function nodesForFilter(para) {{
        let nodes = para === "all" ? allNodes.slice() : allNodes.filter(n => n.para === para);
        if (para === "all" && nodes.length > maxDisplay) {{
          nodes.sort((a, b) => (b.raw?.degree || 0) - (a.raw?.degree || 0));
          nodes = nodes.slice(0, maxDisplay);
          banner.style.display = "block";
          banner.textContent =
            `Showing top ${{maxDisplay}} nodes by connection count (${{allNodes.length}} total). Use PARA filters to narrow down.`;
        }} else {{
          banner.style.display = "none";
        }}
        return nodes;
      }}

      function renderDetail(node) {{
        if (!node || !node.raw) return;
        const raw = node.raw;
        detailPlaceholder.style.display = "none";
        detailContent.style.display = "block";
        const tags = (raw.tags || []).map(t => `<span class="tag">${{escapeHtml(t)}}</span>`).join("");
        detailContent.innerHTML = `
          <h2>${{escapeHtml(raw.label)}}</h2>
          <div class="meta">${{escapeHtml(raw.para)}} · degree ${{raw.degree || 0}} · ${{escapeHtml(raw.created || "unknown date")}}</div>
          <div class="summary">${{escapeHtml(raw.summary || "No summary available.")}}</div>
          <div class="tags">${{tags || '<span class="tag">no tags</span>'}}</div>
          <div class="meta" style="margin-top:1rem; word-break:break-all;">${{escapeHtml(raw.path || "")}}</div>
        `;
      }}

      function escapeHtml(value) {{
        return String(value)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;");
      }}

      function buildNetwork(nodes) {{
        const nodeIds = nodes.map(n => n.id);
        const edges = edgesForNodes(nodeIds);
        const data = {{
          nodes: new vis.DataSet(nodes.map(n => {{
            const copy = JSON.parse(JSON.stringify(n));
            delete copy.raw;
            delete copy.recent;
            return copy;
          }})),
          edges: new vis.DataSet(edges),
        }};

        const options = {{
          nodes: {{
            shape: "dot",
            scaling: {{ min: 12, max: 36 }},
          }},
          edges: {{
            width: 1.5,
            selectionWidth: 2,
          }},
          physics: {{
            enabled: nodes.length > 1,
            stabilization: {{ iterations: Math.min(150, 50 + nodes.length) }},
            barnesHut: {{
              gravitationalConstant: -3200,
              centralGravity: 0.25,
              springLength: 130,
              springConstant: 0.04,
              damping: 0.09,
            }},
          }},
          interaction: {{
            dragNodes: true,
            dragView: true,
            zoomView: true,
            hover: true,
            tooltipDelay: 120,
            navigationButtons: true,
            keyboard: {{ enabled: true, bindToWindow: false }},
          }},
        }};

        if (network) {{
          network.destroy();
          network = null;
        }}

        network = new vis.Network(networkEl, data, options);

        network.on("click", function (params) {{
          if (!params.nodes.length) return;
          const nodeId = params.nodes[0];
          const node = nodes.find(n => n.id === nodeId) || allNodes.find(n => n.id === nodeId);
          renderDetail(node);
        }});

        startPulse(nodes);
      }}

      function startPulse(visibleNodes) {{
        if (pulseTimer) clearInterval(pulseTimer);
        const visibleRecent = visibleNodes.filter(n => recentIds.has(n.id));
        if (!visibleRecent.length || !network) return;

        pulseTimer = setInterval(() => {{
          pulseOn = !pulseOn;
          visibleRecent.forEach(node => {{
            network.body.data.nodes.update({{
              id: node.id,
              borderWidth: pulseOn ? 4 : 2,
              color: {{
                ...node.color,
                border: pulseOn ? "#fbbf24" : node.color.background,
              }},
            }});
          }});
        }}, 800);
      }}

      function setActiveFilter(para) {{
        activePara = para;
        document.querySelectorAll(".filter-btn").forEach(btn => {{
          btn.classList.toggle("active", btn.dataset.para === para);
        }});
        const nodes = nodesForFilter(para);
        buildNetwork(nodes);
      }}

      document.querySelectorAll(".filter-btn").forEach(btn => {{
        btn.addEventListener("click", () => setActiveFilter(btn.dataset.para));
      }});

      setActiveFilter("all");
    }})();
  </script>
</body>
</html>
"""


def write_graph_html(
    graph_file: Path | None = None,
    output_file: Path | None = None,
    graph: dict[str, Any] | None = None,
) -> Path:
    """Write graph.html to disk."""
    target = output_file or GRAPH_HTML
    if graph is None:
        graph = load_graph(graph_file or GRAPH_FILE)

    html = render_graph_html(graph)
    temp_path = target.with_suffix(".html.tmp")
    temp_path.write_text(html, encoding="utf-8")
    temp_path.replace(target)
    LOGGER.info("Wrote graph visualization -> %s", target)
    return target


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render interactive graph.html from graph.json.",
    )
    parser.add_argument(
        "--graph-file",
        type=Path,
        default=GRAPH_FILE,
        help=f"Input graph.json (default: {GRAPH_FILE})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GRAPH_HTML,
        help=f"Output HTML file (default: {GRAPH_HTML})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_directories()
    output = write_graph_html(graph_file=args.graph_file, output_file=args.output)
    graph = load_graph(args.graph_file)
    node_count = len(graph.get("nodes", []))
    print(f"graph.html: {node_count} node(s) -> {output}")
    print(f"Open: open {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
