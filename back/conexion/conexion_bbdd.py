import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='resilio',      # Cambia por tu usuario de MySQL
            password='Resilio123$',  # Cambia por tu contraseña
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
