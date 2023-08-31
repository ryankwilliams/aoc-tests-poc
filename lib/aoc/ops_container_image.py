"""Operations module.

This package contains additional packages/modules "libraries" that
handle Ansible On Clouds operations using the ops container image.
"""
from typing import Dict
from typing import List

from pytest_ansible.host_manager import BaseHostManager

from lib.containers import ContainerEngine


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


class OpsContainerImage(OpsContainerImageMixin):
    """OpsContainerImage Class."""

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

        if not self.__validate():
            raise SystemExit(1)

        self.container_engine = ContainerEngine(ansible_module)

        self._container_command: str = ""
        self._container_command_args: List[str] = []
        self._container_env_vars: Dict[str, str] = {}
        self._container_volume_mount: List[str] = []

        if not self.setup():
            raise SystemExit(1)

    @property
    def container_command(self) -> str:
        """Returns the container command string to run within the command generator vars container."""
        return self._container_command

    @container_command.setter
    def container_command(self, value: str) -> None:
        """Sets the command string value for the command generator vars container."""
        self._container_command = (
            f"{value} -e '{' '.join(self.container_command_args)}'"
        )

    @property
    def container_command_args(self) -> List[str]:
        """Returns the container command arguments."""
        return self._container_command_args

    @container_command_args.setter
    def container_command_args(self, value: List[str]) -> None:
        """Sets the container command arguments."""
        self._container_command_args = value

    @property
    def container_env_vars(self) -> Dict[str, str]:
        """Returns the container's environment variables to be set."""
        return self._container_env_vars

    @container_env_vars.setter
    def container_env_vars(self, value: Dict[str, str]) -> None:
        """Sets the container's environment variables to be set."""
        self._container_env_vars = value

    @property
    def container_volume_mount(self) -> List[str]:
        """Returns the container's volume mounts."""
        return self._container_volume_mount

    @container_volume_mount.setter
    def container_volume_mount(self, value: List[str]) -> None:
        """Sets the container's volume mounts."""
        self._container_volume_mount = value

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

    def setup(self) -> bool:
        """Performs setup operations to perform aoc backups."""
        login_result: bool = self.container_engine.registry_login(
            self.aoc_ops_image.split("/")[0],
            self.aoc_image_registry_username,
            self.aoc_image_registry_password,
        )
        pull_image_result: bool = self.container_engine.pull_image(
            self.aoc_ops_image, self.aoc_ops_image_tag
        )
        return login_result and pull_image_result

    def run(self) -> bool:
        """Initiates/performs backup operation."""
        return self.container_engine.run(
            image=f"{self.aoc_ops_image}:{self.aoc_ops_image_tag}",
            command=self.container_command,
            volumes=self.container_volume_mount,
            env_vars=self.container_env_vars,
        )
