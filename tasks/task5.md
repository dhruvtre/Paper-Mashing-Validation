Goal: Generate "mashed" research ideas by randomly pairing predecessor papers for each future paper.
Budget: { gpu_type: "A10G", max_hours: 2, max_memory_GB: 24 }
Output:
- Core Deliverables: A JSON file `/outputs/mashing_ideas.json`.
- Verification Artifacts: A log file `/outputs/mashing_generation.log` printing each generated idea and its source pair.
Inputs:
- `/outputs/config.json` (from Task 1)
- `/outputs/future_predecessor_map.json` (from Task 2)
- `src/idea_generator.py` (from Task 3)
Guidelines:
- Create `src/run_mashing.py` and add a `@stub.function(gpu="A10G")` to `run.py`.
- Load the `llm_model_name` from `/outputs/config.json`.
- Load `/outputs/future_predecessor_map.json`.
- **Pairing Logic:** For each `future_paper_id` that has at least two predecessors:
  1.  Randomly select two distinct `predecessor_id`s from its list. This forms your pair.
- For each pair, fetch the abstracts of the two predecessor papers using the `arxiv` or `semanticscholar` library.
- Call `generate_mashing_idea` with the abstracts.
- Save results to `/outputs/mashing_ideas.json`. Each entry: `{"source_pair": ["<predecessor_A_id>", "<predecessor_B_id>"], "target_future_paper": "<future_paper_id>", "generated_idea": "..."}`.
- Use a fixed random seed `seed=42` for the random pairing.
Additional Context: This task executes the experimental arm, now with the pairing logic explicitly included.