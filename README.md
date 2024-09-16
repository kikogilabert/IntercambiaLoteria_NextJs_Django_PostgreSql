# IntercambiaLoteria_NextJs_Django_PostgreSql

## Descripción

1. Steps to run the project

### Backend
0.1 Install PostgresSQL

0.2 Create a database in PostgresSQL

0.3 Create a virtual environment

0.4 Create a .env file in the django_server folder with the following variables:

-DB_NAME

-DB_USER

-DB_PASSWORD

-DB_HOST

-DB_PORT

-SECRET_KEY


1. Install dependencies once in the virtual environment

```bash
pip install -r requirements.txt
```
2. Run the server, make sure you are in the server folder

```bash
python manage.py runserver
```

3. Run the migrations for the database

```bash
python manage.py makemigrations
python manage.py migrate
```

Try the register with the example object:

endpoint must be: http://localhost:8000/administracion/register/

```json
{
    "num_receptor": 12345,
    "id_administracion": "22",
    "nombre_comercial": "Comercial Prueba",
    "password":"tilitili",
    "direccion": "Calle Prueba, 123",
    "localidad": "Localidad Prueba",
    "provincia": "Provincia Prueba",
    "numero_admon": 123,
    "codigo_postal": "12345",
    "email": "prueba@example.com",
    "telefono": "123456789",
    "propietario": {
        "dni": "12345678A",
        "nombre": "Nombre Prueba",
        "telefono": "987654321",
        "direccion": "Calle Prueba, 456",
        "tipo_propietario": "PF"
    }
}
```


### Frontend
cd /client
    
```bash 
npm install
```
    
```bash
npm run dev
```