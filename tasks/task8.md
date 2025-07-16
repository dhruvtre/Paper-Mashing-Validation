Goal: Evaluate prompt effectiveness by calculating the perplexity of future papers.
Budget: { gpu_type: "A10G", max_hours: 2, max_memory_GB: 30 }
Output:
- Core Deliverables: A JSON file `/outputs/perplexity_results.json`.
- Verification Artifacts: A box plot `/outputs/perplexity_comparison.png` comparing the groups.
Inputs:
- `/outputs/config.json` (from Task 1)
- `/outputs/mashing_ideas.json` (from Task 5)
- `src/idea_generator.py` (from Task 3)
Guidelines:
- Create `src/evaluate_perplexity.py` and a `@stub.function(gpu="A10G")` in `run.py`.
- Load the `perplexity_model_name` from `/outputs/config.json`.
- Load `/outputs/mashing_ideas.json`. For each entry:
  1.  Fetch the abstracts for the two `source_pair` papers and the one `target_future_paper`.
  2.  Construct the two prompts using the exact templates from `src/idea_generator.py`: one for control and one for mashing the two source papers.
  3.  Calculate the perplexity of the `target_future_paper`'s abstract, conditioned on each of the two prompts.
- Save perplexity scores to `/outputs/perplexity_results.json`.
- Generate and save a box plot comparing the distributions.
Additional Context: This task tests which prompt makes the actual future paper a more "likely" continuation.