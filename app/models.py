# models.py
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    categoria = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    director = Column(String(255), nullable=False)
    duracion = Column(Integer, nullable=False)  # en minutos
    calificacion = Column(Float, nullable=False)
