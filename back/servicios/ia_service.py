import os
import google.genai as genai


def generar_consejos_IA(puntuacion, dimension_maxima, respuestas_pico):
    """
    Genera consejos personalizados usando Google Gemini.

    Parámetros:
    - puntuacion: float (media global, ej: 3.5)
    - dimension_maxima: str (la dimensión con peor puntuación: 'agotamiento', 'distanciamiento', 'cognitivo', 'emocional')
    - respuestas_pico: list de tuplas [(pregunta_id, valor, texto_pregunta), ...] con valores 4 o 5
    """

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None, "Error: No se ha configurado la API key de Gemini."

    genai.configure(api_key=api_key)

    # Determinar nivel de riesgo        
    if puntuacion >= 4:
        nivel = "CRÍTICO"
        nivel_texto = (
            "Tu nivel de burnout es alto. Es importante que busques ayuda profesional."
        )
    elif puntuacion >= 3:
        nivel = "MODERADO"
        nivel_texto = "Tu nivel de burnout es moderado. Te animamos a implementar cambios positivos."
    else:
        nivel = "BAJO"
        nivel_texto = "¡Tu nivel de burnout es bajo! Sigue cuidando tu bienestar."

    # Procesar respuestas pico para el prompt
    texto_picos = ""
    if respuestas_pico:
        texto_picos = "\nPreguntas con respuestas de mayor concern (4-5):\n"
        for preg_id, valor, texto in respuestas_pico[:3]:
            texto_picos += f"- {texto} (Respuesta: {valor}/5)\n"

    # Prompt dinámico
    prompt = f"""Un usuario ha sacado una puntuación de {puntuacion}/5 en un test de burnout.
Su mayor problema es la dimensión: {dimension_maxima}.
{texto_picos}
Dame 3 consejos cortos y accionables para mejorar su salud mental hoy mismo."""

    # Instrucciones del sistema
    system_prompt = """Eres un asistente especializado en bienestar laboral y emocionalpara la plataforma Resilio. 
Tus consejos deben basarse en la metodología del test BAT-12 (Burnout Assessment Tool).
Reglas estrictas:
1. Sé empático pero profesional.
2. Si el nivel es crítico, recomienda SIEMPRE consultar con un profesional de la salud.
3. Da consejos accionables (ej. ejercicios de respiración, gestión de pausas).
4. No diagnostiques, solo sugiere hábitos basados en los resultados."""

    try:
        model = genai.GenerativeModel(
            "models/gemini-2.5-flash-lite", system_instruction=system_prompt
        )
        response = model.generate_content(prompt)
        return nivel_texto, response.text
    except Exception as e:
        print(f"Error con Gemini: {e}")
        return None, "Tómate un breve descanso y practica la respiración consciente mientras cargamos tus consejos personalizados."
