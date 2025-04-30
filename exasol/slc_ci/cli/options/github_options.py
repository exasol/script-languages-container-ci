import click

github_options = [
    click.option(
        "--github-var",
        type=str,
        required=True,
        help="Sets the github variable where the result of the operation will be stored."
    )
]