import click

github_options = [
    click.option(
        "--github-output-var",
        type=str,
        required=True,
        help="Sets the github variable where the result of the operation will be stored.",
    )
]

github_event_options = [
    click.option(
        "--github-event",
        type=str,
        required=True,
        help="Indicates the github event which triggered the call.",
    )
]
