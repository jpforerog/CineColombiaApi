from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Base, engine, async_session
from app.models import Pelicula
from app.schemas import PeliculaCreate, PeliculaRead, PeliculaUpdate
from app import monitoring
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI()
# 👇 Middleware global para contar y medir requests
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    monitoring.REQUEST_COUNT.labels(
        request.method, request.url.path, response.status_code
    ).inc()

    monitoring.REQUEST_LATENCY.labels(request.url.path).observe(process_time)

    return response

# 👇 Incluimos el router con el endpoint /metrics
app.include_router(monitoring.router)

Instrumentator().instrument(app).expose(app)
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


