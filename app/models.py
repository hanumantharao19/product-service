from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500)
    )

    price = Column(
        Float,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    is_active = Column(
        Boolean,
        default=True
    )