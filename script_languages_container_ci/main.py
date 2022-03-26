#! /usr/bin/env python3
#
from script_languages_container_ci.cli.cli import cli
# noinspection PyUnresolvedReferences
from script_languages_container_ci.cli.commands import (
    run_ci
)

if __name__ == '__main__':
    cli()
