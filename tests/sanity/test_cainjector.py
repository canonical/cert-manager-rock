import subprocess
import os


def test_sanity_cainjector():
    image = os.getenv("ROCK_CERT-MANAGER-CAINJECTOR")
    assert image is not None, "ROCK_CERT-MANAGER-CAINJECTOR is not set"
    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "/cainjector-linux", image, "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert (
        "cert-manager CA injector is a Kubernetes addon to automate the injection of CA data into"
        in docker_run.stdout
    )
