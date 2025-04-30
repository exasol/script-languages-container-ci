import os


def write_github_var(github_var: str, value: str) -> None:
    github_output = os.environ["GITHUB_OUTPUT"]
    with open(github_output, "a") as github_output_file:
        print(f"{github_var}={value}", file=github_output_file)