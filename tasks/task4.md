Goal: Generate and save a set of baseline research ideas for the control group using the configured model.
Budget: { gpu_type: "A10G", max_hours: 1, max_memory_GB: 24 }
Output:
- Core Deliverables: A JSON file `/outputs/control_ideas.json`.
- Verification Artifacts: A log file `/outputs/control_generation.log` printing each generated idea.
Inputs:
- `/outputs/config.json` (from Task 1)
- `src/idea_generator.py` (from Task 3)
Guidelines:
- Create `src/run_control.py` and add a `@stub.function(gpu="A10G")` to `run.py`.
- Load the `llm_model_name` from `/outputs/config.json`.
- Use the `generate_control_idea` function from `src/idea_generator.py`.
- Generate at least 50 distinct research ideas to create a robust control set.
- Save results to `/outputs/control_ideas.json` as a list of strings.
- Use a fixed random seed `seed=42`.
Additional Context: This task executes the control arm of the experiment.