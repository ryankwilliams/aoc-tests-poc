"""Tests validating AoC on AWS backup/restore."""
import typing
from typing import Dict

import pytest
from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.aws.operations.backup import AocAwsBackup
from lib.aoc.aws.operations.backup import AocAwsBackupDataExtraVars
from lib.aoc.aws.operations.backup import AocAwsBackupDataVars
from lib.aoc.aws.operations.backup import AocAwsBackupStackResult
from lib.aoc.aws.operations.restore import AocAwsRestore
from lib.aoc.aws.operations.restore import AocAwsRestoreDataExtraVars
from lib.aoc.aws.operations.restore import AocAwsRestoreDataVars
from lib.aoc.aws.operations.restore import AocAwsRestoreStackResult


@pytest.fixture  # type: ignore
def aoc_aws_backup_stack(
    ansible_module: BaseHostManager,
    pytestconfig: pytest.Config,
) -> AocAwsBackup:
    """Fixture returning aoc aws backup operations."""

    command_generator_vars: AocAwsBackupDataVars = AocAwsBackupDataVars(
        cloud_credentials_path=pytestconfig.getoption("aoc_aws_credentials_path"),
        deployment_name=pytestconfig.getoption("aoc_stack_deployment_name"),
        extra_vars=AocAwsBackupDataExtraVars(
            aws_backup_iam_role_arn=pytestconfig.getoption(
                "aoc_aws_backup_iam_role_arn"
            ),
            aws_backup_vault_name=pytestconfig.getoption("aoc_aws_backup_vault_name"),
            aws_region=pytestconfig.getoption("aoc_aws_region"),
            aws_s3_bucket=pytestconfig.getoption("aoc_aws_backup_s3_bucket"),
            aws_ssm_bucket_name=pytestconfig.getoption(
                "aoc_aws_backup_ssm_bucket_name"
            ),
            backup_prefix=pytestconfig.getoption("aoc_aws_backup_prefix"),
        ),
    )

    return AocAwsBackup(
        aoc_version=pytestconfig.getoption("aoc_version"),
        aoc_ops_image=pytestconfig.getoption("aoc_ops_container_image"),
        aoc_ops_image_tag=pytestconfig.getoption("aoc_ops_container_image_tag"),
        aoc_image_registry_username=pytestconfig.getoption(
            "aoc_ops_container_image_registry_username"
        ),
        aoc_image_registry_password=pytestconfig.getoption(
            "aoc_ops_container_image_registry_password"
        ),
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


@pytest.fixture  # type: ignore
def aoc_aws_restore_stack(
    ansible_module: pytest.fixture,
    pytestconfig: pytest.Config,
) -> AocAwsRestore:
    """Fixture returning aoc aws restore operations."""
    command_generator_vars: AocAwsRestoreDataVars = AocAwsRestoreDataVars(
        cloud_credentials_path=pytestconfig.getoption("aoc_aws_credentials_path"),
        deployment_name=pytestconfig.getoption("aoc_stack_deployment_name"),
        extra_vars=AocAwsRestoreDataExtraVars(
            aws_backup_name=pytestconfig.getoption("aoc_aws_backup_vault_name"),
            aws_region=pytestconfig.getoption("aoc_aws_region"),
            aws_s3_bucket=pytestconfig.getoption("aoc_aws_backup_s3_bucket"),
            aws_ssm_bucket_name=pytestconfig.getoption(
                "aoc_aws_backup_ssm_bucket_name"
            ),
        ),
    )

    return AocAwsRestore(
        aoc_version=pytestconfig.getoption("aoc_version"),
        aoc_ops_image=pytestconfig.getoption("aoc_ops_container_image"),
        aoc_ops_image_tag=pytestconfig.getoption("aoc_ops_container_image_tag"),
        aoc_image_registry_username=pytestconfig.getoption(
            "aoc_ops_container_image_registry_username"
        ),
        aoc_image_registry_password=pytestconfig.getoption(
            "aoc_ops_container_image_registry_password"
        ),
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


@pytest.mark.aoc_aws_backup_restore_stack
class TestAoCAwsStackBackupRestore:
    """Test suite covering backup/restore operations for an AAP stack."""

    # TODO:
    #   1. Remove backup files (should happen pass or fail)
    #   2. Remove s3 bucket (should happen pass or fail)

    @pytest.mark.aoc_aws_backup_stack  # type: ignore
    def test_backup_stack(self, aoc_aws_backup_stack: AocAwsBackup) -> None:
        """Test verifies a stack can be backed up using the ops container image.

        Test procedure:
            1. Validate registry.redhat.io authentication/pull ops container image
                (Handled when fixture constructs AocAwsBackup class)
            2. Validate required test data for backup playbook is defined
            3. Generate the ops backup playbook extra vars
            4. Create s3 bucket to store backup files
            5. Run ops container targeting backup playbook w/extra vars
            6. Get the stack backup name to be used for restoring the stack
        Expected results:
            1. S3 bucket is created
            2. Ops container backup playbook finishes successfully
            3. Backup object exists in the s3 bucket
            4. Backup object name is in the playbook output
        """
        assert aoc_aws_backup_stack.validate_command_generator_vars(
            typing.cast(Dict[str, str], aoc_aws_backup_stack.command_generator_vars)
        )
        assert aoc_aws_backup_stack.create_s3_bucket()

        stack_backup_results: AocAwsBackupStackResult = (
            aoc_aws_backup_stack.backup_stack()
        )
        assert stack_backup_results["playbook_result"]
        assert (
            stack_backup_results["backup_object_name"]
            in stack_backup_results["playbook_output"]
        )

    @pytest.mark.aoc_aws_restore_stack  # type: ignore
    def test_restore_stack(self, aoc_aws_restore_stack: AocAwsRestore) -> None:
        """Test verifies a stack can be restored from a provided backup file.

        Test procedure:
            1. Validate registry.redhat.io authentication/pull ops container image
                (Handled when fixture constructs AocAwsRestore class)
            2. Validate required test data for restore playbook is defined
            3. Generate the ops restore playbook extra vars
            4. Run ops container targeting restore playbook w/extra vars
            5. Verify stack is operational/accessible
        Expected results:
            1. Ops container backup playbook finishes successfully
            2. Access to the AoC stack is working as prior to the restore
        """
        assert aoc_aws_restore_stack.validate_command_generator_vars(
            typing.cast(Dict[str, str], aoc_aws_restore_stack.command_generator_vars)
        )
        stack_restore_results: AocAwsRestoreStackResult = (
            aoc_aws_restore_stack.restore_stack()
        )
        assert stack_restore_results["playbook_result"]
        # TODO: Determine post checks to verify restore
