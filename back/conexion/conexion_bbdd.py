"""
=================================================
CONEXIÓN A BASE DE DATOS (conexion_bbdd.py)
=================================================

Este archivo se encarga de conectar con la base de datos MySQL.

¿PARA QUÉ SIRVE?
-----------------
Cada vez que necesitamos leer o escribir en la base de datos,
primero llamamos a obtener_conexion() para establecer conexión.

CONCEPTOS BÁSICOS:
-------------------
- MySQL: Sistema de gestión de bases de datos relacional
- Host: Dirección del servidor (localhost = tu propio ordenador)
- User: Nombre de usuario para conectar
- Password: Contraseña (nunca pongáis estas cosas en Git!)
- Database: Nombre de la base de datos específica

NOTA DE SEGURIDAD:
-------------------
En un proyecto real, las credenciales (password, user)
deberían estar en variables de entorno, NO hardcodeadas.
"""

# Importamos la librería de MySQL para Python
import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    """
    Función que establece conexión con MySQL.

    RETORNA:
    --------
    - conexion: Objeto de conexión si todo fue bien
    - None: Si hubo algún error al conectar

    CÓMO USARLA:
    -------------
    from conexion.conexion_bbdd import obtener_conexion

    db = obtener_conexion()
    if db:
        cursor = db.cursor()
        # hacer consultas...
        cursor.close()
        db.close()
    """

    try:
        # =============================================
        # CONECTAR A MYSQL
        # =============================================
        # mysql.connector.connect() crea una conexión al servidor

        conexion = mysql.connector.connect(
            host="localhost",  # Servidor MySQL (aquí es local)
            user="resilio",  # Usuario de la base de datos
            password="Resilio123$",  # Contraseña del usuario
            database="resilio_db",  # Nombre de la base de datos
        )

        # Verificar que la conexión fue exitosa
        # is_connected() devuelve True si todo OK
        if conexion.is_connected():
            # Devolvemos el objeto de conexión para usarlo
            return conexion

    except Error as e:
        # Si hay algún error (servidor no disponible, credenciales mal, etc.)
        # Lo打印imos en consola (en producción sería un log)
        print(f"Error al conectar a MySQL: {e}")
        return None
