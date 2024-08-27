import pytest
from pytest_celery import (
    CeleryBrokerCluster,
    CeleryTestSetup,
    RabbitMQTestBroker,
    RedisTestBroker,
)

from app.tasks import noop


@pytest.fixture
def celery_broker_cluster(
    celery_rabbitmq_broker: RabbitMQTestBroker,
) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster(
    celery_redis_broker: RedisTestBroker,
) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_redis_broker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    from app import tasks
    default_worker_tasks.add(tasks)
    return default_worker_tasks


def test_hello_world(celery_setup: CeleryTestSetup) -> None:
    assert isinstance(celery_setup.broker, RabbitMQTestBroker)
    assert isinstance(celery_setup.backend, RedisTestBroker)
    
    # Test the `noop` task
    result = noop.s().apply()
    
    assert result.get() is None

