from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from tasks import add_product

app = FastAPI()

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/northwind"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.on_event("startup")
async def startup():
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