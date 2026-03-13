import google.genai as genai
from google.genai import types

def generar_consejos_ia(puntuacion, dimension_maxima, api_key):
    try:
        # --- ADVERTENCIA 1: Inicio ---
        print("\n⏳ [1/3] Iniciando cliente de Gemini (Nuevo SDK)...")
        client = genai.Client(api_key=api_key)

        prompt = f"""Un usuario ha sacado una puntuación de {puntuacion}/5 en un test de burnout.
Su mayor problema es la dimensión: {dimension_maxima}.
Genera 3 consejos MUY BREVES (máximo 15 palabras cada uno).

Devuelve EXACTAMENTE este código HTML con tus consejos integrados, sin usar Markdown ni bloques de código:
<div class="consejos-grid">
    <div class="consejo-card">
        <h4>💡 [Título corto 1]</h4>
        <p>[Tu consejo de max 15 palabras]</p>
    </div>
    <div class="consejo-card">
        <h4>⚡ [Título corto 2]</h4>
        <p>[Tu consejo de max 15 palabras]</p>
    </div>
    <div class="consejo-card">
        <h4>🧘 [Título corto 3]</h4>
        <p>[Tu consejo de max 15 palabras]</p>
    </div>
</div>"""

        system_prompt = """Eres un asistente especializado en bienestar laboral para la plataforma Resilio. 
Reglas:
1. Sé empático pero profesional.
2. Da consejos accionables (ej. ejercicios de respiración).
3. No diagnostiques, solo sugiere hábitos.
4. MUY IMPORTANTE: Devuelve ÚNICAMENTE el código HTML puro que se te pide en el prompt. No incluyas saludos ni explicaciones extra."""

        # --- ADVERTENCIA 2: Petición enviada ---
        print("🧠 [2/3] Enviando petición al modelo gemini-3-flash-preview...")
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        
        # --- ADVERTENCIA 3: Éxito ---
        print("✅ [3/3] ¡Respuesta de Gemini 3 Flash recibida con éxito!\n")
        
       # Limpieza a prueba de balas para los backticks de la IA
        texto_limpio = response.text.replace("```html", "").replace("```HTML", "").replace("```", "").strip()
        
        return texto_limpio
        
    except Exception as e:
        # --- ADVERTENCIA DE FALLO EN TERMINAL ---
        print(f"\n❌ ERROR CRÍTICO CON GEMINI: {e}\n")
        
        # Si falla, devolvemos una tarjeta roja de aviso para no romper el diseño HTML
        return """
        <div class="consejos-grid">
            <div class="consejo-card" style="border-top-color: #ff4757;">
                <h4>⚠️ Aviso del Sistema</h4>
                <p>Tus resultados se guardaron con éxito, pero los consejos de la IA no pudieron cargar en este momento.</p>
            </div>
        </div>
        """