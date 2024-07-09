#
# Copyright 2024 Canonical, Ltd.
#
import logging
from pathlib import Path
import os

from test_util import harness, util
from test_util.config import MANIFESTS_DIR

LOG = logging.getLogger(__name__)


def test_integration_certmanager(session_instance: harness.Instance):
    images = [
        {"variable": "ROCK_CERT_MANAGER_CONTROLLER", "prefix": None},
        {"variable": "ROCK_CERT_MANAGER_WEBHOOK", "prefix": "webhook"},
        {"variable": "ROCK_CERT_MANAGER_CAINJECTOR", "prefix": "cainjector"},
        {"variable": "ROCK_CERT_MANAGER_ACMESOLVER", "prefix": "acmesolver"},
    ]

    helm_command = [
        "k8s",
        "helm",
        "install",
        "cert-manager",
        "--repo",
        "https://charts.jetstack.io",
        "cert-manager",
        "--namespace",
        "cert-manager",
        "--create-namespace",
        "--version",
        "v1.12.2",
        "--set",
        "installCRDs=true",
    ]

    for image in images:
        image_uri = os.getenv(image["variable"])
        assert image_uri is not None, f"{image['variable']} is not set"
        image_split = image_uri.split(":")

        if image["prefix"]:
            helm_command += [
                "--set",
                f"{image['prefix']}.image.repository={image_split[0]}",
                "--set",
                f"{image['prefix']}.image.tag={image_split[1]}",
                "--set",
                f"{image['prefix']}.securityContext.runAsUser=584792",
            ]
        else:
            helm_command += [
                "--set",
                f"image.repository={image_split[0]}",
                "--set",
                f"image.tag={image_split[1]}",
                "--set",
                "securityContext.runAsUser=584792",
            ]

    session_instance.exec(helm_command)

    manifest = MANIFESTS_DIR / "cert-manager-test.yaml"
    session_instance.exec(
        ["k8s", "kubectl", "apply", "-f", "-"],
        input=Path(manifest).read_bytes(),
    )

    util.stubbornly(retries=3, delay_s=1).on(session_instance).exec(
        [
            "k8s",
            "kubectl",
            "wait",
            "--for=condition=ready",
            "certificate",
            "selfsigned-cert",
            "--namespace",
            "cert-manager-test",
            "--timeout",
            "180s",
        ]
    )

    util.stubbornly(retries=5, delay_s=10).on(session_instance).until(
        lambda p: "selfsigned-cert-tls" in p.stdout.decode()
    ).exec(
        [
            "k8s",
            "kubectl",
            "get",
            "secret",
            "--namespace",
            "cert-manager-test",
            "-o",
            "json",
        ]
    )
