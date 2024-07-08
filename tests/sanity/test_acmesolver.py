import subprocess
import os


def test_sanity_acmesolver():
    image = os.getenv("ROCK_CERT-MANAGER-ACMESOLVER")
    assert image is not None, "ROCK_CERT-MANAGER-ACMESOLVER is not set"
    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "/acmesolver-linux", image, "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert "HTTP server used to solve ACME challenges." in docker_run.stdout
