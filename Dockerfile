# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /code

# Copiar requirements e instalar
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app
COPY . .

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
