"""Tests validating AoC on AWS restores."""
import os

import pytest

from tests.lib.operations.restore.aws import *
from tests.operations.defaults import *


@pytest.fixture
def aoc_aws_restore(ansible_module: pytest.fixture) -> AocAwsRestore:
    """Fixture returning aoc aws restore operations."""
    command_generator_vars: AocAwsRestoreAvailableVars = AocAwsRestoreDataVars(
        cloud_credentials_path="todo"
    )

    if aoc_version == "2.3":
        command_generator_vars = Aoc23AwsRestoreDataVars(cloud_credentials_path="todo")

    return AocAwsRestore(
        aoc_version=aoc_version,
        aoc_ops_image=aoc_ops_image,
        aoc_ops_image_tag=aoc_ops_image_tag,
        aoc_image_registry_username=aoc_image_registry_username,
        aoc_image_registry_password=aoc_image_registry_password,
        ansible_module=ansible_module,
        command_generator_vars=command_generator_vars,
    )


class TestAoCAwsRestore:
    @pytest.mark.aws
    @pytest.mark.aoc_aws_restore
    @pytest.mark.operations
    def test_restore(self, aoc_aws_restore: AocAwsRestore) -> None:
        assert aoc_aws_restore.run()
