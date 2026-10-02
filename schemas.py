from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    category: str
    in_stock: bool = Field(default=True)
    published_year: int | None = Field(default=None)


class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = None
    category: str | None = None
    in_stock: bool | None = None
    published_year: int | None = None

    