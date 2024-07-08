import subprocess
import os


def test_sanity_controller():
    image = os.getenv("ROCK_CERT_MANAGER_CONTROLLER")
    assert image is not None, "ROCK_CERT_MANAGER_CONTROLLER is not set"
    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "/controller-linux", image, "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert (
        "cert-manager is a Kubernetes addon to automate the management and issuance"
        in docker_run.stdout
    )
