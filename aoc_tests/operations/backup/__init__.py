"""Backup package.

This package contains additional packages/modules "libraries" that
handle Ansible On Clouds offerings back up operations.
"""
from aoc_tests.operations import OperationsBase


class AocBackup(OperationsBase):
    """AocBackup Ansible Automation Platform Class."""

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
        super().__init__(
            cloud,
            aoc_version,
            aoc_ops_image,
            aoc_ops_image_tag,
            aoc_image_registry_username,
            aoc_image_registry_password,
        )

        if not self.__validate():
            raise SystemExit(1)

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        # TODO: Implement this/should we validate anything?
        return True

    def run(self) -> bool:
        """Initiates/performs backup operation."""
        self.container_engine.client.containers.run(
            f"{self.aoc_ops_image}:{self.aoc_ops_image_tag}", "command_generator_vars"
        )
        return True
