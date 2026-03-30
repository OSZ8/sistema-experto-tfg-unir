# Usa una imagen oficial y ligera de Python 3.11 adaptada a producción
FROM python:3.11-slim

# Metadatos del TFG
LABEL maintainer="Oscar Sánchez"
LABEL project="Sistema Experto TFG LoL"

# Evita que Python genere archivos .pyc en disco (mejora rendimiento)
ENV PYTHONDONTWRITEBYTECODE=1
# Obliga a Python a imprimir los logs directamente sin buffer
ENV PYTHONUNBUFFERED=1

# Configura el directorio de trabajo en el contenedor de Docker
WORKDIR /app

# Copia estrictamente los ficheros de dependencias primero para cachear capas
COPY requirements.txt .

# Instala las librerías base necesarias sin almacenar caché para aligerar la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda la arquitectura backend y frontend al contenedor
COPY . .

# Expone el puerto por el que Flask/Gunicorn servirá peticiones HTTP
EXPOSE 5000

# Añade un usuario sin privilegios root por motivos de ciberseguridad
RUN useradd -m tfg_user
USER tfg_user

# Punto de entrada maestro: Arranca el servidor asíncrono Gunicorn de producción (No usamos pre-cargado de Flask "app.run")
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
