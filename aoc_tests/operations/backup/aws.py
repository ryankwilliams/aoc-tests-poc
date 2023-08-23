"""AoC on AWS Backup module.

This module performs the standard operations for backing up an
AoC deployment on AWS cloud.
"""
from typing import TypedDict
from typing import Union

from aoc_tests.operations.backup import AocBackup

__all__ = [
    "AocAwsBackup",
    "AocAwsBackupDataVars",
    "Aoc23AwsBackupDataVars",
    "AocAwsBackupAvailableVars",
]


class AocAwsBackupDataExtraVars(TypedDict, total=False):
    """AoC default backup operations playbook data extra vars."""

    aws_backup_iam_role: str
    aws_backup_vault_name: str
    aws_region: str
    aws_s3_bucket: str


class AocAwsBackupDataVars(TypedDict, total=False):
    """AoC default backup operations playbook data vars."""

    cloud_credentials_path: str
    deployment_name: str
    extra_vars: AocAwsBackupDataExtraVars


class Aoc23AwsBackupDataVars(TypedDict, total=False):
    """AoC 2.3 backup operations playbook data vars."""

    cloud_credentials_path: str
    extra_vars: AocAwsBackupDataExtraVars


AocAwsBackupAvailableVars = Union[Aoc23AwsBackupDataVars, AocAwsBackupDataVars]


class AocAwsBackup(AocBackup):
    """AocAwsBackup Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        data: AocAwsBackupAvailableVars,
    ) -> None:
        """Constructor.

        :param aoc_version: the aoc version deployed
        :param aoc_ops_image: the aoc operations container image
        :param aoc_ops_image_tag: the aoc operations container image tag
        :param aoc_image_registry_username: the username to authenticate with
            the image registry holding aoc operations image
        :param aoc_image_registry_password: the password to authenticate with
            the image registry holding aoc operations image
        """
        super().__init__(
            "aws",
            aoc_version,
            aoc_ops_image,
            aoc_ops_image_tag,
            aoc_image_registry_username,
            aoc_image_registry_password,
        )

        self.data: AocAwsBackupAvailableVars = data

        if not self.__validate():
            raise SystemExit(1)

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        # TODO: Implement this/should we validate anything?
        return True
