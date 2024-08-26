from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    description = Column(String)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    unit_price = Column(Float)

    category = relationship("Category", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product(product_name={self.product_name}, unit_price={self.unit_price})>"

Category.products = relationship("Product", back_populates="category")