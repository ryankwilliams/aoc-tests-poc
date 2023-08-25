"""Tests validating AoC on AWS backups."""
import pytest

from lib.aoc.aws.operations.backup import *
from tests.aoc.defaults import *


@pytest.fixture
def aoc_aws_backup(ansible_module: pytest.fixture) -> AocAwsBackup:
    """Fixture returning aoc aws backup operations."""
    command_generator_vars: AocAwsBackupAvailableVars = AocAwsBackupDataVars(
        cloud_credentials_path="todo"
    )

    if aoc_version == "2.3":
        command_generator_vars = Aoc23AwsBackupDataVars(cloud_credentials_path="todo")

    return AocAwsBackup(
        aoc_version=aoc_version,
        aoc_ops_image=aoc_ops_image,
        aoc_ops_image_tag=aoc_ops_image_tag,
        aoc_image_registry_username=aoc_image_registry_username,
        aoc_image_registry_password=aoc_image_registry_password,
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


class TestAoCAwsBackup:
    @pytest.mark.aws
    @pytest.mark.aoc_aws_backup
    @pytest.mark.operations
    def test_backup(self, aoc_aws_backup: AocAwsBackup) -> None:
        assert aoc_aws_backup.run()
