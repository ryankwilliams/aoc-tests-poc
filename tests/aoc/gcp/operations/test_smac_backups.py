"""Tests validating AoC on GCP backups."""
import pytest

from lib.aoc.gcp.operations.backup import *
from tests.aoc.conftest import AocDefaultOptions


@pytest.fixture
def aoc_gcp_backup(
    ansible_module: pytest.fixture, aoc_default_options: AocDefaultOptions
) -> AocGcpBackup:
    """Fixture returning aoc gcp backup operations."""
    command_generator_vars: AocGcpBackupAvailableVars = AocGcpBackupDataVars(
        todo="todo"
    )

    if aoc_default_options["stack_version"] == "2.3":
        command_generator_vars = Aoc23GcpBackupDataVars(todo="todo")

    return AocGcpBackup(
        aoc_version=aoc_default_options["stack_version"],
        aoc_ops_image=aoc_default_options["ops_container_image"],
        aoc_ops_image_tag=aoc_default_options["ops_container_image_tag"],
        aoc_image_registry_username=aoc_default_options[
            "ops_container_image_registry_username"
        ],
        aoc_image_registry_password=aoc_default_options[
            "ops_container_image_registry_password"
        ],
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


class TestAoCGcpBackup:
    @pytest.mark.gcp
    @pytest.mark.aoc_gcp_backup
    @pytest.mark.operations
    def test_backup(self, aoc_gcp_backup: AocGcpBackup) -> None:
        assert aoc_gcp_backup.run()
