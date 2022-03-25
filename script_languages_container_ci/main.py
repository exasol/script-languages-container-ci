#! /usr/bin/env python3
#
from slc_ci.cli.cli import cli
# noinspection PyUnresolvedReferences
from slc_ci.cli.commands import (
    health,
    generate_buildspec,
    deploy_source_credentials,
    deploy_ci_build
)

if __name__ == '__main__':
    cli()