import subprocess
import os


def test_sanity_webhook():
    image = os.getenv("ROCK_CERT-MANAGER-WEBHOOK")
    assert image is not None, "ROCK_CERT-MANAGER-WEBHOOK is not set"
    docker_run = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "/webhook-linux", image, "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert "Webhook component providing API validation" in docker_run.stdout
