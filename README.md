# 🧠 Resilio - Plataforma de Detección del Burnout

**Resilio** es una aplicación web integral diseñada para evaluar, monitorizar y prevenir el Síndrome de Burnout (Agotamiento Profesional) en entornos organizacionales y personales.

La herramienta utiliza el **test BAT-12** (Burnout Assessment Tool) con rigor científico y lo combina con la inteligencia artificial de **Google Gemini** para ofrecer consejos personalizados basados en los resultados individuales.

## 🚀 Características Principales

*   **Evaluación Científica (BAT-12):** Diagnóstico preciso basado en 4 dimensiones del burnout (Agotamiento, Distanciamiento Mental, Deterioro Cognitivo y Deterioro Emocional).
*   **Roles Múltiples:**
    *   **Administrador:** Visión global de toda la plataforma, gestión de empresas y usuarios, exportación de datos y estadísticas globales.
    *   **Recursos Humanos (HR):** Panel específico para la empresa asignada, permitiendo monitorizar la salud mental por departamentos manteniendo la privacidad individual.
    *   **Empleado / Personal:** Historial de evaluaciones, evolución temporal y consejos personalizados generados por IA.
*   **Paneles de Control (Dashboards):** Gráficos e indicadores de riesgo en tiempo real.
*   **Integración con IA:** Generación automática de recomendaciones de bienestar a través de Google GenAI (Gemini API).
*   **Exportación de Datos:** Descarga de informes en formato CSV para análisis externo.

## 🛠️ Tecnologías

*   **Backend:** Python, Flask (y Werkzeug)
*   **Base de Datos:** MySQL (con `mysql-connector-python`)
*   **Inteligencia Artificial:** Google GenAI (Gemini API)
*   **Frontend:** HTML5, CSS3, JavaScript (Plantillas Jinja2)
*   **Configuración:** `python-dotenv` para gestión de variables de entorno

## 📁 Estructura del Proyecto

```text
resilio/
├── back/
│   ├── app.py                ← Núcleo de la aplicación Flask: rutas y controladores
│   ├── conexion/
│   │   └── conexion_bbdd.py  ← Capa de acceso y pool de conexiones a MySQL
│   ├── database/             ← Scripts SQL para esquemas y datos iniciales
│   │   ├── resilio_db_actual.sql
│   │   └── schema.sql
│   ├── servicios/
│   │   ├── test_service.py   ← Lógica de negocio para calcular el BAT-12
│   │   └── ia_service.py     ← Interfaz con la API de Google Gemini
│   ├── static/               ← Archivos estáticos (CSS, JS, Imágenes)
│   └── templates/            ← Vistas HTML (Jinja2)
│       ├── dashboards/       ← Paneles específicos por rol (admin, hr, empleado, personal)
│       ├── test.html         ← Vista del cuestionario
│       └── historial.html    ← Vista del histórico de resultados
├── Estructura.txt            ← Resumen de la estructura
├── .gitignore
└── README.md
```

## 🌐 Demo de la Aplicación

¡Puedes probar Resilio en producción de forma online!

👉 **[Prueba la Demo de Resilio](https://resilio-production.up.railway.app)**
