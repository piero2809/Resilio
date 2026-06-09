# Resilio
**Aplicación para detectar el burnout**

Resilio es una aplicación web diseñada para ayudar a detectar el síndrome de burnout en los usuarios mediante la evaluación del test BAT-12. El proyecto cuenta con un backend desarrollado en Flask y una base de datos MySQL, además de integrar capacidades de inteligencia artificial para generar recomendaciones personalizadas.

## Tecnologías Principales

- **Framework Web:** Flask (y Werkzeug)
- **Base de Datos:** MySQL (usando `mysql-connector-python`)
- **Inteligencia Artificial:** Google GenAI (Gemini API)
- **Seguridad y Configuración:** `python-dotenv` para variables de entorno

## Estructura del Proyecto

- `back/`: Contiene el código fuente de la aplicación Flask.
  - `app.py`: Archivo principal con las rutas de la aplicación.
  - `conexion/`: Lógica de conexión a la base de datos MySQL.
  - `servicios/`: Lógica de negocio, incluyendo el procesamiento del test BAT-12 (`test_service.py`) y la integración con IA.
- `BBDD/`: Archivos SQL con la estructura y datos de la base de datos.
- `requirements.txt`: Lista de dependencias del proyecto.

## DEMO DE LA APP
 [Prueba la Demo de Resilio!](resilio-production.up.railway.app)
 
