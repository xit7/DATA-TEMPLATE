# Copilot / AI Agent Instructions — DATA-TEMPLATE

Purpose
- Short, actionable guidance for AI coding agents working in this repository.

Quick context
- This repository is a data- and analysis-focused collection of Jupyter notebooks and small support files. Main content lives under:
  - `000-analytics_compendium/` — analysis notebooks, narrative-first explorations (example: [000-analytics_compendium/000-general_advice+KPI.ipynb](000-analytics_compendium/000-general_advice+KPI.ipynb)).
  - `010-ml_examples/` — modeling examples and short tutorials (example: [010-ml_examples/000-general_approach+modeloverview.ipynb](010-ml_examples/000-general_approach+modeloverview.ipynb)).
  - `data/` — CSVs used by notebooks (example: [data/loans_income.csv](data/loans_income.csv)).
  - `requirements.txt` at the repo root (and occasional per-folder `requirements.txt`).

Big-picture architecture & patterns
- This is not a web/service repo — it is a notebook-first analysis repo. Code is organized as numbered notebooks (leading numbers indicate ordering/chapters). Treat notebooks as the primary artifacts: they contain narrative, cells with exploratory code, and the intended outputs.
- Minimal glue code exists; the majority of change tasks are either: (a) update notebook logic/cells, or (b) extract code to a small script/module for reuse.

Developer workflows (commands an agent may need)
- Install dependencies (recommended):

  ```bash
  pip install -r requirements.txt
  ```

- When changing logic in a notebook, prefer:
  - Convert the notebook to a script to edit logic (e.g., `jupyter nbconvert --to script path/to/notebook.ipynb`) or use the `nbformat` Python API.
  - Implement and test logic in a `.py` file, then update the notebook with cleaned cells that call the new module.
- Avoid executing long-running notebook cells automatically. If execution is necessary, keep it limited and prefer headless runs using `nbconvert --execute` with timeouts.

Project-specific conventions
- Filenames start with numeric prefixes for ordering (e.g., `000-`, `010-`). Preserve these prefixes when adding new notebooks to fit existing sequencing.
- Notebook cells often mix narrative and code; when editing code, preserve surrounding Markdown explanations. If you refactor code into modules, add a short MD cell noting that the code was moved and why.
- Keep data reads relative and explicit: prefer `data/` paths (example: [data/loans_income.csv](data/loans_income.csv)). Do not assume external storage or cloud buckets unless a notebook mentions them.

Integration points & external dependencies
- External integrations are minimal — dependencies are package-based (see `requirements.txt`). If a notebook imports a package not in the root `requirements.txt`, check the folder-level `requirements.txt` and update the root file only if you verify it's needed globally.

Editing guidance & examples
- Small change (fix a calculation in a notebook):
  1. Convert notebook to script (`nbconvert`), or edit cell in place.
  2. Run the affected cell(s) locally (or with `nbconvert --execute`) to verify outputs.
  3. Preserve narrative; add a small Markdown note describing the fix.

- Larger change (add a reusable function):
  1. Create a small module under a new `src/` or `lib/` directory (follow existing repo structure; add `src/` if none exists).
  2. Write unit-level tests if appropriate (there are no existing test suites — discuss with the repo owner before adding global test infra).
  3. Update the calling notebooks to import the new module and replace duplicated cells with a short example cell.

What NOT to change automatically
- Do not reformat or re-order notebooks' Markdown narrative unless explicitly requested.
- Do not delete or move data files in `data/` without confirmation — notebooks expect these exact relative paths.

Where to look for examples
- Narrative notebook patterns: [000-analytics_compendium/000-general_advice+KPI.ipynb](000-analytics_compendium/000-general_advice+KPI.ipynb)
- Modeling examples: [010-ml_examples/030-workflow_model+tuning.ipynb](010-ml_examples/030-workflow_model+tuning.ipynb)
- Root dependency list: [requirements.txt](requirements.txt)

If you modify or add files
- Update `requirements.txt` when you add new runtime dependencies used across multiple notebooks.
- If you add helper modules, include a short README in the new folder showing a minimal import example and one-line usage.

Questions for the human
- If you plan to introduce automated tests or CI runs that execute notebooks, confirm acceptable execution timeouts and whether it's ok to run `--execute` on the full notebook set.

— End of instructions —

If anything above is unclear or you want the instructions expanded (e.g., add explicit nbconvert examples or a sample `src/` layout), tell me which part to refine.
