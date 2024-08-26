from fastapi import FastAPI

from app import engine
from app.models import Base, Product
from app.tasks import add_product

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/products/")
async def create_product(name: str, category_id: int, price: float):
    task = add_product.delay(name, category_id, price)
    return {"task_id": task.id}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    async with AsyncSessionLocal() as session:
        product = await session.get(Product, product_id)
        return product