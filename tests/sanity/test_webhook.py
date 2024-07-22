#
# Copyright 2024 Canonical, Ltd.
# See LICENSE file for licensing details
#
import pytest
from k8s_test_harness.util import docker_util, env_util

IMG_NAME = "cert-manager-webhook"
IMG_PLATFORM = "amd64"

EXP_HELPSTR = "Webhook component providing API validation"


@pytest.mark.parametrize("version", ("1.10.1", "1.12.2"))
def test_sanity_webhook(version):
    rock = env_util.get_build_meta_info_for_rock_version(
        IMG_NAME, version, IMG_PLATFORM
    )

    docker_run = docker_util.run_in_docker(rock.image, ["/webhook-linux", "--help"])
    assert EXP_HELPSTR in docker_run.stdout
