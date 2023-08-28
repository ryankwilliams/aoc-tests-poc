"""AoC aws conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os
from typing import TypedDict

import pytest


def pytest_addoption(parser) -> None:
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


class AocAwsDefaultOptions(TypedDict):
    """Aoc aws default options typed dict."""

    credentials_path: str
    region: str


@pytest.fixture
def aoc_aws_default_options(request) -> AocAwsDefaultOptions:
    """AoC aws tests default pytest options fixture.

    A fixture providing default options that can be used by any
    AoC aws tests.
    """
    return AocAwsDefaultOptions(
        credentials_path=request.config.getoption("aoc_aws_credentials_path"),
        region=request.config.getoption("aoc_aws_region"),
    )
