import logging
from typing import Optional, Tuple

from exasol.slc.internal.tasks.test.test_container_content import (
    build_test_container_content,
)
from exasol_integration_test_docker_environment.lib.api.build_test_container import (
    build_test_container,
)

from exasol.slc_ci.lib.ci_step_output_printer import (
    CIStepOutputPrinter,
    CIStepOutputPrinterProtocol,
)


class CIBuildTestContainer:

    def __init__(
        self, printer: CIStepOutputPrinterProtocol = CIStepOutputPrinter(logging.info)
    ):
        self._printer = printer

    def build_test_container(
        self,
        rebuild: bool,
        build_docker_repository: Optional[str],
        commit_sha: str,
        docker_user: str,
        docker_password: str,
        test_container_folder: str,
    ):
        """
        Build the test container with given commit SHA.
        """

        logging.info(
            f"Running command 'build_test_container' with parameters: {locals()}"
        )
        content = build_test_container_content(test_container_folder)
        test_container_image_infos = build_test_container(
            force_rebuild=rebuild,
            workers=7,
            test_container_content=content,
            source_docker_repository_name=build_docker_repository,
            source_docker_tag_prefix=commit_sha,
            source_docker_username=docker_user,
            source_docker_password=docker_password,
            log_level="WARNING",
            use_job_specific_log_file=True,
        )
        self._printer.print_exasol_docker_images()
