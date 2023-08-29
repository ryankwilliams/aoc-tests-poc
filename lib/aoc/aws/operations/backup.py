"""AoC on AWS backup module.

This module performs the standard operations for backing up an
AoC deployment on AWS cloud.
"""
import typing
from typing import Dict
from typing import List
from typing import TypedDict

import pytest

from lib.aoc.ops_container_image import OpsContainerImage

__all__ = [
    "AocAwsBackup",
    "AocAwsBackupDataVars",
    "AocAwsBackupDataExtraVars",
]


class AocAwsBackupDataExtraVars(TypedDict, total=False):
    """AoC default backup operations playbook data extra vars."""

    aws_backup_iam_role_arn: str
    aws_backup_vault_name: str
    aws_region: str
    aws_s3_bucket: str
    aws_ssm_bucket_name: str
    backup_prefix: str


class AocAwsBackupDataVars(TypedDict, total=False):
    """AoC default backup operations playbook data vars."""

    cloud_credentials_path: str
    deployment_name: str
    extra_vars: AocAwsBackupDataExtraVars


class AocAwsBackup(OpsContainerImage):
    """AocAwsBackup Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: pytest.fixture,
        command_generator_vars: AocAwsBackupDataVars,
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

        self.command_generator_vars: AocAwsBackupDataVars = command_generator_vars
        self.command_generator_setup()

    def command_generator_setup(self) -> None:
        """Performs any setup required to run command generator playbooks."""
        container_command_args: List[str] = [
            f'aws_foundation_stack_name={self.command_generator_vars["deployment_name"]}',
            f'aws_region={self.command_generator_vars["extra_vars"]["aws_region"]}',
            f'aws_backup_vault_name={self.command_generator_vars["extra_vars"]["aws_backup_vault_name"]}',
            f'aws_backup_iam_role_arn={self.command_generator_vars["extra_vars"]["aws_backup_iam_role_arn"]}',
            f'aws_s3_bucket={self.command_generator_vars["extra_vars"]["aws_s3_bucket"]}',
        ]

        if self.aoc_version != "2.3":
            container_command_args.extend(
                [
                    f'aws_ssm_bucket_name={self.command_generator_vars["extra_vars"]["aws_ssm_bucket_name"]}',
                    f'backup_prefix={self.command_generator_vars["extra_vars"]["backup_prefix"]}',
                ]
            )

        self.container_command_args = container_command_args
        self.container_command = "redhat.ansible_on_clouds.aws_backup_stack"
        self.container_env_vars = {
            "ANSIBLE_CONFIG": "TODO",
            "DEPLOYMENT_NAME": f'{self.command_generator_vars["deployment_name"]}',
            "GENERATE_INVENTORY": "true",
            "PLATFORM": f"{self.cloud.upper()}",
        }

        self.container_volume_mount = [
            f'{self.command_generator_vars["cloud_credentials_path"]}:/home/runner/.aws/credentials:ro',
        ]

    def validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        return self.validate_command_generator_vars(
            typing.cast(Dict[str, str], self.command_generator_vars)
        )
