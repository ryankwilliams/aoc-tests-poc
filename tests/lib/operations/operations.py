"""Operations Package.

This package contains additional packages/modules "libraries" that
handle Ansible On Clouds operations using the ops container image.
"""
from typing import Dict

import pytest

from tests.lib.container_engine import ContainerEngine


class OperationsBase:
    """OperationsBase Class."""

    def __init__(
        self,
        cloud: str,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: pytest.fixture,
    ) -> None:
        """Constructor.

        :param cloud: the cloud provider AAP is deployed into
        :param aoc_version: the aoc version deployed
        :param aoc_ops_image: the aoc operations container image
        :param aoc_ops_image_tag: the aoc operations container image tag
        :param aoc_image_registry_username: the username to authenticate with
            the image registry holding aoc operations image
        :param aoc_image_registry_password: the password to authenticate with
            the image registry holding aoc operations image
        :param ansible_module: the pytest ansible module fixture
        """
        self.cloud: str = cloud
        self.aoc_version: str = aoc_version
        self.aoc_ops_image: str = aoc_ops_image
        self.aoc_ops_image_tag: str = aoc_ops_image_tag
        self.aoc_image_registry_username: str = aoc_image_registry_username
        self.aoc_image_registry_password: str = aoc_image_registry_password

        if not self.__validate():
            raise SystemExit(1)

        self.container_engine = ContainerEngine(ansible_module)

        self._command: str = ""

        self.setup()

    @property
    def command(self) -> str:
        """Returns the command string to run within the command generator vars container."""
        return self._command

    @command.setter
    def command(self, value: str) -> None:
        """Sets the command string value for the command generator vars container."""
        self._command = value

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        result: bool = True

        validation_matrix: Dict[str, str] = {
            "AoC operations image": self.aoc_ops_image,
            "AoC operations image tag": self.aoc_ops_image_tag,
            "AoC operations image registry username": self.aoc_image_registry_username,
            "AoC operations image registry password": self.aoc_image_registry_password,
        }

        for key, value in validation_matrix.items():
            if value == "":
                print(f"{key} is not set. Please verify it was set and try again.\n")
                result = False

        return result

    def setup(self) -> None:
        """Performs setup operations to perform aoc backups."""
        self.container_engine.registry_login(
            self.aoc_ops_image.split("/")[0],
            self.aoc_image_registry_username,
            self.aoc_image_registry_password,
        )
        self.container_engine.pull_image(self.aoc_ops_image, self.aoc_ops_image_tag)

    def run(self) -> bool:
        """Initiates/performs backup operation."""
        self.container_engine.run(
            f"{self.aoc_ops_image}:{self.aoc_ops_image_tag}",
            self.command,
        )
        return True
