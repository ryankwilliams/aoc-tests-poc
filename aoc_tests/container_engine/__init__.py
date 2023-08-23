"""Container engine package.

This package contains additional packages/modules "libraries" that work
directly with a container runtime engine (e.g. docker, podman).
"""
import docker


class ContainerEngine:
    """ContainerEngine Class."""

    def __init__(self) -> None:
        """Constructor."""
        # TODO: Revise this for other users/container runtime engines
        self.client: docker.DockerClient = docker.DockerClient(
            base_url="unix:///run/user/1000/podman/podman.sock"
        )

    def registry_login(self, registry: str, username: str, password: str) -> None:
        """Logins to the registry provided using username/password

        :param registry: the registry hostname
        :param username: the registry username to authenticate with
        :param password: the registry password to authenticate with
        """
        self.client.login(registry=registry, username=username, password=password)

    def pull_image(self, image: str, tag: str) -> None:
        """Pull the image/tag provided.

        :param image: the container image fqdn
        :param tag: the container image tag
        """
        self.client.images.pull(repository=image, tag=tag)
