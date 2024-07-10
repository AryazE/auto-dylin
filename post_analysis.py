import fire
import tempfile
from pathlib import Path
from dynapyt.post_run import post_run


def post_analysis(uid: str, test_workflow: str):
    temp_dir = tempfile.gettempdir()
    coverage_dir = Path(temp_dir) / f"dynapyt_coverage-{uid}"
    output_dir = f"dynapyt_output-{uid}"
    post_run(coverage_dir, output_dir)
    with open(test_workflow, "r") as f:
        full_workflow = f.read()
    return full_workflow


if __name__ == "__main__":
    fire.Fire(post_analysis)
