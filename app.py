from fastapi import FastAPI, HTTPException, Depends
import os



jsonPeliculas = {
  "peliculas": [
    {
        "id":1,
      "nombre": "El Padrino",
      "categoria": "Drama",
      "año": 1972,
      "director": "Francis Ford Coppola",
      "duracion": 175,
      "calificacion": 9.2
    },
    {
        "id":2,
      "nombre": "Pulp Fiction",
      "categoria": "Acción",
      "año": 1994,
      "director": "Quentin Tarantino",
      "duracion": 154,
      "calificacion": 8.9
    },
    {
        "id":3,
      "nombre": "El Señor de los Anillos: La Comunidad del Anillo",
      "categoria": "Fantasía",
      "año": 2001,
      "director": "Peter Jackson",
      "duracion": 178,
      "calificacion": 8.8
    }
  ]
        }
# FastAPI app
app = FastAPI(
    title="API de Películas",
    description="API REST para gestionar información de películas",
    version="1.0.0"
)




@app.get("/peliculas")
async def listar_peliculas():
    return jsonPeliculas

@app.get("/peliculas/{id}")
async def obtener_pelicula(id: int):
    """Obtener los detalles de una película por su ID"""
    resultado = list(filter(lambda p: p["id"] == id, jsonPeliculas["peliculas"]))
    if resultado is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return resultado

"""@app.post("/peliculas", response_model=MovieResponse, status_code=201)
async def crear_pelicula(movie: MovieCreate, db: Session = Depends(get_db)):
    
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie"""

"""@app.put("/peliculas/{id}", response_model=MovieResponse)
async def actualizar_pelicula(id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
   
    db_movie = db.query(Movie).filter(Movie.id == id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Actualizar solo los campos proporcionados
    for field, value in movie_update.dict(exclude_unset=True).items():
        setattr(db_movie, field, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie"""

"""@app.delete("/peliculas/{id}", status_code=204)
async def eliminar_pelicula(id: int, db: Session = Depends(get_db)):
    
    db_movie = db.query(Movie).filter(Movie.id == id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    db.delete(db_movie)
    db.commit()
    return

@app.get("/")
async def root():
   
    return {"message": "API de Películas funcionando correctamente"}"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)