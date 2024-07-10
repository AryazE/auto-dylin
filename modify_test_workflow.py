import tempfile
import uuid
from pathlib import Path
import fire
from ruamel.yaml import YAML


def modify_workflow(workflow_file):
    with open(workflow_file, "r") as f:
        workflow = f.read()
    yaml = YAML()
    workflow = yaml.load(workflow)

    uid = str(uuid.uuid4())
    temp_dir = tempfile.gettempdir()
    coverage_dir = Path(temp_dir) / f"dynapyt_coverage-{uid}"
    coverage_dir.mkdir(parents=True, exist_ok=True)
    with open("analyses.txt", "r") as f:
        analyses = f.read().strip().split("\n")
    additional_steps = [
        {
            "name": "Instrumentation",
            "run": f"python -m dynapyt.run_instrumentation --directory . --analysis {analyses}",
        },
        {
            "name": "Add analyses file",
            "run": f"cp analyses.txt {temp_dir}/dynapyt_analyses-{uid}.txt",
        },
    ]

    dynapyt_envs = {
        "DYNAPYT_COVERAGE": str(coverage_dir),
        "DYNAPYT_SESSION_ID": uid,
    }

    for _, job in workflow["jobs"].items():
        checkout_point = 0
        for step_num, step in enumerate(job["steps"]):
            if "actions/checkout@" in step["uses"]:
                checkout_point = step_num + 1
            elif "test" in step["name"].lower() or "pytest" in step["run"]:
                if "env" in step:
                    step["env"].update(dynapyt_envs)
                else:
                    step["env"] = dynapyt_envs
        if checkout_point > 0:
            job["steps"] = (
                job["steps"][:checkout_point]
                + additional_steps
                + job["steps"][checkout_point:]
            )

    yaml.dump(workflow, Path(workflow_file))
    return f"uid={uid}"


if __name__ == "__main__":
    fire.Fire(modify_workflow)
