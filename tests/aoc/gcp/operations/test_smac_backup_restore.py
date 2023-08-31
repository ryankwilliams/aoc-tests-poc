"""Tests validating AoC on GCP backup/restore."""
import pytest
from pytest_ansible.host_manager import BaseHostManager

from lib.aoc.gcp.operations.backup import AocGcpBackup
from lib.aoc.gcp.operations.backup import AocGcpBackupDataVars
from lib.aoc.gcp.operations.restore import AocGcpRestore
from lib.aoc.gcp.operations.restore import AocGcpRestoreDataVars
from tests.aoc.conftest import AocDefaultOptions


@pytest.fixture  # type: ignore
def aoc_gcp_backup(
    ansible_module: BaseHostManager, aoc_default_options: AocDefaultOptions
) -> AocGcpBackup:
    """Fixture returning aoc gcp backup operations."""
    command_generator_vars: AocGcpBackupDataVars = AocGcpBackupDataVars(todo="todo")

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


@pytest.fixture  # type: ignore
def aoc_gcp_restore(
    ansible_module: pytest.fixture, aoc_default_options: AocDefaultOptions
) -> AocGcpRestore:
    """Fixture returning aoc gcp restore operations."""
    command_generator_vars: AocGcpRestoreDataVars = AocGcpRestoreDataVars(todo="todo")

    return AocGcpRestore(
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


@pytest.mark.gcp
@pytest.mark.operations
@pytest.mark.aoc_gcp_backup_restore
class TestAoCGcpBackupRestore:
    @pytest.mark.aoc_gcp_backup  # type: ignore
    def test_backup(self, aoc_gcp_backup: AocGcpBackup) -> None:
        assert aoc_gcp_backup.validate()
        assert aoc_gcp_backup.run()

    @pytest.mark.aoc_gcp_restore  # type: ignore
    def test_restore(self, aoc_gcp_restore: AocGcpRestore) -> None:
        assert aoc_gcp_restore.validate()
        assert aoc_gcp_restore.run()
