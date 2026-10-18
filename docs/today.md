# Today local planner v1

Today opens at startup. Research opens Ask and Analytics opens Analyse with one click; the sidebar retains Home, Capture, Ask, Explore, Library, Insights, Datasets and Analyse.

Choose a planning day, Day or Week, and an IANA display timezone (for example Asia/Kolkata). The time rail shows actual scheduled intervals, including intervals crossing midnight. Due dates are separate from scheduled time. Unscheduled tasks have neither; overdue tasks remain visible. Three priorities show the first three incomplete tasks relevant to the selected day, sorted by priority (1 highest), scheduled start, creation time and ID.

Create a task below the timeline. Title is required; details, project, due date and related files are optional. Leave “Schedule this task” unchecked to avoid assigning time. For scheduled tasks enter both local start and end as `YYYY-MM-DDTHH:MM`, with an IANA task timezone. Clocks moving forward can make times invalid; repeated hours require choosing first or second occurrence. The display timezone changes presentation, not saved instants. Due dates are civil dates independent of the display timezone.

Use Edit / reschedule to change any task fields, or Complete to persist done status. All tasks remain accessible by their scheduled/due day or unscheduled list. Project labels create persisted projects; the Project status panel changes active/done status independently of tasks. Related files must already exist under `wiki/`, `knowledge/` or `datasets/` within DATA_DIR. References do not read or send file contents and may become stale if files are moved.

## Privacy and limits

`DATA_DIR/planner/tasks.sqlite3` is a private SQLite store, ignored by git, with a 0700 planner directory and 0600 database on POSIX. Use a private configured DATA_DIR. The directory path and registry files reject symlinks and hard-linked registry files. Local records are not encrypted; protect your OS account and backups. No task details appear in error messages, and task fields render as plain text. No source-note extraction, calendar, paid service, external AI, recurrence, notification, background sync, drag-and-drop or deletion is provided. Week is a seven-day list; it does not move tasks automatically. Existing Ask consent behavior is unchanged.

Demo mode shows synthetic examples only and never instantiates the private task service. Local edits are unavailable in demo.

## Storage and recovery

Schema version 1 migrations, each write, and full task snapshots in history commit in SQLite transactions with foreign keys and FULL synchronous writes. Project status changes also have timestamped history. Task IDs and creation times are immutable. Edits include the previous update timestamp; concurrent edits fail instead of overwriting changes. Unknown future schemas fail closed. History is an audit/recovery source, not an automatic undo UI.

Before backing up, stop Streamlit and other writers, then copy the entire `planner/` directory into a private backup location. Never commit this directory or publish it in a demo bundle. To recover, stop all writers, retain a separate copy of the damaged directory, check a backup using SQLite `PRAGMA integrity_check`, and restore that verified directory with private permissions. Do not manually edit records in the active database. SQLite rolls back interrupted uncommitted writes. Permission, lock, corruption or migration failures show a generic error; fix the storage problem before retrying. No app action deletes tasks or resets storage.

## Synthetic verification

Tests create temporary workspaces; they do not use personal planner data:

```sh
PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 .venv/bin/python tests/browser_today_check.py
```

Browser tests require Playwright and Chrome (`SECONDSELF_TEST_CHROME` overrides its executable). They start an isolated localhost app, block outbound browser requests, exercise creation, rescheduling, completion, reload, navigation and 390/1440px layouts. Unit tests cover timezone gaps/ambiguity, invalid dates, categories, sorting, transactions, schema handling, stale writes, restart persistence and storage guards.

For a manual synthetic workspace, choose a new empty private directory and launch with `PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=false SECONDSELF_DATA_DIR=/absolute/path/to/synthetic-workspace streamlit run app.py`. Enter only invented tasks. To review the built-in read-only examples instead, launch with `PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true streamlit run app.py`.

The implementation separates `task_service.py` (validation, timezone conversion, constrained SQLite records and transactions) from `today_ui.py` (forms and presentation). `app.py` owns the existing session-state navigation. No existing knowledge or dataset registry is mutated by task operations; references only validate existing local file paths.
