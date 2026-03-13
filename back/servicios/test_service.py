"""
=================================================
SERVICIO: Test BAT-12 (test_service.py)
=================================================

Este archivo contiene la LÓGICA DE NEGOCIO del test.
Se encarga de:
1. Leer las respuestas del formulario
2. Calcular las medias de cada dimensión
3. Guardar los resultados en la base de datos

CÓMO SE USA:
---------------
Se importa desde app.py y se llama así:
    exito, resultado = calcular_y_guardar_bat12(user_id, request.form, db)

RETORNA:
- (True, media_total) si todo fue bien
- (False, mensaje_error) si hubo algún problema

CONCEPTOS IMPORTANTES:
- BAT-12 tiene 12 preguntas divididas en 4 dimensiones
- Cada dimensión tiene 3 preguntas
- La puntuación va de 1 a 5
- media = suma de valores / número de preguntas
"""

import os
from datetime import datetime
from servicios.ia_service import generar_consejos_ia


def calcular_y_guardar_bat12(user_id, form_data, db):
    """
    Procesa las respuestas del BAT-12, calcula medias y guarda en BBDD.

    PARÁMETROS:
    -----------
    - user_id: ID del usuario que hizo el test
    - form_data: Diccionario con las respuestas (viene del formulario HTML)
    - db: Conexión a la base de datos MySQL

    RETORNA:
    --------
    - Tupla (éxito_booleano, mensaje_o_media)
      Ejemplo: (True, 3.45) o (False, "Debes responder a todas las preguntas")
    """

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)

        # =============================================
        # 1. OBTENER MAPA DE PREGUNTAS
        # =============================================
        # Antes de calcular, necesitamos saber qué pregunta
        # pertenece a qué dimensión.
        # Hacemos una consulta a la tabla 'preguntas'
        # y creamos un diccionario: {pregunta_id: dimension_id}

        cursor.execute("SELECT id, dimension_id FROM preguntas")
        # Convertimos los resultados en un diccionario:
        # mapa_preguntas = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, ...}
        mapa_preguntas = {
            fila["id"]: fila["dimension_id"] for fila in cursor.fetchall()
        }

        # =============================================
        # 2. INICIALIZAR VARIABLES PARA CÁLCULOS
        # =============================================
        # Vamos a sumar los valores de cada dimensión
        # Dimensión 1 = Agotamiento
        # Dimensión 2 = Distanciamiento
        # Dimensión 3 = Deterioro Cognitivo
        # Dimensión 4 = Deterioro Emocional

        sumas_dimensiones = {1: 0, 2: 0, 3: 0, 4: 0}  # Suma de valores
        conteos_dimensiones = {1: 0, 2: 0, 3: 0, 4: 0}  # Cuántas preguntas respondidas
        respuestas_para_insertar = []  # Para guardar en auditoría
        suma_total = 0  # Suma global
        total_preguntas = 0  # Contador global

        # =============================================
        # 3. PROCESAR RESPUESTAS DEL FORMULARIO
        # =============================================
        # El form_data viene como: {'pregunta_1': '3', 'pregunta_2': '4', ...}
        # Iteramos sobre cada respuesta

        for key, value in form_data.items():
            # Solo nos interesan las keys que empiezan por 'pregunta_'
            # (hay otros campos en el formulario)
            if key.startswith("pregunta_"):
                # Extraer el ID de la pregunta del nombre
                # "pregunta_5" -> 5
                pregunta_id = int(key.split("_")[1])

                # Convertir la respuesta a número entero
                valor_respuesta = int(value)

                # Buscar a qué dimensión pertenece esta pregunta
                dim_id = mapa_preguntas.get(pregunta_id)

                if dim_id:
                    # Sumar el valor a la dimensión correspondiente
                    sumas_dimensiones[dim_id] += valor_respuesta
                    conteos_dimensiones[dim_id] += 1

                    # También guardamos para la suma global
                    suma_total += valor_respuesta
                    total_preguntas += 1

                    # Guardamos para auditoría (respuestas individuales)
                    respuestas_para_insertar.append((pregunta_id, valor_respuesta))

        # =============================================
        # 4. VALIDACIÓN
        # =============================================
        # El test tiene 12 preguntas, si responde menos,error
        if total_preguntas < 12:
            return False, "Debes responder a todas las preguntas."

        # =============================================
        # 5. CÁLCULO DE MEDIAS (Estadística)
        # =============================================
        # Fórmula: media = suma / conteo
        # Redondeamos a 2 decimales para que sea legible

        # Media de Agotamiento (dimensión 1)
        media_agotamiento = round(sumas_dimensiones[1] / conteos_dimensiones[1], 2)

        # Media de Distanciamiento (dimensión 2)
        media_distanciamiento = round(sumas_dimensiones[2] / conteos_dimensiones[2], 2)

        # Media de Deterioro Cognitivo (dimensión 3)
        media_cognitivo = round(sumas_dimensiones[3] / conteos_dimensiones[3], 2)

        # Media de Deterioro Emocional (dimensión 4)
        media_emocional = round(sumas_dimensiones[4] / conteos_dimensiones[4], 2)

        # Media global (todas las preguntas)
        media_total = round(suma_total / 12, 2)

        # Determinar dimensión máxima para los consejos
        dimensiones = {
            "agotamiento": media_agotamiento,
            "distanciamiento": media_distanciamiento,
            "cognitivo": media_cognitivo,
            "emocional": media_emocional,
        }
        dimension_maxima = max(dimensiones, key=dimensiones.get)

        # Generar consejos con IA (si está configurada)
        consejos = "No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas."
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                consejos = generar_consejos_ia(media_total, dimension_maxima, api_key)
        except Exception as e:
            print(f"Error al generar consejos: {e}")

        # =============================================
        # 6. GUARDAR EVALUACIÓN EN LA BASE DE DATOS
        # =============================================
        # Insertamos una fila en la tabla 'evaluaciones'

        query_eval = """
            INSERT INTO evaluaciones 
            (usuario_id, puntuacion_total, dim_agotamiento, dim_distanciamiento, dim_cognitivo, dim_emocional, consejos) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query_eval,
            (
                user_id,
                media_total,
                media_agotamiento,
                media_distanciamiento,
                media_cognitivo,
                media_emocional,
                consejos,
            ),
        )

        # Obtenemos el ID de la evaluación que acabamos de crear
        # Esto nos sirve para guardar las respuestas individuales
        evaluacion_id = cursor.lastrowid

        # =============================================
        # 7. GUARDAR AUDITORÍA (RESPUESTAS INDIVIDUALES)
        # =============================================
        # Guardamos cada respuesta por separado (opcional pero útil)
        # Esto permite ver las respuestas exactas después

        query_resp = "INSERT INTO respuestas_evaluacion (evaluacion_id, pregunta_id, valor) VALUES (%s, %s, %s)"

        # Preparamos los datos en el formato correcto
        datos_respuestas = [
            (evaluacion_id, p_id, val) for p_id, val in respuestas_para_insertar
        ]

        # executemany() ejecuta la misma consulta múltiples veces
        cursor.executemany(query_resp, datos_respuestas)

        # =============================================
        # 8. CONFIRMAR CAMBIOS
        # =============================================
        # commit() guarda definitivamente los cambios en la base de datos
        db.commit()

        # Si todo fue bien, retornamos True y la media total
        return True, media_total

    except Exception as e:
        # Si hay cualquier error (base de datos, etc.)
        # Deshacemos los cambios para no dejar datos a medias
        if db:
            db.rollback()
        return False, str(e)

    finally:
        # SIEMPRE cerramos el cursor, tanto si hay error como si no
        if cursor:
            cursor.close()



