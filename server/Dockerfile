# Usa una imagen de Python
FROM python:3.10-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia el archivo de requerimientos
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al contenedor
COPY django_backend/ ./django_backend/

# Copia el script de entrada al contenedor
# COPY django_backend/run.sh /usr/src/app/run.sh

# Hace el script ejecutable
# RUN chmod +x /usr/src/app/run.sh

# Expone el puerto 8000
EXPOSE 8888

# Usa el script como el punto de entrada
# ENTRYPOINT ["/usr/src/app/run.sh"]


# Expone el puerto 8000
EXPOSE 8888

# Corre el servidor de desarrollo de Django
CMD ["python", "django_backend/manage.py", "runserver", "0.0.0.0:8888"]

