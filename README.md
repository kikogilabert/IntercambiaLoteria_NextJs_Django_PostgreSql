# IntercambiaLoteria_NextJs_Django_PostgreSql

## Descripción

1. Steps to run the project

### Backend
1. Install PostgresSQL 16.4 from [an External Link](https://www.postgresql.org/ftp/source/).

2. Create a database in PostgresSQL

```bash
cd C:\Program Files\PostgreSQL\16\bin>
psql -U postgres
CREATE DATABASE intercambios_loteria;
```

- Ckeck if database is created:
```bash
\l
                                                                    List of databases
         Name         |  Owner   | Encoding | Locale Provider |      Collate       |       Ctype        | ICU Locale | ICU Rules |   Access privileges
----------------------+----------+----------+-----------------+--------------------+--------------------+------------+-----------+-----------------------
 intercambios_loteria | postgres | UTF8     | libc            | Spanish_Spain.1252 | Spanish_Spain.1252 |            |           |
```

- Close postgress console:
```bash
\q
```

3.  Create a virtual environment and activate it.
```bash
cd to/your/local/repo/path
cd server
python -m venv venv
.\venv\Scripts\activate
```

4. Install dependencies into the virtual environment:
```bash
pip install -r requirements.txt
```

5. Create a .env file in the django_server folder with the following variables:
```bash
-DB_NAME
-DB_USER
-DB_PASSWORD
-DB_HOST
-DB_PORT
-SECRET_KEY
```

6. Run the migrations for the database.

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Run the server, make sure you are in the server folder

```bash
python manage.py runserver
```

8. Try the register with the example object:

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
    "id_propietario": {
        "dni": "12345678A",
        "nombre": "Nombre Prueba",
        "telefono": "987654321",
        "direccion": "Calle Prueba, 456",
        "tipo_propietario": "PF"
    }
}
```


### Frontend

1. Install NodeJS 18.20 from from [an External Link](https://nodejs.org/en/download/prebuilt-installer/current).

2. Once installed, change directory to client and run npm commands.

```bash
cd client
npm install
npm run dev
```

Check if is running: [http://localhost:3000/](http://localhost:3000/).