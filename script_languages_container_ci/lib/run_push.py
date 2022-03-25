from exasol_script_languages_container_tool.cli.commands import push

from script_languages_container_ci.lib import print_docker_images


def run_push(flavor: str,
             target_docker_repository: str, target_docker_tag_prefix: str,
             docker_user: str, docker_password: str):
    print(f"Running command 'push' with parameters: {locals()} ")
    push.callback(flavor=f"flavors/{flavor}", push_all=True, force_push=True, workers=7,
                  target_docker_repository_name=target_docker_repository,
                  target_docker_tag_prefix=target_docker_tag_prefix,
                  target_docker_username=docker_user, target_docker_password=docker_password)
    print_docker_images()
