import pytest
import requests

@pytest.fixture
def pelicula_data():
    return {
        "nombre": "Inception",
        "categoria": "Sci-Fi",
        "ano": 2010,
        "director": "Christopher Nolan",
        "duracion": 148,
        "calificacion": 8.8
    }

def test_create_pelicula(api_url, pelicula_data):
    r = requests.post(f"{api_url}/peliculas/", json=pelicula_data)
    assert r.status_code == 200
    data = r.json()
    assert data["nombre"] == pelicula_data["nombre"]
    return data["id"]  # opcional si se quiere encadenar


def test_get_all_peliculas(api_url, pelicula_data):
    # Crear primero
    r = requests.post(f"{api_url}/peliculas/", json=pelicula_data)
    pelicula_id = r.json()["id"]

    r = requests.get(f"{api_url}/peliculas/")
    assert r.status_code == 200
    peliculas = r.json()
    assert any(p["id"] == pelicula_id for p in peliculas)


def test_get_pelicula_by_id(api_url, pelicula_data):
    r = requests.post(f"{api_url}/peliculas/", json=pelicula_data)
    pelicula_id = r.json()["id"]

    r = requests.get(f"{api_url}/peliculas/{pelicula_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["nombre"] == pelicula_data["nombre"]


def test_update_pelicula(api_url, pelicula_data):
    r = requests.post(f"{api_url}/peliculas/", json=pelicula_data)
    pelicula_id = r.json()["id"]

    update = {**pelicula_data, "duracion": 150, "calificacion": 9.0}
    r = requests.put(f"{api_url}/peliculas/{pelicula_id}", json=update)
    assert r.status_code == 200
    data = r.json()
    assert data["duracion"] == 150
    assert data["calificacion"] == 9.0


def test_delete_pelicula(api_url, pelicula_data):
    r = requests.post(f"{api_url}/peliculas/", json=pelicula_data)
    pelicula_id = r.json()["id"]

    r = requests.delete(f"{api_url}/peliculas/{pelicula_id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Pelicula eliminada"

    # Confirmar borrado
    r = requests.get(f"{api_url}/peliculas/{pelicula_id}")
    assert r.status_code == 404
