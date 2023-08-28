"""AoC on AWS restore module.

This module performs the standard operations for restoring an
AoC deployment on AWS cloud.
"""
from typing import TypedDict
from typing import Union

import pytest

from lib.aoc.ops_container_image import OpsContainerImage

__all__ = [
    "AocAwsRestore",
    "AocAwsRestoreDataVars",
    "Aoc23AwsRestoreDataVars",
    "AocAwsRestoreAvailableVars",
]


class AocAwsRestoreDataExtraVars(TypedDict, total=False):
    """AoC default restore operations playbook data extra vars."""

    aws_restore_iam_role: str
    aws_restore_vault_name: str
    aws_region: str
    aws_s3_bucket: str


class AocAwsRestoreDataVars(TypedDict, total=False):
    """AoC default restore operations playbook data vars."""

    cloud_credentials_path: str
    deployment_name: str
    extra_vars: AocAwsRestoreDataExtraVars


class Aoc23AwsRestoreDataVars(TypedDict, total=False):
    """AoC 2.3 restore operations playbook data vars."""

    cloud_credentials_path: str
    extra_vars: AocAwsRestoreDataExtraVars


AocAwsRestoreAvailableVars = Union[Aoc23AwsRestoreDataVars, AocAwsRestoreDataVars]


class AocAwsRestore(OpsContainerImage):
    """AocAwsRestore Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: pytest.fixture,
        command_generator_vars: AocAwsRestoreAvailableVars,
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
            "aws",
            aoc_version,
            aoc_ops_image,
            aoc_ops_image_tag,
            aoc_image_registry_username,
            aoc_image_registry_password,
            ansible_module,
        )

        self.command_generator_vars: AocAwsRestoreAvailableVars = command_generator_vars

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
