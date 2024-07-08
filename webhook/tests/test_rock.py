import subprocess

from charmed_kubeflow_chisme.rock import CheckRock

def test_rock_smoke():
    check_rock = CheckRock("rockcraft.yaml")
    rock_version = check_rock.get_version()
    rock_full_name = str(check_rock.get_name())
    rock_name = rock_full_name.split("-")[-1]
    local_rock_image = f"{rock_full_name}:{rock_version}"
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
    assert "Webhook component providing API validation" in docker_run.stdout
