import google.genai as genai

def generar_consejos_ia(puntuacion, dimension_maxima, api_key):
    """
    Genera consejos personalizados usando Google Gemini.
    """
    try:
        # Usamos el cliente moderno de Gemini
        client = genai.Client(api_key=api_key)

        prompt = f"""Un usuario ha sacado una puntuación de {puntuacion}/5 en un test de burnout.
Su mayor problema es la {dimension_maxima}.
Dame 3 consejos cortos y accionables para mejorar su salud mental hoy mismo."""

        system_prompt = """Eres un asistente especializado en bienestar laboral para la plataforma Resilio. 
Tus consejos deben basarse en la metodología del test BAT-12 (Burnout Assessment Tool).
Reglas estrictas:
1. Sé empático pero profesional.
2. Si el nivel es crítico, recomienda SIEMPRE consultar con un profesional de la salud.
3. Da consejos accionables (ej. ejercicios de respiración, gestión de pausas).
4. No diagnostiques, solo sugiere hábitos basados en los resultados."""

        # AQUÍ DEFINIMOS EL MODELO EN UN SOLO LUGAR
        response = client.models.generate_content(
            model="gemini-3.0-flash", # Puedes cambiar esto en el futuro fácilmente
            contents=prompt,
            config=genai.types.GenerateContentConfig(system_instruction=system_prompt),
        )
        return response.text
        
    except Exception as e:
        print(f"Error con Gemini: {e}")
        if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
            return "Cuota de la API agotada. Intenta de nuevo en unas horas o verifica los límites en Google AI Studio."
        return "Tómate un breve descanso y practica la respiración consciente mientras cargamos tus consejos personalizados."