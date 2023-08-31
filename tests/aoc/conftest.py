"""AoC conftest module.

This module contains commonly used code across all test modules.
Majority of the functions here will be pytest fixtures.
"""
import os
from typing import TypedDict

import pytest
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


class AocDefaultOptions(TypedDict):
    """AoC default options typed dict."""

    ops_container_image: str
    ops_container_image_tag: str
    ops_container_image_registry_username: str
    ops_container_image_registry_password: str
    stack_deployment_name: str
    stack_version: str


@pytest.fixture  # type: ignore
def aoc_default_options(request) -> AocDefaultOptions:
    """AoC tests default pytest options fixture.

    A fixture providing default options that can be used by
    any AoC tests.
    """
    return AocDefaultOptions(
        ops_container_image=request.config.getoption("aoc_ops_container_image"),
        ops_container_image_tag=request.config.getoption("aoc_ops_container_image_tag"),
        ops_container_image_registry_username=request.config.getoption(
            "aoc_ops_container_image_registry_username"
        ),
        ops_container_image_registry_password=request.config.getoption(
            "aoc_ops_container_image_registry_password"
        ),
        stack_deployment_name=request.config.getoption("aoc_stack_deployment_name"),
        stack_version=request.config.getoption("aoc_version"),
    )
