from pydantic import BaseModel, Field


class ProductCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = None

    price: float = Field(
        gt=0
    )

    category: str

    stock: int = Field(
        ge=0
    )


class ProductResponse(BaseModel):

    id: int
    name: str
    description: str | None
    price: float
    category: str
    stock: int
    is_active: bool

    class Config:
        from_attributes = True