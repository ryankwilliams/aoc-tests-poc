"""AoC on AWS backup module.

This module performs the standard operations for backing up an
AoC deployment on AWS cloud.
"""
from typing import List
from typing import TypedDict

import botocore.exceptions
from boto3.session import Session
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef
from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.ops_container import OpsContainer

__all__ = [
    "AocAwsBackup",
    "AocAwsBackupDataVars",
    "AocAwsBackupDataExtraVars",
    "AocAwsBackupStackResult",
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


class AocAwsBackupStackResult(TypedDict):
    """Aoc stack backup results."""

    playbook_output: str
    playbook_result: bool
    backup_object_name: str


class AocAwsBackup(OpsContainer):
    """AocAwsBackup class.

    This class handles all operations to perform an aoc on aws stack backup.
    Perform the following to initiate a backup:
        1. Instantiate the class constructing an object
            > aoc_aws_backup = AocAwsBackup(...)
        2. Call the `setup` method to perform pre backup operations
            > aoc_aws_backup.setup()
        3. Call the `backup_stack` method to perform backup
            > aoc_aws_backup.backup_stack()
    """

    def __init__(
        self,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: BaseHostManager,
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
        self.ansible_module: BaseHostManager = ansible_module

        self.command_generator_vars: AocAwsBackupDataVars = command_generator_vars

    def populate_command_generator_args(self) -> None:
        """Performs any setup required to run command generator playbooks."""
        self.command_args: List[str] = [
            f'aws_foundation_stack_name={self.command_generator_vars["deployment_name"]}',
            f'aws_region={self.command_generator_vars["extra_vars"]["aws_region"]}',
            f'aws_backup_vault_name={self.command_generator_vars["extra_vars"]["aws_backup_vault_name"]}',
            f'aws_backup_iam_role_arn={self.command_generator_vars["extra_vars"]["aws_backup_iam_role_arn"]}',
            f'aws_s3_bucket={self.command_generator_vars["extra_vars"]["aws_s3_bucket"]}',
        ]

        if self.aoc_version != "2.3":
            self.command_args.extend(
                [
                    f'aws_ssm_bucket_name={self.command_generator_vars["extra_vars"]["aws_ssm_bucket_name"]}',
                    f'backup_prefix={self.command_generator_vars["extra_vars"]["backup_prefix"]}',
                ]
            )

        self.command = "redhat.ansible_on_clouds.aws_backup_stack"
        self.env_vars = {
            "ANSIBLE_CONFIG": "../aws-ansible.cfg",
            "DEPLOYMENT_NAME": f'{self.command_generator_vars["deployment_name"]}',
            "GENERATE_INVENTORY": "true",
            "PLATFORM": f"{self.cloud.upper()}",
        }
        self.volume_mounts = [
            f'{self.command_generator_vars["cloud_credentials_path"]}:/home/runner/.aws/credentials:ro',
        ]

    def create_s3_bucket(self) -> bool:
        """Create s3 bucket to store backup files."""
        result = self.ansible_module.s3_bucket(
            name=self.command_generator_vars["extra_vars"]["aws_s3_bucket"],
            state="present",
        )
        if "failed" in result.contacted["localhost"]:
            print(result.contacted["localhost"]["msg"])
            return False
        return True

    def delete_s3_bucket(self) -> bool:
        """Delete s3 bucket holding backup files."""
        result = self.ansible_module.s3_bucket(
            name=self.command_generator_vars["extra_vars"]["aws_s3_bucket"],
            state="absent",
        )
        if "failed" in result.contacted["localhost"]:
            print(result.contacted["localhost"]["msg"])
            return False
        return True

    def get_s3_backup_object(self) -> str:
        """Gets the stack backup object stored in the s3 bucket."""
        # TODO: Submit an RFE to playbook to have a final task to write
        #   the bucket name to an output file for consumption.
        #   Need to mount new volume into container to fetch file
        bucket_name: str = self.command_generator_vars["extra_vars"]["aws_s3_bucket"]

        s3_client: S3Client = Session().client("s3")

        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            print(
                f'Unable to locate bucket {bucket_name}, server message: {e.response["Error"]["Message"]}'
            )
            return ""

        bucket_objects: ListObjectsV2OutputTypeDef = s3_client.list_objects_v2(
            Bucket=bucket_name, Delimiter="/"
        )

        return str(bucket_objects["CommonPrefixes"][-1]["Prefix"].strip("/"))

    def backup_stack(self) -> AocAwsBackupStackResult:
        """Performs stack backup."""
        backup_object_name: str = ""

        self.populate_command_generator_args()

        output, result = self.run_container(
            name=f'{self.command_generator_vars["deployment_name"]}-backup-stack'
        )

        if result:
            backup_object_name = self.get_s3_backup_object()

        return AocAwsBackupStackResult(
            backup_object_name=backup_object_name,
            playbook_output=output,
            playbook_result=result,
        )
