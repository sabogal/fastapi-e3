# Imagen completa de Python
FROM python:3.11

# Buenas prácticas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo en el contenedor
WORKDIR /code

# Instala dependencias primero (mejor cache)
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código (solo la carpeta app/)
COPY app /code/app

# Expone el puerto
EXPOSE 8000

# Comando por defecto (producción simple)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
