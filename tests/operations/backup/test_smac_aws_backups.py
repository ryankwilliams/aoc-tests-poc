"""Tests validating AoC on AWS backups."""
import os

import pytest

from tests.lib.operations.backup.aws import *

aoc_ops_image: str = os.getenv(
    "AOC_OPS_IMAGE",
    "registry.redhat.io/ansible-on-clouds/ansible-on-clouds-ops-rhel9",
)
aoc_ops_image_tag: str = os.getenv("AOC_OPS_IMAGE_TAG", "2.4.20230630")
aoc_image_registry_username: str = os.getenv("AOC_OPS_IMAGE_REGISTRY_USERNAME", "")
aoc_image_registry_password: str = os.getenv("AOC_OPS_IMAGE_REGISTRY_PASSWORD", "")
aoc_version: str = os.getenv("AOC_VERSION", "2.4")


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
