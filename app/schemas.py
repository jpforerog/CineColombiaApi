# schemas.py
from pydantic import BaseModel

class PeliculaBase(BaseModel):
    nombre: str
    categoria: str
    ano: int
    director: str
    duracion: int
    calificacion: float

# Para crear película (input)
class PeliculaCreate(PeliculaBase):
    pass

# Para actualizar película
class PeliculaUpdate(BaseModel):
    nombre: str | None = None
    categoria: str | None = None
    ano: int | None = None
    director: str | None = None
    duracion: int | None = None
    calificacion: float | None = None

# Para devolver película (output)
class PeliculaRead(PeliculaBase):
    id: int

    class Config:
        orm_mode = True
