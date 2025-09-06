# database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DB_USER = os.getenv("DB_USER", "juan")
DB_PASS = os.getenv("DB_PASS", "MYSQL_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "db")  # 👈 importante: host = db
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "mydb")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
