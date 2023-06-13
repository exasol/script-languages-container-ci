from inspect import cleandoc
from pathlib import Path
from typing import Callable, Protocol

from exasol_script_languages_container_ci.lib.common import _get_docker_images


class CIStepOutputPrinterProtocol(Protocol):

    def print_docker_images(self):
        raise NotImplementedError()

    def print_file(self, filename: Path):
        raise NotImplementedError()


class CIStepOutputPrinter(CIStepOutputPrinterProtocol):

    def __init__(self, writer: Callable[[str], None]):
        self._writer = writer

    def print_docker_images(self):
        """
        Prints all docker images whith "exa" in it's name to stdout.
        :return: None
        """

        self._writer(cleandoc("""
            {seperator}
            Printing docker images
            {seperator}
            {images}""").format(
            seperator=20 * "=", images="\n".join(_get_docker_images())
        ))

    def print_file(self, filename: Path):
        """
        Print the file's content to the writer.
        """
        with open(filename, "r") as f:
            self._writer(f.read())
