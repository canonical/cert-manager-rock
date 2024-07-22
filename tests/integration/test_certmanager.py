#
# Copyright 2024 Canonical, Ltd.
# See LICENSE file for licensing details
#

from pathlib import Path

import pytest
from k8s_test_harness import harness
from k8s_test_harness.util import constants, env_util, exec_util, k8s_util
from k8s_test_harness.util.k8s_util import HelmImage

IMG_PLATFORM = "amd64"
INSTALL_NAME = "cert-manager"

DIR = Path(__file__).absolute().parent
MANIFESTS_DIR = DIR / ".." / "templates"


def _get_rock_image(name: str, version: str):
    rock = env_util.get_build_meta_info_for_rock_version(
        f"cert-manager-{name}", version, IMG_PLATFORM
    )
    return rock.image


@pytest.mark.parametrize("version", ("1.10.1", "1.12.2"))
def test_certmanager(function_instance: harness.Instance, version: str):
    images = [
        HelmImage(uri=_get_rock_image("controller", version)),
        HelmImage(uri=_get_rock_image("webhook", version), prefix="webhook"),
        HelmImage(uri=_get_rock_image("cainjector", version), prefix="cainjector"),
        HelmImage(uri=_get_rock_image("acmesolver", version), prefix="acmesolver"),
    ]

    helm_command = k8s_util.get_helm_install_command(
        name=INSTALL_NAME,
        chart_name="cert-manager",
        images=images,
        namespace=constants.K8S_NS_KUBE_SYSTEM,
        chart_version=version,
        repository="https://charts.jetstack.io",
    )
    helm_command += ["--set", "installCRDs=true"]
    function_instance.exec(helm_command)

    manifest = MANIFESTS_DIR / "cert-manager-test.yaml"
    function_instance.exec(
        ["k8s", "kubectl", "apply", "-f", "-"],
        input=Path(manifest).read_bytes(),
    )

    k8s_util.wait_for_resource(
        function_instance,
        resource_type="certificate",
        name="selfsigned-cert",
        namespace="cert-manager-test",
        condition=constants.K8S_CONDITION_READY,
    )

    exec_util.stubbornly(retries=5, delay_s=10).on(function_instance).until(
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
