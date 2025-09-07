import os
import time
import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    # URL donde estará accesible la API desde la máquina host
    url = os.getenv("API_URL", "http://localhost:8001")
    # Espera hasta que /docs o /openapi.json responda (máx ~60s)
    for _ in range(60):
        try:
            r = requests.get(f"{url}/docs", timeout=2)
            if r.status_code < 500:
                return url
        except Exception:
            time.sleep(1)
    pytest.exit(f"API no respondió en {url} — asegúrate de levantar docker compose")
