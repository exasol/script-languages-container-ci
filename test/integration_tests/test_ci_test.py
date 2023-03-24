from pathlib import Path

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest


def test():
    script_path = Path(__file__).absolute().parent
    flavor_path = str(script_path / "flavors" / "real-test-flavor")
    test_container_folder = str(script_path / "test_container")
    run_db_test_flavor_result, run_db_test_linkernamespace = \
        CIExecuteTest().execute_tests(
            flavor_path=(flavor_path,),
            docker_user=None,
            docker_password=None,
            test_container_folder=test_container_folder
        )
    assert flavor_path in run_db_test_flavor_result.test_results_per_flavor \
           and "release" in run_db_test_flavor_result.test_results_per_flavor[flavor_path].test_results_per_release_goal \
           and flavor_path in run_db_test_linkernamespace.test_results_per_flavor \
           and "base_test_build_run" in run_db_test_linkernamespace.test_results_per_flavor[
               flavor_path].test_results_per_release_goal
