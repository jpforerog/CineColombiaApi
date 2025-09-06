from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Base, engine, async_session
from models import Pelicula
from schemas import PeliculaCreate, PeliculaRead, PeliculaUpdate

app = FastAPI()

# 🔹 Crear las tablas si no existen
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependencia para sesión
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Crear película
@app.post("/peliculas/", response_model=PeliculaRead)
async def create_pelicula(pelicula: PeliculaCreate, session: AsyncSession = Depends(get_session)):
    nueva = Pelicula(**pelicula.dict())
    session.add(nueva)
    await session.commit()
    await session.refresh(nueva)
    return nueva

# Listar todas
@app.get("/peliculas/", response_model=list[PeliculaRead])
async def get_peliculas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Pelicula))
    return result.scalars().all()

# Obtener por ID
@app.get("/peliculas/{pelicula_id}", response_model=PeliculaRead)
async def get_pelicula(pelicula_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Pelicula).where(Pelicula.id == pelicula_id))
    pelicula = result.scalars().first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    return pelicula

# Actualizar
@app.put("/peliculas/{pelicula_id}", response_model=PeliculaRead)
async def update_pelicula(pelicula_id: int, data: PeliculaUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Pelicula).where(Pelicula.id == pelicula_id))
    pelicula = result.scalars().first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(pelicula, key, value)

    session.add(pelicula)
    await session.commit()
    await session.refresh(pelicula)
    return pelicula

# Eliminar
@app.delete("/peliculas/{pelicula_id}")
async def delete_pelicula(pelicula_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Pelicula).where(Pelicula.id == pelicula_id))
    pelicula = result.scalars().first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    await session.delete(pelicula)
    await session.commit()
    return {"message": "Pelicula eliminada"}
