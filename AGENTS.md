# Project Overview

Apache NiFi processors for reading and writing QVD files.

qvd4nifi brings the proprietary Qlik View Data (QVD) format into NiFi flows. It is a set of
Python processors (NiFi 2.x Python extensions) that convert between QVD and NDJSON, built on
top of the [PyQvd](https://github.com/MuellerConstantin/PyQvd) library. It is delivered as a
standalone NAR file with all dependencies bundled, published on GitHub Releases.

## Functionality

**`ReadQvd`** (`qvd4nifi/reader.py`)
Converts the content of a QVD flow file into NDJSON, one record per line, using the display
value of each cell. Sets the attributes `mime.type`, `qvd.record.count` and
`qvd.columns.count`.

**`WriteQvd`** (`qvd4nifi/writer.py`)
Converts NDJSON flow file content into a QVD file. The columns are taken from the keys of the
first record. Sets the same attributes as `ReadQvd`.

Both are `FlowFileTransform` processors and route to `success`; errors surface as processor
exceptions.

## Tech Stack

- **Language**: Python >= 3.10, < 3.13
- **Packaging**: Poetry
- **Task Runner**: Nox (`noxfile.py`)
- **Testing**: pytest
- **Linting**: pylint (configured in `pyproject.toml`)
- **Runtime dependencies**: `PyQvd`; `nifiapi` is provided by NiFi at runtime
- **Local NiFi**: Docker Compose (`compose.yaml`)

# Project Structure

```
.
├── qvd4nifi/
│   ├── reader.py             # ReadQvd processor
│   └── writer.py             # WriteQvd processor
├── scripts/
│   └── build_nar.py          # Builds the NAR into dist/
├── tests/
├── data/                     # Sample QVD files (small, medium, large), mounted read-only as /data in the container
├── scratchpad/               # Git-ignored output directory, mounted as /scratchpad in the container
├── compose.yaml              # Local NiFi with the built NAR mounted
├── noxfile.py
├── pyproject.toml
└── CHANGELOG.md
```

# Development

Tasks run through Nox inside the Poetry environment:

- `poetry run nox -s tests` – tests
- `poetry run nox -s lint` – pylint over `qvd4nifi` and `tests`
- `poetry run nox -s nar` – builds the NAR into `dist/`

To try the processors in a real NiFi, build the NAR and run `docker compose up -d` (UI at
`https://localhost:8443/nifi`, credentials in `compose.yaml`). After rebuilding the NAR apply
it with `docker compose restart nifi`.

A change is only done when `tests` and `lint` pass without findings. Changes to processor
behavior should additionally be checked in the local NiFi.

# Design Decisions

- **Thin wrapper around PyQvd**: All QVD handling belongs to PyQvd. The processors only
  translate between flow file content and PyQvd. Don't reimplement format logic here; fix or
  extend PyQvd instead.
- **Lazy imports**: PyQvd is imported inside `transform`, because NiFi installs the
  processor's `dependencies` only after loading the module. The matching
  `# pylint: disable=import-outside-toplevel` is intentional.
- **Versions are declared in several places**: The project version in `pyproject.toml` and the
  `version` in each processor's `ProcessorDetails`, as well as the pinned `PyQvd==x.y.z` in each
  `dependencies`, must be kept in sync, also with the range in `pyproject.toml`.
- **Python processor API**: Processors use the NiFi Python API (`nifiapi`), which is only
  available inside NiFi. Don't import it from code that has to run outside of NiFi.
- **Standalone NAR**: The NAR must contain all dependencies. Don't rely on packages installed
  in the NiFi environment.
- **Format fidelity**: Files written must stay loadable by QlikView/Qlik Sense. Don't guess
  about the format; when in doubt, ask instead of assuming.

## Coding Principles

- **KISS**: Prefer the simplest solution that works. Avoid unnecessary abstractions – extract only after the third repetition (Rule of Three).
- **DRY**: Define logic once, import everywhere. Duplicated code is a maintenance liability.
- **YAGNI**: Don't build features or abstractions on speculation. Implement what's needed now.
- **Single Responsibility**: Each function, class, and module has one clear purpose.
- **Fail Fast**: Validate inputs early, raise meaningful errors immediately. Never swallow exceptions silently.
- **Guard Clauses over Nesting**: Prefer early returns over deeply nested `if/else` blocks.
- **Explicit over Implicit**: Prefer explicit parameters and return types over hidden assumptions or side effects.
- **No Comment Spam**: Document _why_, not _what_. `# increment counter` before `counter += 1` is not welcome.

## General Instructions

- Prefer reading before writing – understand the existing structure before generating new files or refactoring. Don't assume conventions; verify them.
- Never dig into `.venv/`, `.nox/`, `dist/`, `build/` or other generated directories – if you need to understand a dependency, read its docs. If you still need additional information just ask me.
- Don't fix what you didn't break – scope changes strictly to what was asked. No opportunistic refactors, formatting fixes, or "while I'm here" changes. But if
  you find something feel free to tell me.
- One task at a time – complete and verify the current task before moving to the next. Don't batch unrelated changes in one go.
- Every bugfix comes with a test that reproduces the bug.
- Comments explain the code and the decisions behind it, not the discussion that led to a change. That belongs in the commit message or the issue.
- User-facing changes get an entry in an `[Unreleased]` section at the top of `CHANGELOG.md` (Keep a Changelog format; create the section if missing).
- English is the project language for code, comments, docs and commit messages. Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `build:`, `test:`, …).
