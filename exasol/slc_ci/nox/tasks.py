from __future__ import annotations

__all__ = [
    "run_find_available_flavors",
    "run_get_build_runner_for_flavor",
    "run_get_test_runner_for_flavor",
    "run_get_test_set_names_for_flavor",
    "run_db_tests",
    "run_check_if_build_needed",
    "run_export_and_scan_vulnerabilities",
]

import argparse
import json
import os

import nox
from nox import Session
from slc_build_config import SLC_BUILD_CONFIG #type: ignore # pylint: disable=(import-error),

import exasol.slc_ci.api as api
from exasol.slc_ci.nox.arg_parser_builder import ArgumentParserBuilder


def _write_github_output(args: argparse.Namespace, value: str) -> None:
    github_output = os.environ["GITHUB_OUTPUT"]
    with open(github_output, "a") as github_output_file:
        print(f"{args.github_var}={value}", file=github_output_file)


@nox.session(name="ci:find-available-flavors", python=False)
def run_find_available_flavors(session: Session) -> None:
    args = ArgumentParserBuilder(session).with_github_var().parse()
    flavor_list = list(api.get_flavors(SLC_BUILD_CONFIG.flavors_path))
    _write_github_output(args, json.dumps(flavor_list))


@nox.session(name="ci:get-build-runner-for-flavor", python=False)
def run_get_build_runner_for_flavor(session: nox.Session):
    """
    Returns the runner for a flavor
    """
    args = ArgumentParserBuilder(session).with_flavor().with_github_var().parse()
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)
    _write_github_output(args, flavor_config.build_runner)


@nox.session(name="ci:get-test-runner-for-flavor", python=False)
def run_get_test_runner_for_flavor(session: nox.Session):
    """
    Returns the test-runner for a flavor
    """
    args = ArgumentParserBuilder(session).with_flavor().with_github_var().parse()
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)
    _write_github_output(args, flavor_config.test_config.test_runner)


@nox.session(name="ci:get-test-set-names-for-flavor", python=False)
def run_get_test_set_names_for_flavor(session: nox.Session):
    """
    Returns the test-set names for a flavor as JSON list
    """
    args = ArgumentParserBuilder(session).with_flavor().with_github_var().parse()
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)
    test_sets_names = [
        test_set.name for test_set in flavor_config.test_config.test_sets
    ]
    _write_github_output(args, json.dumps(test_sets_names))


@nox.session(name="ci:run-db-tests", python=False)
def run_db_tests(session: nox.Session):
    """
    Runs integration tests
    """
    args = (
        ArgumentParserBuilder(session)
        .with_flavor()
        .with_docker()
        .with_testset_name()
        .with_slc_directory()
        .parse()
    )
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)

    api.run_tests(
        flavor=args.flavor,
        slc_directory=args.slc_directory,
        flavor_config=flavor_config,
        build_config=SLC_BUILD_CONFIG,
        test_set_name=args.test_set_name,
        docker_user=args.docker_user,
        docker_password=args.docker_password,
    )


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


@nox.session(name="ci:export-and-scan-vulnerabilities", python=False)
def run_export_and_scan_vulnerabilities(session: nox.Session):
    """
    Exports the SLC and runs the vulnerabilities checks. Returns the path to the cached SLC.
    """
    args = (
        ArgumentParserBuilder(session)
        .with_flavor()
        .with_branch_name()
        .with_docker()
        .with_github_var()
        .with_commit_sha()
        .parse()
    )

    slc_cache_file = api.export_and_scan_vulnerabilities(
        flavor=args.flavor,
        build_config=SLC_BUILD_CONFIG,
        branch_name=args.branch_name,
        docker_user=args.docker_user,
        docker_password=args.docker_password,
        commit_sha=args.commit_sha,
    )
    _write_github_output(args, str(slc_cache_file))
