from exasol_script_languages_container_tool.cli.commands import run_db_test

from script_languages_container_ci.lib import print_docker_images, get_last_commit_message


def run_test(flavor: str):
    if "skip tests" not in get_last_commit_message():
        print(f"Running command 'run_db_test' with parameters {locals()} ")
        run_db_test.callback(flavor=f"flavors/{flavor}", workers=7)
        print(f"Running command 'run_db_test' for linker_namespace_sanity with parameters {locals()} ")
        run_db_test.callback(flavor=f"flavors/{flavor}", workers=7,
                    test_folder="test/linker_namespace_sanity", release_goal="base_test_build_run")
        print_docker_images()
    else:
        print("Skipping tests.")
