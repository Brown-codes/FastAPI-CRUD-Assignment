from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    author: Mapped[str] = mapped_column(index=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(index=True, nullable=False)
    in_stock: Mapped[bool] = mapped_column(nullable=False, default=True)
    published_year: Mapped[int|None] = mapped_column(default=None)

