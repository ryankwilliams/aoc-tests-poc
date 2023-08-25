"""AoC on GCP restoreRestore module.

This module performs the standard operations for backing up an
AoC deployment on GCP cloud.
"""
from typing import TypedDict
from typing import Union

import pytest

from tests.lib.operations import OperationsBase

__all__ = [
    "AocGcpRestore",
    "AocGcpRestoreDataVars",
    "Aoc23GcpRestoreDataVars",
    "AocGcpRestoreAvailableVars",
]


class AocGcpBackUpDataExtraVars(TypedDict, total=False):
    """AoC default restore operations playbook data extra vars."""

    # TODO: Implement typed dict
    todo: str


class AocGcpRestoreDataVars(TypedDict, total=False):
    """AoC default restore operations playbook data vars."""

    # TODO: Implement typed dict
    todo: str


class Aoc23GcpRestoreDataVars(AocGcpRestoreDataVars):
    """AoC 2.3 gcp restore operations playbook data vars."""

    pass


AocGcpRestoreAvailableVars = Union[Aoc23GcpRestoreDataVars, AocGcpRestoreDataVars]


class AocGcpRestore(OperationsBase):
    """AocGcpRestore Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: pytest.fixture,
        command_generator_vars: AocGcpRestoreAvailableVars,
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

        self.command_generator_vars: AocGcpRestoreAvailableVars = command_generator_vars

        # TODO: Populate the correct command with arguments
        self.command = "command_generator_vars"

        if not self.__validate():
            raise SystemExit(1)

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing restores.

        :return: the overall result of the validations performed
        """
        # TODO: Implement this/should we validate anything?
        return True
