from __future__ import annotations

__all__ = [
    "run_find_available_flavors",
    "run_get_build_runner_for_flavor",
    "run_get_test_runner_for_flavor",
    "run_get_test_set_names_for_flavor",
    "run_db_tests",
    "run_check_if_build_needed",
]

import argparse
import json
from argparse import ArgumentParser
from pathlib import Path

import nox
from nox import Session
from slc_build_config import SLC_BUILD_CONFIG

import exasol.slc_ci.api as api


def _parse_flavor(session: Session) -> str:
    def parser() -> ArgumentParser:
        p = ArgumentParser(
            usage=f"nox -s {session.name} -- --flavor <flavor>",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        p.add_argument("--flavor", required=True)
        return p

    args = parser().parse_args(session.posargs)
    return args.flavor


@nox.session(name="ci:find-available-flavors", python=False)
def run_find_available_flavors(session: Session) -> None:
    flavor_list = list(api.get_flavors(SLC_BUILD_CONFIG.flavors_path))
    print(json.dumps(flavor_list))


@nox.session(name="ci:get-build-runner-for-flavor", python=False)
def run_get_build_runner_for_flavor(session: nox.Session):
    """
    Returns the runner for a flavor
    """
    flavor = _parse_flavor(session)
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, flavor)
    print(flavor_config.build_runner)


@nox.session(name="ci:get-test-runner-for-flavor", python=False)
def run_get_test_runner_for_flavor(session: nox.Session):
    """
    Returns the test-runner for a flavor
    """
    flavor = _parse_flavor(session)
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, flavor)
    print(flavor_config.test_config.test_runner)


@nox.session(name="ci:get-test-set-names-for-flavor", python=False)
def run_get_test_set_names_for_flavor(session: nox.Session):
    """
    Returns the test-set names for a flavor as JSON list
    """
    flavor = _parse_flavor(session)
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, flavor)
    test_sets_names = [test_set.name for test_set in flavor_config.test_config.test_sets]
    print(json.dumps(test_sets_names))


@nox.session(name="ci:run-db-tests", python=False)
def run_db_tests(session: nox.Session):
    """
    Runs integration tests
    """

    def parser() -> ArgumentParser:
        p = ArgumentParser(
            usage="nox -s run-db-tests -- --flavor <flavor> --test-set <test-set-name>",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        p.add_argument("--flavor", required=True)
        p.add_argument("--test-set-name", required=True)
        p.add_argument("--slc-directory", required=True)
        return p

    args = parser().parse_args(session.posargs)
    flavor_config = api.get_flavor_ci_model(SLC_BUILD_CONFIG, args.flavor)
    matched_test_set = [
        test_set
        for test_set in flavor_config.test_config.test_sets
        if test_set.name == args.test_set_name
    ]
    if len(matched_test_set) != 1:
        raise ValueError(f"Invalid test set name: {args.test_set_name}")
    test_set_folders = [folder for folder in matched_test_set[0].folders]
    slc_directory = Path(args.slc_directory)
    if not slc_directory.exists():
        raise ValueError(f"{args.slc_directory} does not exist")
    slc_files = list(slc_directory.glob(f"{args.flavor}*.tar.gz"))
    if len(slc_files) != 1:
        raise ValueError(
            f"{args.flavor} does not contain expected tar.gz file, but \n {slc_files}"
        )

    api.run_tests(
        flavor=args.flavor,
        slc_path=slc_files[0],
        test_folders=test_set_folders,
        docker_user=args.docker_user,
        docker_password=args.docker_password,
    )


@nox.session(name="ci:check-if-build-need", python=False)
def run_check_if_build_needed(session: nox.Session):
    """
    Returns "True" if rebuild and test is needed, "False" otherwise
    """

    def parser() -> ArgumentParser:
        p = ArgumentParser(
            usage="nox -s check-if-build-need -- --flavor <flavor> --branch-name <branch_name>",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        p.add_argument("--flavor", required=True)
        p.add_argument("--branch-name", required=True)
        return p

    args = parser().parse_args(session.posargs)
    need_to_build = api.check_if_build_needed(
        branch_name=args.branch_name, flavor=args.flavor, build_config=SLC_BUILD_CONFIG
    )
    print("True") if need_to_build else print("False")


@nox.session(name="ci:export-and-scan-vulnerabilities", python=False)
def run_export_and_scan_vulnerabilities(session: nox.Session):
    """
    Exports the SLC and runs the vulnerabilities checks. Returns the path to the cached SLC.
    """

    def parser() -> ArgumentParser:
        p = ArgumentParser(
            usage="nox -s check-if-build-need -- --flavor <flavor> --branch-name <branch_name> "
            "--docker-user <docker_user> --docker-password <docker_password> "
            "--commit-sha <commit_sha> --github-output $GITHUB_OUTPUT",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        p.add_argument("--flavor", required=True)
        p.add_argument("--branch-name", required=True)
        p.add_argument("--docker-user", required=True)
        p.add_argument("--docker-password", required=True)
        p.add_argument("--commit-sha", required=True)
        p.add_argument("--github-output", required=True)
        return p

    args = parser().parse_args(session.posargs)
    slc_cache_file = api.export_and_scan_vulnerabilities(
        flavor=args.flavor,
        build_config=SLC_BUILD_CONFIG,
        branch_name=args.branch_name,
        docker_user=args.docker_user,
        docker_password=args.docker_password,
        commit_sha=args.commit_sha,
    )
    with open(args.github_output, "a") as f:
        print(f"slc_path={slc_cache_file}", file=f)

