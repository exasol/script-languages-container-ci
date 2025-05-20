from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.ci_push_test_container import CIPushTestContainer


def test(
    test_containers_folder,
):
    test_type = "successful"
    input_commit_sha = "123"
    test_container_folder = str(test_containers_folder / test_type)
    with LocalDockerRegistryContextManager("test_ci_push_test_container") as registry:
        CIPushTestContainer().push_test_container(
            build_docker_repository=registry.name,
            force=True,
            commit_sha=input_commit_sha,
            docker_user=None,
            docker_password=None,
            test_container_folder=test_container_folder,
        )
        expected_images = {
            "name": "test_ci_push_test_container",
            "tags": [
                f"123_db-test-container_RHAJNDFIQLI4HPWH6PJXBXJ3GPZAHO6T6G6Z5QDM3MKBNPN2AOGQ",
            ],
        }
        assert expected_images["name"] == registry.images["name"] and set(
            expected_images["tags"]
        ) == set(registry.images["tags"])
