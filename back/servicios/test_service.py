# back/servicios/test_service.py

def calcular_y_guardar_bat12(user_id, form_data, db):
    """
    Procesa las respuestas del BAT-12, calcula medias y guarda en BBDD.
    Retorna una tupla: (éxito_booleano, mensaje_o_media)
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # 1. Mapa de dimensiones
        cursor.execute("SELECT id, dimension_id FROM preguntas")
        mapa_preguntas = {fila['id']: fila['dimension_id'] for fila in cursor.fetchall()}
        
        # 2. Variables matemáticas
        sumas_dimensiones = {1: 0, 2: 0, 3: 0, 4: 0}
        conteos_dimensiones = {1: 0, 2: 0, 3: 0, 4: 0}
        respuestas_para_insertar = []
        suma_total = 0
        total_preguntas = 0

        # 3. Procesar el diccionario del formulario
        for key, value in form_data.items():
            if key.startswith('p_'):
                pregunta_id = int(key.split('_')[1])
                valor_respuesta = int(value)
                
                dim_id = mapa_preguntas.get(pregunta_id)
                if dim_id:
                    sumas_dimensiones[dim_id] += valor_respuesta
                    conteos_dimensiones[dim_id] += 1
                    suma_total += valor_respuesta
                    total_preguntas += 1
                    respuestas_para_insertar.append((pregunta_id, valor_respuesta))

        # Validación
        if total_preguntas < 12:
            return False, "Debes responder a todas las preguntas."

        # 4. Cálculo Científico
        media_agotamiento = round(sumas_dimensiones[1] / conteos_dimensiones[1], 2)
        media_distanciamiento = round(sumas_dimensiones[2] / conteos_dimensiones[2], 2)
        media_cognitivo = round(sumas_dimensiones[3] / conteos_dimensiones[3], 2)
        media_emocional = round(sumas_dimensiones[4] / conteos_dimensiones[4], 2)
        media_total = round(suma_total / 12, 2)

        # 5. Guardar Evaluaciones
        query_eval = """
            INSERT INTO evaluaciones 
            (usuario_id, puntuacion_total, dim_agotamiento, dim_distanciamiento, dim_cognitivo, dim_emocional) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_eval, (user_id, media_total, media_agotamiento, media_distanciamiento, media_cognitivo, media_emocional))
        evaluacion_id = cursor.lastrowid

        # 6. Guardar Auditoría (Respuestas exactas)
        query_resp = "INSERT INTO respuestas_evaluacion (evaluacion_id, pregunta_id, valor) VALUES (%s, %s, %s)"
        datos_respuestas = [(evaluacion_id, p_id, val) for p_id, val in respuestas_para_insertar]
        cursor.executemany(query_resp, datos_respuestas)

        db.commit()
        return True, media_total

    except Exception as e:
        if db: db.rollback()
        return False, str(e)
    finally:
        if cursor: cursor.close()