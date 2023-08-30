"""Containers module.

This module provides a core class 'container engine' that other
classes can import/use. Handles the common operations when working
with containers to reduce duplication.
"""
import typing
from typing import Dict
from typing import List
from typing import Tuple

from pytest_ansible.host_manager import BaseHostManager


class ContainerEngine:
    """ContainerEngine class."""

    def __init__(self, ansible_module: BaseHostManager) -> None:
        """Constructor.

        :param ansible_module: the pytest ansible module fixture
        """
        self.ansible_module: BaseHostManager = ansible_module

    def registry_login(self, registry: str, username: str, password: str) -> bool:
        """Logins to the registry provided using username/password

        :param registry: the registry hostname
        :param username: the registry username to authenticate with
        :param password: the registry password to authenticate with
        """
        result = self.ansible_module.docker_login(
            registry_url=registry,
            username=username,
            password=password,
        )
        if "failed" in result.contacted["localhost"]:
            print(result.contacted["localhost"]["msg"])
            return False
        return True

    def pull_image(self, image: str, tag: str) -> bool:
        """Pull the image/tag provided.

        :param image: the container image fqdn
        :param tag: the container image tag
        """
        result = self.ansible_module.docker_image(name=image, tag=tag, source="pull")
        if "failed" in result.contacted["localhost"]:
            print(result.contacted["localhost"]["msg"])
            return False
        return True

    def run(
        self,
        name: str,
        image: str,
        command: str,
        volumes: List[str],
        env_vars: Dict[str, str],
    ) -> Tuple[str, bool]:
        """Run the container and its provided options.

        :param image: the image (w/tag) to start the container from
        :param command: the command to run within the container
        :param volumes: the volumes to mount into the container
        :param env_vars: the environment variables to set into the container
        """
        result = self.ansible_module.docker_container(
            name=name,
            image=image,
            command=command,
            detach="false",
            state="started",
            volumes=volumes,
            env=env_vars,
        )

        playbook_output: str = result.contacted["localhost"]["container"]["Output"]
        print(playbook_output)

        self.ansible_module.docker_container(name=name, state="absent")

        return (
            playbook_output,
            typing.cast(int, result.contacted["localhost"]["status"]) == 0,
        )
