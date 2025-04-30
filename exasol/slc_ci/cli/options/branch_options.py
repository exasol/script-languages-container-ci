import click

branch_option = click.option(
    "--branch-name",
    type=str,
    required=True,
    help="In case of a PR, the source branch of the PR.",
)

base_branch_option = click.option(
    "--base-branch-name",
    type=str,
    required=True,
    help="In case of a PR, the target branch of the PR.",
)

branch_options = [branch_option, base_branch_option]
