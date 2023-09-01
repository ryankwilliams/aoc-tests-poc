"""AoC aws backup conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os

from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser) -> None:
    """Handles setting up options that are applicable to aoc aws."""

    parser.addoption(
        "--aoc-aws-backup-iam-role-arn",
        action="store",
        default=os.getenv("AOC_AWS_BACKUP_IAM_ROLE_ARN", ""),
        help="ARN that has permissions to perform backup operations",
    )

    parser.addoption(
        "--aoc-aws-backup-vault-name",
        action="store",
        default=os.getenv("AOC_AWS_BACKUP_VAULT_NAME", "Default"),
        help="Name of backup vault holding efs recovery points",
    )

    parser.addoption(
        "--aoc-aws-backup-prefix",
        action="store",
        default=os.getenv("AOC_AWS_BACKUP_PREFIX", "aoc-backup"),
        help="Prefix to add to the backup name",
    )

    for option in [
        {
            "name": "--aoc-aws-backup-s3-bucket",
            "default": os.getenv("AOC_AWS_BACKUP_S3_BUCKET", ""),
            "help": "S3 bucket name where to store backup files",
        },
        {
            "name": "--aoc-aws-restore-s3-bucket",
            "default": os.getenv("AOC_AWS_RESTORE_S3_BUCKET", ""),
            "help": "S3 bucket name where backup files are stored",
        },
    ]:
        parser.addoption(
            option["name"],
            action="store",
            default=option["default"],
            help=option["help"],
        )

    for option in [
        {
            "name": "--aoc-aws-backup-ssm-bucket-name",
            "default": os.getenv("AOC_AWS_BACKUP_SSM_BUCKET_NAME", ""),
            "help": "S3 bucket where temporary config files for aws ssm are stored",
        },
        {
            "name": "--aoc-aws-restore-ssm-bucket-name",
            "default": os.getenv("AOC_AWS_RESTORE_SSM_BUCKET_NAME", ""),
            "help": "S3 bucket where temporary config files for aws ssm are stored",
        },
    ]:
        parser.addoption(
            option["name"],
            action="store",
            default=option["default"],
            help=option["help"],
        )

    parser.addoption(
        "--aoc-aws-restore-backup-name",
        action="store",
        default=os.getenv("AOC_AWS_RESTORE_BACKUP_NAME", ""),
        help="The backup folder name stored in S3 bucket",
    )
