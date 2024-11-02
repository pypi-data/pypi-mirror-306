import docker


class UsernetesRunner:
    """
    A Usernetes Runner will run usernetes via docker compose.

    We do this easily by using the docker python sdk.
    """

    def __init__(self, compose_file=None):
        """
        Create a new transformer backend, accepting any options type.

        Validation of transformers is done by the registry
        """
        self.client = docker.from_env()
        self.compose_file = compose_file or "docker-compose.yaml"

    def up(self):
        """
        Run docker-compose up, always with detached.
        """
        self.client.compose.up(file=self.compose_file, detach=True)

    # Optionally, you can access the logs of the containers
    # for container in client.compose.containers():
    #    print(container.logs())

    def down(self):
        """
        Run docker-compose down.

        This stops and removes containers.
        """
        self.client.compose.down(file=self.compose_file)
