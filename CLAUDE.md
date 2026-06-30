# DATA-TEMPLATE — CLAUDE.md

## Purpose

Educational and reference starterkit for data science and analytics. Content is organized as numbered Jupyter notebooks covering statistical foundations, business analytics, and machine learning — written in a narrative-first style (theory + code + outputs in one artifact).

**Not** a web service or backend — it is a notebook-first repo. There is no app to run, no server to start.

---

## Repository Layout

```
000-analytics_compendium/   # Analytics reference (24 notebooks)
010-ml_examples/            # ML tutorials and examples (16 notebooks)
030-CoE/                    # Center of Excellence maturity content
040-sql/                    # SQL execution-order reference
data/                       # Sample datasets (CSV) — do not move
img/                        # Reference images (EDA checklist, Greek alphabet)
requirements.txt            # Root Python dependencies
.python-version             # Python 3.11.9
```

---

## Notebook Inventory

### 000-analytics_compendium/
| Notebook | Topic |
|----------|-------|
| 000-general_advice+KPI | Data science mindset, OMTM, KPI framing |
| 001-metrics_cheatsheet_notebook | Business metrics quick reference |
| 005-terminology_med_mode_zscore_pvalue... | Statistical terminology |
| 007-a-z_eda_exploring_data+mlbest_practice | EDA template and best practices |
| 008-expected_value_framework | Expected value framework |
| 010-pivot_table | Pandas pivot operations |
| 010-probability+odds | Probability, odds, likelihood |
| 015-data_sampling+representation | Sampling distributions |
| 020-deviation-variance-stddev | Variance and standard deviation |
| 030-derivative | Calculus derivatives |
| 040-factoranalysis | Factor analysis / dimensionality reduction |
| 050-plots | When to use which chart type |
| 065-csat_clv_churn | CSAT, CLV, churn (customer metrics) |
| 070-cohort_basic | Cohort analysis fundamentals |
| 071-cohorts+who_uses_what | Advanced cohort analysis |
| 080-hypothesis_tests | Hypothesis testing |
| 082-significance_test | Significance checks |
| 085-ab-test | A/B testing methodology |
| 090-co-coccurance | Co-occurrence analysis |
| 100-lift+leverage | Lift and leverage |
| 500-onepager | Analytics one-pager template |
| 900-dashboard | Dashboard design example |
| 1000-playground | Experimental / scratch notebook |

### 010-ml_examples/
| Notebook | Topic |
|----------|-------|
| 000-general_approach+modeloverview | ML workflow overview |
| 012-terminology_models_objective_fct... | ML terminology, objective functions |
| 015-quality: balance, baserate+quality | Class imbalance, baserate |
| 016-overfitting,modelcomplexity+... | Overfitting and regularization |
| 020-residuals | Residual analysis |
| 030-workflow_model+tuning | Model selection + hyperparameter tuning |
| 040-support-vector-machines | SVM |
| 050-expected_value_calculation_for_outcome | EV with predictive models |
| 051-expected_mau_uplift | Feature uplift analysis on MAU |
| 055-clv_development_time | CLV prediction |
| 060-bayes | Bayesian classification |
| 070-knn_feature_selection | Feature selection + KNN |
| 080-k_means_unsup_clustering | K-Means clustering |
| 090-knn_similarity_neighbors_clusters | K-Nearest Neighbors |
| 091-recommender_next_best_action | Next-best-action recommender |
| 100-causation+counterfactuals | Causality and counterfactuals |

---

## Conventions

- **Numeric filename prefixes** (`000-`, `010-`, ...) define ordering/chapters — preserve them when adding new notebooks. Gap space intentionally left between numbers (e.g. 070, 071, 080) so new content can be inserted without renaming.
- **Narrative-first**: notebooks mix Markdown explanation with code cells. When editing code, always preserve surrounding Markdown. If you extract logic to a module, add a short MD cell noting what moved and why.
- **Data paths are relative**: always use `data/` paths (e.g. `pd.read_csv("../data/loans_income.csv")`). Do not reference cloud storage or absolute paths unless a notebook already does.
- **Adobe brand colors** for any charts or diagrams: primary Red `#EB1000`, Dark Gray `#2C2C2C`, accents — Magenta `#E63888`, Purple `#6349E0`, Blue `#3273DE`, Teal `#21A5A2`, Green `#009C3B`, Yellow `#FFCE2E`, Orange `#E9740A`.

---

## Developer Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Convert notebook to script for logic editing
jupyter nbconvert --to script path/to/notebook.ipynb

# Headless execution (with timeout)
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 path/to/notebook.ipynb
```

When adding a reusable function:
1. Create a module under a new `src/` directory (none exists yet — create it if needed).
2. Update calling notebooks to import from it, replacing duplicated cells.
3. Add a short README in `src/` with a one-line import example.

---

## What NOT to do

- Do not reformat or reorder Markdown narrative without an explicit request.
- Do not move or delete files in `data/` — notebooks depend on those exact relative paths.
- Do not add global test infrastructure (CI, pytest suite) without discussing with the repo owner first.
- Do not auto-execute long-running cells; use `nbconvert --execute` with a timeout if execution is needed.

---

## Key Reference Notebooks

- Narrative patterns: [000-analytics_compendium/000-general_advice+KPI.ipynb](000-analytics_compendium/000-general_advice+KPI.ipynb)
- Modeling workflow: [010-ml_examples/030-workflow_model+tuning.ipynb](010-ml_examples/030-workflow_model+tuning.ipynb)
- Dependencies: [requirements.txt](requirements.txt)
