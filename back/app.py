import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='tu_usuario',      # Cambia por tu usuario de MySQL
            password='tu_password',  # Cambia por tu contraseña
            database='resilio'       # El nombre de tu BBDD
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Ejemplo de cómo usarías el cursor en tus funciones:
# conexion = obtener_conexion()
# cursor = conexion.cursor(dictionary=True) # dictionary=True devuelve los datos como diccionarios

CREATE USER 
'resilio'@'localhost' 
IDENTIFIED  BY 'Resilio123$';

GRANT USAGE ON *.* TO 'resilio'@'localhost';

ALTER USER 'resilio'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON resilio.* 
TO 'resilio'@'localhost';

FLUSH PRIVILEGES;