
from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import async_session
from app.models import Product

async def run_query_examples(session: AsyncSession) -> None:
    def print_results(results: Sequence[Product]) -> None:
        print("Results:")
        for product in results:
            print(f"\t{product}")
        print()
    
    # 1. Basic SELECT
    # -- SELECT * FROM products;
    stmt = select(Product)
    print(stmt)
    

    result = await session.execute(stmt)
    products: Sequence[Product] = result.scalars().all()
    print_results(products)

    stmt = select(Product).where(Product.unit_price > 20)
    result = await session.execute(stmt)
    print_results(result.scalars().all())
    

async def main_async() -> None:
    async with async_session() as session, session.begin():
        await run_query_examples(session)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())
