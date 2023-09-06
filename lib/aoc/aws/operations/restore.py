"""AoC on AWS restore module.

This module performs the standard operations for restoring an
AoC deployment on AWS cloud.
"""
from typing import List
from typing import TypedDict

from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.ops_container import OpsContainer

__all__ = [
    "AocAwsRestore",
    "AocAwsRestoreDataVars",
    "AocAwsRestoreDataExtraVars",
    "AocAwsRestoreStackResult",
]


class AocAwsRestoreDataExtraVars(TypedDict, total=False):
    """AoC default restore operations playbook data extra vars."""

    # aws_backup_iam_role_arn: str  # optional
    aws_backup_name: str  # backup object returned from backup playbook
    # aws_backup_restore_point_arn: str  # optional
    # aws_backup_vault_name: str  # optional
    # aws_rds_db_snapshot_arn: str  # optional
    aws_region: str
    aws_s3_bucket: str
    aws_ssm_bucket_name: str


class AocAwsRestoreDataVars(TypedDict, total=False):
    """AoC default restore operations playbook data vars."""

    cloud_credentials_path: str
    deployment_name: str
    extra_vars: AocAwsRestoreDataExtraVars


class AocAwsRestoreStackResult(TypedDict):
    """AoC stack restore results."""

    playbook_output: str
    playbook_result: bool


class AocAwsRestore(OpsContainer):
    """AocAwsRestore Class."""

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: BaseHostManager,
        command_generator_vars: AocAwsRestoreDataVars,
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

        self.command_generator_vars: AocAwsRestoreDataVars = command_generator_vars

    def populate_command_generator_args(self) -> None:
        """Performs any setup required to run command generator playbooks."""
        self.command_args: List[str] = [
            f'aws_foundation_stack_name={self.command_generator_vars["deployment_name"]}',
            f'aws_backup_name={self.command_generator_vars["extra_vars"]["aws_backup_name"]}',
            f'aws_region={self.command_generator_vars["extra_vars"]["aws_region"]}',
            f'aws_s3_bucket={self.command_generator_vars["extra_vars"]["aws_s3_bucket"]}',
            f'aws_ssm_bucket_name={self.command_generator_vars["extra_vars"]["aws_ssm_bucket_name"]}',
        ]
        self.command = "redhat.ansible_on_clouds.aws_restore_stack"
        self.env_vars = {
            "ANSIBLE_CONFIG": "../aws-ansible.cfg",
            "DEPLOYMENT_NAME": f'{self.command_generator_vars["deployment_name"]}',
            "GENERATE_INVENTORY": "true",
            "CHECK_GENERATED_INVENTORY": "false",
            "PLATFORM": f"{self.cloud.upper()}",
        }
        self.volume_mounts = [
            f'{self.command_generator_vars["cloud_credentials_path"]}:/home/runner/.aws/credentials:ro',
        ]

    def restore_stack(self) -> AocAwsRestoreStackResult:
        """Performs stack restore."""
        self.populate_command_generator_args()

        output, result = self.run_container(
            name=f'{self.command_generator_vars["deployment_name"]}-restore-stack'
        )
        return AocAwsRestoreStackResult(
            playbook_output=output,
            playbook_result=result,
        )
