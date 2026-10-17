# SecondSelf 3.1 — Statistical Analysis Engine v1

## Goal
Add an Analyse workspace operating on immutable registered dataset versions. Numerical calculations are performed locally using SciPy and statsmodels, never invented by an AI model.

## Scope
- Choose registered dataset version, select variables, configure and preview analysis and exclusions.
- Exploratory statistics; Pearson/Spearman correlations; paired/unpaired t-tests; chi-square tests; OLS and binary logistic regression.
- Output observations used/excluded, missingness rules, coefficients, effect sizes, test statistics, p-values, confidence intervals and fit diagnostics as applicable.
- Surface invalid inputs, low sample sizes, multicollinearity, singular matrices, perfect separation, violated assumptions and other caveats explicitly; no causal assertions.
- Save immutable reproducible run manifests with dataset ID/version/hash, algorithm, exact parameters, software versions, UTC timestamp, results, diagnostics and output hash. Bound persisted results and provide safe export.
- Preserve existing dataset versions, Document Ingestion, AI Insights, Ask, Capture, Explore and Library. Analyses must never modify raw datasets.
- Use allowlisted statistical procedures, bounded data/memory/output size, atomic persistence, safe parameter validation. No uploaded code or LLM-generated code execution.
- Entirely local. No paid AI calls, external dataset transfer or autonomous network fetch. DEPLOY_MODE read-only.
- Test synthetic analytical reference fixtures, missingness, invalid method assumptions, repeatability, privacy, recovery, browser Analyse UX, and all existing regression suites; update docs and CI.

## Non-goals
Advanced causal inference, Bayesian statistics, panel data, time-series forecasting, arbitrary Python/R code or autonomous interpretation are future releases.

## Delivery
Work on statistical-engine-v1 branch. Produce one integrated draft PR with passing tests. Do not merge, deploy, use personal datasets or paid services.
