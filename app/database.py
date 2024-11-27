from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_DATABASE_URl = 'postgresql://karik:karik2022@localhost/postgres'

engine = create_engine(SQL_DATABASE_URl)

SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
