"""Operations Package.

This package contains additional packages/modules "libraries" that
handle Ansible On Clouds operations using the ops container image.
"""
from typing import Dict

from aoc_tests.container_engine import ContainerEngine


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
        """
        self.cloud: str = cloud
        self.aoc_version: str = aoc_version
        self.aoc_ops_image: str = aoc_ops_image
        self.aoc_ops_image_tag: str = aoc_ops_image_tag
        self.aoc_image_registry_username: str = aoc_image_registry_username
        self.aoc_image_registry_password: str = aoc_image_registry_password

        if not self.__validate():
            raise SystemExit(1)

        self.container_engine: ContainerEngine = ContainerEngine()

        self.setup()

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
