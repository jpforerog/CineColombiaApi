import pytest
import subprocess
import time
import requests

@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # 🔹 Levanta stack de pruebas
    subprocess.run(
        ["docker-compose", "up", "-d", "--build"],
        cwd="tests/integracion",
        check=True
    )

    # 🔹 Esperar a que la API responda
    url = "http://localhost:8002/peliculas/"
    for _ in range(20):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (200, 404):
                print("✅ API lista!")
                break
        except Exception:
            time.sleep(2)

    yield  # Aquí corren los tests

    # 🔹 Apagar contenedores al finalizar
    subprocess.run(
        ["docker-compose", "down", "-v"],
        cwd="tests/integracion",
        check=True
    )

@pytest.fixture
def api_url():
    return "http://localhost:8002"
