import os

import pytest

# TODO: Handle return codes from ansible module calls


class ContainerEngine:
    """ContainerEngine class."""

    def __init__(self, ansible_module: pytest.fixture) -> None:
        """Constructor.

        :param ansible_module: the pytest ansible module fixture
        """
        self.ansible_module: pytest.fixture = ansible_module

        # TODO: Revise this for other users/container runtime engines
        os.environ["DOCKER_HOST"] = "unix:///run/user/1000/podman/podman.sock"

    def registry_login(self, registry: str, username: str, password: str) -> None:
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
        print(result)

    def pull_image(self, image: str, tag: str) -> None:
        """Pull the image/tag provided.

        :param image: the container image fqdn
        :param tag: the container image tag
        """
        result = self.ansible_module.podman_image(
            name=image,
            tag=tag,
        )
        print(result)

    def run(self, image: str, command: str) -> None:
        """Run the container and its provided options.

        :param image: the image (w/tag) to start the container from
        :param command: the command to run within the container
        """
        result = self.ansible_module.docker_container(
            name="container",
            image=image,
            command=command,
            detach="false",
        )
        print(result.contacted["localhost"]["container"]["Output"])
