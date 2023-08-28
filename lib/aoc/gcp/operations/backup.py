"""AoC on GCP backup module.

This module performs the standard operations for backing up an
AoC deployment on GCP cloud.
"""
from typing import TypedDict
from typing import Union

import pytest

from lib.aoc.ops_container_image import OpsContainerImage

__all__ = [
    "AocGcpBackup",
    "AocGcpBackupDataVars",
    "Aoc23GcpBackupDataVars",
    "AocGcpBackupAvailableVars",
]


class AocGcpBackUpDataExtraVars(TypedDict, total=False):
    """AoC default backup operations playbook data extra vars."""

    # TODO: Implement typed dict
    todo: str


class AocGcpBackupDataVars(TypedDict, total=False):
    """AoC default backup operations playbook data vars."""

    # TODO: Implement typed dict
    todo: str


class Aoc23GcpBackupDataVars(AocGcpBackupDataVars):
    """AoC 2.3 gcp backup operations playbook data vars."""

    pass


AocGcpBackupAvailableVars = Union[Aoc23GcpBackupDataVars, AocGcpBackupDataVars]


class AocGcpBackup(OpsContainerImage):
    """AocGcpBackup Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: pytest.fixture,
        command_generator_vars: AocGcpBackupAvailableVars,
    ) -> None:
        """Constructor.

        :param aoc_version: the aoc version deployed
        :param aoc_ops_image: the aoc operations container image
        :param aoc_ops_image_tag: the aoc operations container image tag
        :param aoc_image_registry_username: the username to authenticate with
            the image registry holding aoc operations image
        :param aoc_image_registry_password: the password to authenticate with
            the image registry holding aoc operations image
        :param ansible_module: the pytest ansible module fixture
        :param command_generator_vars: the data to provide to aoc operations command generator playbooks
        """
        super().__init__(
            "gcp",
            aoc_version,
            aoc_ops_image,
            aoc_ops_image_tag,
            aoc_image_registry_username,
            aoc_image_registry_password,
            ansible_module,
        )

        self.command_generator_vars: AocGcpBackupAvailableVars = command_generator_vars

        # TODO: Populate the correct command with arguments
        self.command = "command_generator_vars"

        if not self.__validate():
            raise SystemExit(1)

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        # TODO: Implement this/should we validate anything?
        return True
