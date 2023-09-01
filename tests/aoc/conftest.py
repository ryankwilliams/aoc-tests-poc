"""AoC conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os

from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser) -> None:
    """Handles setting up options that are applicable to all tests."""
    parser.addoption(
        "--aoc-version",
        action="store",
        default=os.getenv("AOC_VERSION", "2.4"),
        help="The aoc version for the deployed stack",
    )

    parser.addoption(
        "--aoc-ops-container-image",
        action="store",
        default=os.getenv(
            "AOC_OPS_CONTAINER_IMAGE",
            "registry.redhat.io/ansible-on-clouds/ansible-on-clouds-ops-rhel9",
        ),
        help="The aoc operational container image",
    )

    parser.addoption(
        "--aoc-ops-container-image-tag",
        action="store",
        default=os.getenv(
            "AOC_OPS_CONTAINER_IMAGE_TAG",
            "2.4.20230630",
        ),
        help="The aoc operational container image tag",
    )

    parser.addoption(
        "--aoc-ops-container-image-registry-username",
        action="store",
        default=os.getenv(
            "AOC_OPS_CONTAINER_IMAGE_REGISTRY_USERNAME",
            "",
        ),
        help="The username to authenticate with ops image registry",
    )

    parser.addoption(
        "--aoc-ops-container-image-registry-password",
        action="store",
        default=os.getenv(
            "AOC_OPS_CONTAINER_IMAGE_REGISTRY_PASSWORD",
            "",
        ),
        help="The password to authenticate with ops image registry",
    )

    parser.addoption(
        "--aoc-stack-deployment-name",
        action="store",
        default=os.getenv("AOC_STACK_DEPLOYMENT_NAME", ""),
        help="AoC stack deployment name",
    )
