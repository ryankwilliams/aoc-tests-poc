"""AoC on GCP restore module.

This module performs the standard operations for backing up an
AoC deployment on GCP cloud.
"""
import typing
from typing import Dict
from typing import TypedDict

from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.ops_container import OpsContainer

__all__ = [
    "AocGcpRestore",
    "AocGcpRestoreDataVars",
]


class AocGcpBackUpDataExtraVars(TypedDict, total=False):
    """AoC default restore operations playbook data extra vars."""

    # TODO: Implement typed dict
    todo: str


class AocGcpRestoreDataVars(TypedDict, total=False):
    """AoC default restore operations playbook data vars."""

    # TODO: Implement typed dict
    todo: str


class AocGcpRestore(OpsContainer):
    """AocGcpRestore Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: BaseHostManager,
        command_generator_vars: AocGcpRestoreDataVars,
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

        self.command_generator_vars: AocGcpRestoreDataVars = command_generator_vars
        self.command_generator_setup()

    def command_generator_setup(self) -> None:
        """Performs any setup required to run command generator playbooks."""
        # TODO: Implementation
        self.command = "command_generator_vars"

    def validate(self) -> bool:
        """Validates any necessary input prior to performing restores.

        :return: the overall result of the validations performed
        """
        return self.validate_command_generator_vars(
            typing.cast(Dict[str, str], self.command_generator_vars)
        )
