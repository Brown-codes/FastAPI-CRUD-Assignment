from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

database_url = "sqlite:///./bookstore.db"

engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

