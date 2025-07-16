Goal: Evaluate generated ideas using cosine similarity against future papers.
Budget: { gpu_type: "A10G", max_hours: 1, max_memory_GB: 24 }
Output:
- Core Deliverables: A JSON file `/outputs/similarity_results.json`.
- Verification Artifacts: A box plot `/outputs/similarity_comparison.png` comparing the groups.
Inputs:
- `/outputs/control_ideas.json` (from Task 4)
- `/outputs/mashing_ideas.json` (from Task 5)
- `/outputs/future_predecessor_map.json` (from Task 2)
- `src/embedder.py` (from Task 6)
Guidelines:
- Create `src/evaluate_similarity.py` and a `@stub.function(gpu="A10G")` in `run.py`.
- Fetch the abstracts of all "future papers" identified in `/outputs/future_predecessor_map.json`.
- For the experimental group, calculate the cosine similarity between the embedding of each `generated_idea` and the embedding of its specific `target_future_paper` abstract.
- For the control group, calculate the cosine similarity of each control idea against *all* available future paper abstracts and record the maximum similarity score for each control idea.
- Save scores to `/outputs/similarity_results.json` as `{"control_scores": [...], "mashing_scores": [...]}`.
- Generate and save a box plot comparing the score distributions.
Additional Context: This task quantifies the semantic relevance of generated ideas.