import celery.utils

from app.celery import celery_app


@celery_app.task(bind=True)  # type: ignore
def add_product(
    self: celery.Task,
    name: str,
    description: str,
    category_id: int,
    price: float,
) -> None:
    # Implement logic to add a product to the database
    ...


@celery_app.task(bind=True)  # type: ignore
def noop(*args: list, **kwargs: dict) -> celery.utils.noop:
    return celery.utils.noop(*args, **kwargs)
