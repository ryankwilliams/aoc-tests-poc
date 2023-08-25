"""Defaults module.

This module contains common variables that can be used by various test modules.
"""
import os

__all__ = [
    "aoc_ops_image",
    "aoc_ops_image_tag",
    "aoc_image_registry_username",
    "aoc_image_registry_password",
    "aoc_version",
]


aoc_ops_image: str = os.getenv(
    "AOC_OPS_IMAGE",
    "registry.redhat.io/ansible-on-clouds/ansible-on-clouds-ops-rhel9",
)
aoc_ops_image_tag: str = os.getenv("AOC_OPS_IMAGE_TAG", "2.4.20230630")
aoc_image_registry_username: str = os.getenv("AOC_OPS_IMAGE_REGISTRY_USERNAME", "")
aoc_image_registry_password: str = os.getenv("AOC_OPS_IMAGE_REGISTRY_PASSWORD", "")
aoc_version: str = os.getenv("AOC_VERSION", "2.4")
