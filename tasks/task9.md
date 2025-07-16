Goal: Analyze and synthesize all results into a final report.
Budget: { gpu_type: "NONE", max_hours: 0.5, max_memory_GB: 8 }
Output:
- Core Deliverables: A Markdown file `/outputs/final_report.md`.
- Verification Artifacts: Console output of summary statistics and t-test results.
Inputs:
- `/outputs/similarity_results.json` (from Task 7)
- `/outputs/perplexity_results.json` (from Task 8)
- `/outputs/similarity_comparison.png` (from Task 7)
- `/outputs/perplexity_comparison.png` (from Task 8)
Guidelines:
- Create `src/analyze_results.py` and a `@stub.function` in `run.py`.
- Load the JSON results.
- Calculate and display summary statistics (mean, std dev).
- Perform an independent t-test (`scipy.stats.ttest_ind`) to check for statistically significant differences.
- Generate `/outputs/final_report.md` containing a summary table, p-values, an interpretation of the results, and the embedded plots.
Additional Context: This final task concludes the hypothesis test by interpreting the generated evidence.