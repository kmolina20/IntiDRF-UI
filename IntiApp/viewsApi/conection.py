import psycopg2

try:
    credenciales = {
        "dbname": "db_metadata",
        "user": "postgres",
        "password": "root",
        "host": "localhost",
        "port": 5432
    }
    conexion = psycopg2.connect(**credenciales)
except psycopg2.Error as e:
    print("Ocurrió un error al conectar a PostgreSQL: ", e)