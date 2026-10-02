from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=List[schemas.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    category: str | None = None,
    published_year: int | None = None,
    author: str | None = None,
    max_price: float | None = None,
    sort_by: str | None = None,
    limit: int =10,
    skip: int = 0
):

    query = db.query(models.Book)

    if category:
        query = query.filter(models.Book.category == category)
    if published_year:
        query = query.filter(models.Book.published_year == published_year)
    if author:
        query = query.filter(models.Book.author == author)
    if max_price:
        query = query.filter(models.Book.price <= max_price)

    if sort_by:
        if sort_by == "price":
            query = query.order_by(models.Book.price)
        elif sort_by == "published_year":
            query = query.order_by(models.Book.published_year)
        elif sort_by == "title":
            query = query.order_by(models.Book.title)

    books = query.offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/categories/", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Book.category).distinct().all()
    return [category[0] for category in categories]

@app.get("/categories/{category}", response_model=List[schemas.BookResponse])
def get_books_by_category(category: str, db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(models.Book.category == category).all()
    return books


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book.model_dump()
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.patch("/books/{book_id}", response_model=schemas.BookResponse)
def patch_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return 