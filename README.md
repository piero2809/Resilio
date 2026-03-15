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

## Instalación y Configuración

1. **Clonar el repositorio y preparar el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos:**
   - Se requiere un servidor MySQL en ejecución.
   - Utilizar el archivo SQL correspondiente en la carpeta `BBDD/` (e.g. `reslio_db_actual.sql`) para crear el esquema y cargar los datos iniciales.
   - La conexión por defecto está configurada en `back/conexion/conexion_bbdd.py` (Host: `localhost`, Usuario: `resilio`, Contraseña: `Resilio123$`, Base de datos: `resilio_db`).

4. **Variables de Entorno:**
   - Asegúrate de configurar las variables de entorno necesarias, en especial `GEMINI_API_KEY` para los consejos de IA. Crea un archivo `API-KEY.env` en la raíz de la carpeta `back/` o en su ubicación requerida si corresponde.

## Ejecución de la Aplicación

Para iniciar el servidor de desarrollo, ejecuta:

```bash
python back/app.py
```

## Ejecución de Pruebas

El proyecto utiliza `pytest` para las pruebas automatizadas. Para ejecutar las pruebas correctamente desde el directorio raíz del proyecto:

```bash
PYTHONPATH=. pytest
```
