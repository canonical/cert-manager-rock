import random
import pytest
import string
import subprocess

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

def test_rock(rock_test_env):
    """Test rock."""
    temp_dir, container_name = rock_test_env
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"
    # assert we have the expected files
    docker_run = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/acmesolver-linux",
            LOCAL_ROCK_IMAGE,
            "-h"
        ],
        capture_output=True,
    )
    assert "HTTP server used to solve ACME challenges." in docker_run.stdout.decode("utf-8")
    