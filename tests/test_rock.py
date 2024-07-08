import random
import pytest
import string
import subprocess
import os

from parameterized import parameterized
from charmed_kubeflow_chisme.rock import CheckRock


@pytest.fixture()
def rock_test_env(tmpdir):
    """Yields a temporary directory and random docker container name, then cleans them up after."""
    container_name = "".join(
        [str(i) for i in random.choices(string.ascii_lowercase, k=8)]
    )
    yield tmpdir, container_name

    try:
        subprocess.run(["docker", "rm", container_name])
    except Exception:
        pass
    # tmpdir fixture we use here should clean up the other files for us


@parameterized.expand([
    ("acmesolver", "HTTP server used to solve ACME challenges."),
    ("webhook", "Webhook component providing API validation"),
    ("controller", "cert-manager is a Kubernetes addon to automate the management and issuance"),
    ("cainjector", "cert-manager CA injector is a Kubernetes addon to automate the injection of CA data into"),
])
def test_rock_smoke(rock_name, expected_stout_substring):
    check_rock = CheckRock(os.path.join(rock_name, "rockcraft.yaml"))
    # rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    local_rock_image = f"cert-manager-{rock_name}:{rock_version}"
    # assert we have the expected files
    docker_run = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            f"/{rock_name}-linux",
            local_rock_image,
            "--help"
        ],
        capture_output=True,
        check=True,
        text=True
    )
    assert expected_stout_substring in docker_run.stdout
