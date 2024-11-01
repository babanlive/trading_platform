from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    category: Mapped['Category'] = relationship('Category', back_populates='products')
