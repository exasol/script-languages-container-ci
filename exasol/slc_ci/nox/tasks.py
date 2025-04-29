from __future__ import annotations

__all__ = [
    "run_find_available_flavors",
    "run_get_build_runner_for_flavor",
    "run_check_if_build_needed",
]

import argparse
import json
import os

import nox
from nox import Session
from slc_build_config import (  # type: ignore # pylint: disable=(import-error),
    SLC_BUILD_CONFIG,
)

import exasol.slc_ci.api as api
from exasol.slc_ci.nox.arg_parser_builder import ArgumentParserBuilder


def _write_github_output(args: argparse.Namespace, value: str) -> None:
    github_output = os.environ["GITHUB_OUTPUT"]
    with open(github_output, "a") as github_output_file:
        print(f"{args.github_var}={value}", file=github_output_file)


@nox.session(name="ci:find-available-flavors", python=False)
def run_find_available_flavors(session: Session) -> None:
    args = ArgumentParserBuilder(session).with_github_var().parse()
    flavor_list = list(api.get_flavors(SLC_BUILD_CONFIG))
    _write_github_output(args, json.dumps(flavor_list))


@nox.session(name="ci:get-build-runner-for-flavor", python=False)
def run_get_build_runner_for_flavor(session: nox.Session):
    """
    Returns the runner for a flavor
    """
    args = ArgumentParserBuilder(session).with_flavor().with_github_var().parse()
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)
    _write_github_output(args, flavor_config.build_runner)


@nox.session(name="ci:check-if-build-need", python=False)
def run_check_if_build_needed(session: nox.Session):
    """
    Returns "True" if rebuild and test is needed, "False" otherwise
    """
    args = (
        ArgumentParserBuilder(session)
        .with_flavor()
        .with_branch_name()
        .with_github_var()
        .parse()
    )
    need_to_build = api.check_if_build_needed(
        branch_name=args.branch_name, flavor=args.flavor, build_config=SLC_BUILD_CONFIG
    )
    _write_github_output(args, "True" if need_to_build else "False")
