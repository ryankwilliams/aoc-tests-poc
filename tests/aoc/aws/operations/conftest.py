"""AoC aws backup conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os
from typing import TypedDict

import pytest

AOC_AWS_BACKUP_PREFIX_OPTION: str = "aoc-aws-backup"


def pytest_addoption(parser) -> None:
    """Handles setting up options that are applicable to aoc aws."""

    parser.addoption(
        f"--{AOC_AWS_BACKUP_PREFIX_OPTION}-iam-role-arn",
        action="store",
        default=os.getenv(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.upper().replace('-', '_')}_IAM_ROLE_ARN", ""
        ),
        help="ARN that has permissions to perform backup operations",
    )

    parser.addoption(
        f"--{AOC_AWS_BACKUP_PREFIX_OPTION}-vault-name",
        action="store",
        default=os.getenv(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.upper().replace('-', '_')}_VAULT_NAME",
            "Default",
        ),
        help="Name of backup vault holding efs recovery points",
    )

    parser.addoption(
        f"--{AOC_AWS_BACKUP_PREFIX_OPTION}-prefix",
        action="store",
        default=os.getenv(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.upper().replace('-', '_')}_PREFIX",
            "aoc-backup",
        ),
        help="Prefix to add to the backup name",
    )

    parser.addoption(
        f"--{AOC_AWS_BACKUP_PREFIX_OPTION}-s3-bucket",
        action="store",
        default=os.getenv(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.upper().replace('-', '_')}_S3_BUCKET", ""
        ),
        help="S3 bucket name where to store backup files",
    )

    parser.addoption(
        f"--{AOC_AWS_BACKUP_PREFIX_OPTION}-ssm-bucket-name",
        action="store",
        default=os.getenv(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.upper().replace('-', '_')}_SSM_BUCKET_NAME",
            "",
        ),
        help="S3 bucket where temporary config files for aws ssm are stored",
    )


class AocAwsBackupDefaultOptions(TypedDict):
    """AoC aws backup default options typed dict."""

    backup_iam_role_arn: str
    backup_vault_name: str
    backup_prefix: str
    backup_s3_bucket: str
    backup_ssm_bucket_name: str


@pytest.fixture
def aoc_aws_backup_default_options(request) -> AocAwsBackupDefaultOptions:
    """AoC aws backup tests default pytest options fixture.

    A fixture providing default options that can be used by any
    AoC aws backup tests.
    """
    return AocAwsBackupDefaultOptions(
        backup_iam_role_arn=request.config.getoption(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.replace('-', '_')}_iam_role_arn"
        ),
        backup_vault_name=request.config.getoption(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.replace('-', '_')}_vault_name"
        ),
        backup_prefix=request.config.getoption(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.replace('-', '_')}_prefix"
        ),
        backup_s3_bucket=request.config.getoption(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.replace('-', '_')}_s3_bucket"
        ),
        backup_ssm_bucket_name=request.config.getoption(
            f"{AOC_AWS_BACKUP_PREFIX_OPTION.replace('-', '_')}_ssm_bucket_name"
        ),
    )
