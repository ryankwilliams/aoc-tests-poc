"""AoC aws conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os

from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser) -> None:
    """Handles setting up options that are applicable to aoc aws."""
    parser.addoption(
        "--aoc-aws-credentials-path",
        action="store",
        default=os.getenv("AOC_AWS_CREDENTIALS_PATH", ""),
        help="Path to aws credentials file",
    )

    parser.addoption(
        "--aoc-aws-region",
        action="store",
        default=os.getenv("AOC_AWS_REGION", ""),
        help="AWS region",
    )
