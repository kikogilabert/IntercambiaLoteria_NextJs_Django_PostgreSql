#!/bin/sh

# # Espera a que la base de datos esté disponible
# echo "Esperando a que la base de datos esté disponible..."
# while ! nc -z $DJANGO_DB_HOST 5432; do
#   sleep 1
# done

# # Ejecuta las migraciones
# echo "Aplicando migraciones..."
# python django_backend/manage.py makemigrations
# python django_backend/manage.py migrate

# # Corre el servidor de desarrollo de Django
# exec python django_backend/manage.py runserver 0.0.0.0:8888