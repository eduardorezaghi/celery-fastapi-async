import os
from typing import Any, Type

import celery
import pytest
from pytest_celery import (
    CeleryWorkerContainer,
    defaults,
)
from pytest_docker_tools import build, container, fxtr


class SmokeWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self._client

    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> Any:
        return celery.__version__

    @classmethod
    def log_level(cls) -> str:
        return "DEBUG"

    @classmethod
    def worker_name(cls) -> str:
        return "smoke_tests_worker"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery"


worker_image = build(
    path=".",
    dockerfile="Dockerfile.worker",
    tag="celery-worker:example",
    buildargs=SmokeWorkerContainer.buildargs(),
)


# Define container settings
default_worker_container = container(
    image="{worker_image.id}",
    ports=fxtr("default_worker_ports"),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={
        # Volume: Worker /app
        "{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME,
        # Mount: app source
        os.path.abspath(os.getcwd()): {
            "bind": "/mycustomapp",
            "mode": "rw",
        },
    },
    wrapper_class=SmokeWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=fxtr("default_worker_command"),
)


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer
