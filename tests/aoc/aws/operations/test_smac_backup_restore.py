"""Tests validating AoC on AWS backup/restore."""
import typing
from typing import Dict
from typing import Iterator
from typing import List

import pytest
from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.aws.operations.backup import AocAwsBackup
from lib.aoc.aws.operations.backup import AocAwsBackupDataExtraVars
from lib.aoc.aws.operations.backup import AocAwsBackupDataVars
from lib.aoc.aws.operations.restore import AocAwsRestore
from lib.aoc.aws.operations.restore import AocAwsRestoreDataExtraVars
from lib.aoc.aws.operations.restore import AocAwsRestoreDataVars


@pytest.fixture  # type: ignore
def aoc_aws_backup_stack(
    ansible_module: BaseHostManager,
    pytestconfig: pytest.Config,
) -> Iterator[AocAwsBackup]:
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

    aoc_aws_backup = AocAwsBackup(
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
    yield aoc_aws_backup

    # Delete backup and s3 bucket
    if pytestconfig.cache.get("delete_stack_backup", True):
        aoc_aws_backup.delete_stack_backup(
            [pytestconfig.cache.get("stack_backup_object_name", "")]
        )
        aoc_aws_backup.delete_s3_bucket()


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

    @pytest.mark.aoc_aws_backup_stack  # type: ignore
    def test_backup_stack(
        self, aoc_aws_backup_stack: AocAwsBackup, pytestconfig: pytest.Config
    ) -> None:
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
        pytestconfig.cache.set(
            "delete_stack_backup", pytestconfig.getoption("aoc_aws_skip_delete_backup")
        )

        assert aoc_aws_backup_stack.validate_command_generator_vars(
            typing.cast(Dict[str, str], aoc_aws_backup_stack.command_generator_vars)
        ), "one or more stack backup vars are undefined"
        assert aoc_aws_backup_stack.create_s3_bucket(), "failed to create S3 bucket"

        stack_backup_results = aoc_aws_backup_stack.backup_stack()
        assert stack_backup_results["playbook_result"], "backup stack playbook failed"
        assert (
            stack_backup_results["backup_object_name"]
            in stack_backup_results["playbook_output"]
        ), "stack backup name does not exist in playbook output"

        pytestconfig.cache.set(
            "stack_backup_object_name", stack_backup_results["backup_object_name"]
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
        ), "one or more stack restore vars are undefined"
        stack_restore_results = aoc_aws_restore_stack.restore_stack()
        assert stack_restore_results["playbook_result"], "restore stack playbook failed"

        # TODO: Determine post checks to verify restore


@pytest.mark.aoc_aws_delete_backups  # type: ignore
def test_delete_backups(
    aoc_aws_backup_stack: AocAwsBackup, pytestconfig: pytest.Config
) -> None:
    """Test verifies a stack backup can be deleted and removed within aws account.

    Test procedure:
        1. Validate registry.redhat.io authentication/pull ops container image
            (Handled when fixture constructs AocAwsRestore class)
        2. Validate required test data for restore playbook is defined
        3. Generate the ops delete backup playbook extra vars
        4. Run ops container targeting delete backup playbook w/extra vars
        5. Verify backups were deleted
    Expected results:
        1. Ops container backup playbook finishes successfully
        2. Backup files no longer exist in S3 bucket
    """
    # Skip having the fixture attempt to delete backups as this test is focused
    # around deleting backups
    pytestconfig.cache.set("delete_stack_backup", False)

    backup_names: List[str] = pytestconfig.getoption("aoc_aws_delete_backup_name")
    assert (
        len(backup_names) != 0
    ), f"no stack backup names provided, received: {backup_names}"

    # TODO: Validate input (e.g. aws region, etc)

    stack_delete_backup_result = aoc_aws_backup_stack.delete_stack_backup(backup_names)
    assert stack_delete_backup_result[
        "playbook_result"
    ], "delete stack backups playbook failed"

    # TODO: Verify objects no longer exists in bucket

    # TODO: Delete the S3 bucket?
