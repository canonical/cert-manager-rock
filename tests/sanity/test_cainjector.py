#
# Copyright 2024 Canonical, Ltd.
# See LICENSE file for licensing details
#

import pytest
from k8s_test_harness.util import docker_util, env_util

IMG_NAME = "cert-manager-cainjector"
IMG_PLATFORM = "amd64"

EXP_HELPSTR = "cert-manager CA injector is a Kubernetes addon to automate the injection of CA data into"


@pytest.mark.parametrize("version", ("1.10.1", "1.12.2"))
def test_sanity_cainjector(version):
    rock = env_util.get_build_meta_info_for_rock_version(
        IMG_NAME, version, IMG_PLATFORM
    )

    docker_run = docker_util.run_in_docker(rock.image, ["/cainjector-linux", "--help"])
    assert EXP_HELPSTR in docker_run.stdout
