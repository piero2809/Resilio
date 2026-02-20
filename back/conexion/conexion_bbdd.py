import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='resilio',      
            password='Resilio123$',  
            database='resilio_db'       
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None 