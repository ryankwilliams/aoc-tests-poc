"""Operations module.

This package contains additional packages/modules "libraries" that
handle Ansible On Clouds operations using the ops container image.
"""
import typing
from typing import Dict
from typing import List
from typing import Tuple

from pytest_ansible.host_manager import BaseHostManager


class OpsContainerImageMixin:
    """OpsContainerImageMixin Class."""

    @staticmethod
    def validate_command_generator_vars(command_vars: Dict[str, str]) -> bool:
        """Validate the command generate data vars for backup operations.

        :return: true = passed, false = failed
        """
        result: bool = True

        for key, value in command_vars.items():
            if key == "extra_vars":
                for extra_var_key, extra_var_value in value.items():  # type: ignore
                    if extra_var_value == "":
                        print(
                            f"Command generator var: {extra_var_key} is unset and needs to be set."
                        )
                        result = False
                continue
            if value == "":
                print(f"Command generator var: {key} is unset and needs to be set.")
                result = False

        return result


class OpsContainer(OpsContainerImageMixin):
    """OpsContainer Class."""

    def __init__(
        self,
        cloud: str,
        aoc_version: str,
        aoc_ops_image: str,
        aoc_ops_image_tag: str,
        aoc_image_registry_username: str,
        aoc_image_registry_password: str,
        ansible_module: BaseHostManager,
    ) -> None:
        """Constructor.

        :param cloud: the cloud provider AAP is deployed into
        :param aoc_version: the aoc version deployed
        :param aoc_ops_image: the aoc operations container image
        :param aoc_ops_image_tag: the aoc operations container image tag
        :param aoc_image_registry_username: the username to authenticate with
            the image registry holding aoc operations image
        :param aoc_image_registry_password: the password to authenticate with
            the image registry holding aoc operations image
        :param ansible_module: the pytest ansible module fixture
        """
        self.cloud: str = cloud
        self.aoc_version: str = aoc_version
        self.aoc_ops_image: str = aoc_ops_image
        self.aoc_ops_image_tag: str = aoc_ops_image_tag
        self.aoc_image_registry_username: str = aoc_image_registry_username
        self.aoc_image_registry_password: str = aoc_image_registry_password
        self.ansible_module: BaseHostManager = ansible_module

        if not self.__validate():
            raise SystemExit(1)

        self._command: str = ""
        self.command_args: List[str] = []
        self.env_vars: Dict[str, str] = {}
        self.volume_mounts: List[str] = []

        # Authenticate with ops container image registry
        if not self.registry_login(
            self.aoc_ops_image.split("/")[0],
            self.aoc_image_registry_username,
            self.aoc_image_registry_password,
        ):
            raise SystemExit(1)

        # Pull ops container image
        if not self.pull_image(self.aoc_ops_image, self.aoc_ops_image_tag):
            raise SystemExit(1)

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

    @property
    def command(self) -> str:
        """Returns the container command string to run within the command generator vars container."""
        return self._command

    @command.setter
    def command(self, value: str) -> None:
        """Sets the command string value for the command generator vars container."""
        self._command = f"{value} -e '{' '.join(self.command_args)}'"

    def __validate(self) -> bool:
        """Validates any necessary input prior to performing backups.

        :return: the overall result of the validations performed
        """
        result: bool = True

        validation_matrix: Dict[str, str] = {
            "AoC operations image": self.aoc_ops_image,
            "AoC operations image tag": self.aoc_ops_image_tag,
            "AoC operations image registry username": self.aoc_image_registry_username,
            "AoC operations image registry password": self.aoc_image_registry_password,
        }

        for key, value in validation_matrix.items():
            if value == "":
                print(f"{key} is not set. Please verify it was set and try again.\n")
                result = False

        return result

    def run(self) -> bool:
        """Maintain backwards compatibility with existing tests invoking run()."""
        # TODO: Deprecate this, each operation class should implement run()
        output: str
        result: bool
        output, result = self.run_container("container")
        return result

    def run_container(self, name: str) -> Tuple[str, bool]:
        """Runs the ops container with necessary input."""
        result = self.ansible_module.docker_container(
            name=name,
            image=f"{self.aoc_ops_image}:{self.aoc_ops_image_tag}",
            command=self.command,
            detach="false",
            state="started",
            volumes=self.volume_mounts,
            env=self.env_vars,
        )

        playbook_output: str = result.contacted["localhost"]["container"]["Output"]
        print(playbook_output)

        self.ansible_module.docker_container(name=name, state="absent")

        return (
            playbook_output,
            typing.cast(int, result.contacted["localhost"]["status"]) == 0,
        )
