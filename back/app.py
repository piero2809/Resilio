"""
=================================================
RESILIO - Aplicación para Detectar el Burnout
=================================================
"""

from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "API-KEY.env"))

from flask import Flask, render_template, request, redirect, url_for, session, flash
from conexion.conexion_bbdd import obtener_conexion
from servicios.test_service import calcular_y_guardar_bat12
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "123123123"


# --------------------------------------------------------
# RUTA PRINCIPAL
# --------------------------------------------------------
@app.route("/")
def index():
    return redirect(url_for("login"))


# --------------------------------------------------------
# LOGIN
# --------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_candidata = request.form["password"]

        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT u.*, e.nombre AS empresa_nombre, d.nombre AS departamento_nombre
            FROM usuarios u
            LEFT JOIN empresas e ON u.empresa_id = e.id
            LEFT JOIN departamentos d ON u.departamento_id = d.id
            WHERE u.email = %s
        """
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        db.close()

        if usuario and check_password_hash(usuario["password"], password_candidata):
            session["user_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol_id"]
            session["empresa_id"] = usuario["empresa_id"]
            session["nombre_empresa"] = usuario["empresa_nombre"]
            session["nombre_dept"] = usuario["departamento_nombre"]
            return redirect(url_for("dashboard"))
        else:
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


# --------------------------------------------------------
# DASHBOARD - Con lógica de admin mejorada
# --------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    rol = session["rol"]
    user_id = session["user_id"]

    # ─── ADMIN (rol 1) ───────────────────────────────────
    if rol == 1:
        db = obtener_conexion()
        if not db:
            flash("Error de conexión a la base de datos.", "error")
            return redirect(url_for("login"))

        cursor = db.cursor(dictionary=True)

        try:
            # KPIs principales
            cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
            total_usuarios = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM empresas")
            total_empresas = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM evaluaciones")
            total_evaluaciones = cursor.fetchone()["total"]

            # Nuevos usuarios este mes
            cursor.execute("""
                SELECT COUNT(*) AS total FROM usuarios
                WHERE MONTH(fecha_registro) = MONTH(NOW())
                AND YEAR(fecha_registro) = YEAR(NOW())
            """)
            nuevos_usuarios_mes = cursor.fetchone()["total"]

            # Evaluaciones este mes
            cursor.execute("""
                SELECT COUNT(*) AS total FROM evaluaciones
                WHERE MONTH(fecha) = MONTH(NOW())
                AND YEAR(fecha) = YEAR(NOW())
            """)
            evaluaciones_mes = cursor.fetchone()["total"]

            # Usuarios en riesgo alto (puntuación >= 3.5)
            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) AS total
                FROM (
                    SELECT usuario_id, puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                    FROM evaluaciones
                ) t
                WHERE rn = 1 AND puntuacion_total >= 3.5
            """)
            usuarios_riesgo_alto = cursor.fetchone()["total"]

            pct_riesgo_alto = round((usuarios_riesgo_alto / total_usuarios * 100), 1) if total_usuarios > 0 else 0

            stats = {
                "total_usuarios": total_usuarios,
                "total_empresas": total_empresas,
                "total_evaluaciones": total_evaluaciones,
                "nuevos_usuarios_mes": nuevos_usuarios_mes,
                "evaluaciones_mes": evaluaciones_mes,
                "usuarios_riesgo_alto": usuarios_riesgo_alto,
                "pct_riesgo_alto": pct_riesgo_alto,
            }

            # Últimos 10 usuarios con conteo de evaluaciones
            cursor.execute("""
                SELECT u.id, u.nombre, u.apellidos, u.email, u.rol_id, u.fecha_registro,
                       e.nombre AS empresa_nombre,
                       COUNT(ev.id) AS total_evaluaciones
                FROM usuarios u
                LEFT JOIN empresas e ON u.empresa_id = e.id
                LEFT JOIN evaluaciones ev ON ev.usuario_id = u.id
                GROUP BY u.id, u.nombre, u.apellidos, u.email, u.rol_id,
                         u.fecha_registro, e.nombre
                ORDER BY u.fecha_registro DESC
                LIMIT 10
            """)
            usuarios = cursor.fetchall()

            # Empresas con conteo de empleados
            cursor.execute("""
                SELECT e.id, e.nombre, e.sector, e.codigo_registro,
                       COUNT(u.id) AS total_empleados
                FROM empresas e
                LEFT JOIN usuarios u ON u.empresa_id = e.id
                GROUP BY e.id, e.nombre, e.sector, e.codigo_registro
                ORDER BY e.id DESC
            """)
            empresas = cursor.fetchall()

            # Usuarios en riesgo alto (con datos)
            cursor.execute("""
                SELECT u.nombre, u.apellidos, emp.nombre AS empresa_nombre,
                       t.puntuacion_total AS ultima_puntuacion
                FROM (
                    SELECT usuario_id, puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                    FROM evaluaciones
                ) t
                JOIN usuarios u ON u.id = t.usuario_id
                LEFT JOIN empresas emp ON emp.id = u.empresa_id
                WHERE t.rn = 1 AND t.puntuacion_total >= 2.5
                ORDER BY t.puntuacion_total DESC
                LIMIT 8
            """)
            usuarios_riesgo = cursor.fetchall()

            # Actividad reciente (últimos registros y evaluaciones)
            cursor.execute("""
                (SELECT 'registro' AS tipo, u.nombre, u.apellidos, u.email,
                        NULL AS puntuacion, u.fecha_registro AS fecha
                 FROM usuarios u ORDER BY fecha_registro DESC LIMIT 5)
                UNION ALL
                (SELECT 'evaluacion' AS tipo, u.nombre, u.apellidos, u.email,
                        ev.puntuacion_total AS puntuacion, ev.fecha AS fecha
                 FROM evaluaciones ev
                 JOIN usuarios u ON u.id = ev.usuario_id
                 ORDER BY ev.fecha DESC LIMIT 5)
                ORDER BY fecha DESC
                LIMIT 8
            """)
            raw_actividad = cursor.fetchall()

            # Formatear actividad para el template
            from datetime import datetime, timezone

            actividad = []
            now = datetime.now()
            for item in raw_actividad:
                fecha = item["fecha"]
                # Calcular tiempo relativo
                if hasattr(fecha, 'replace'):
                    diff = now - fecha.replace(tzinfo=None)
                    total_sec = int(diff.total_seconds())
                    if total_sec < 3600:
                        tiempo = f"hace {total_sec // 60} min"
                    elif total_sec < 86400:
                        tiempo = f"hace {total_sec // 3600}h"
                    else:
                        tiempo = f"hace {total_sec // 86400}d"
                else:
                    tiempo = "—"

                if item["tipo"] == "registro":
                    actividad.append({
                        "titulo": f"Nuevo usuario registrado",
                        "descripcion": f"{item['nombre']} {item['apellidos'] or ''}",
                        "tiempo": tiempo,
                        "icon": "user-plus",
                        "color": "green"
                    })
                else:
                    puntuacion = float(item["puntuacion"]) if item["puntuacion"] else 0
                    color = "red" if puntuacion >= 3.5 else ("yellow" if puntuacion >= 2.5 else "green")
                    actividad.append({
                        "titulo": "Evaluación completada",
                        "descripcion": f"{item['nombre']} — {puntuacion:.2f}/5",
                        "tiempo": tiempo,
                        "icon": "clipboard-check",
                        "color": color
                    })

            # Tendencia mensual (últimos 6 meses)
            cursor.execute("""
                SELECT
                    DATE_FORMAT(fecha, '%b %Y') AS mes,
                    COUNT(*) AS total,
                    SUM(CASE WHEN puntuacion_total >= 3.5 THEN 1 ELSE 0 END) AS riesgo_alto
                FROM evaluaciones
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(fecha, '%Y-%m'), DATE_FORMAT(fecha, '%b %Y')
                ORDER BY MIN(fecha) ASC
            """)
            tendencia_mensual = cursor.fetchall()

            # Si no hay datos de tendencia, generamos datos vacíos para el gráfico
            if not tendencia_mensual:
                from datetime import date
                import calendar
                meses = []
                for i in range(5, -1, -1):
                    d = date.today().replace(day=1)
                    # restar i meses
                    month = d.month - i
                    year = d.year
                    while month <= 0:
                        month += 12
                        year -= 1
                    mes_nombre = calendar.month_abbr[month] + ' ' + str(year)
                    meses.append({"mes": mes_nombre, "total": 0, "riesgo_alto": 0})
                tendencia_mensual = meses

            # Convertir los Decimal a float para tojson
            for t in tendencia_mensual:
                t["total"] = int(t["total"])
                t["riesgo_alto"] = int(t["riesgo_alto"])

        except Exception as e:
            flash(f"Error al cargar el panel de administración: {e}", "error")
            stats = {"total_usuarios": 0, "total_empresas": 0, "total_evaluaciones": 0,
                     "nuevos_usuarios_mes": 0, "evaluaciones_mes": 0,
                     "usuarios_riesgo_alto": 0, "pct_riesgo_alto": 0}
            usuarios = []
            empresas = []
            usuarios_riesgo = []
            actividad = []
            tendencia_mensual = []
        finally:
            cursor.close()
            db.close()

        return render_template(
            "dashboards/admin.html",
            stats=stats,
            usuarios=usuarios,
            empresas=empresas,
            usuarios_riesgo=usuarios_riesgo,
            actividad=actividad,
            tendencia_mensual=tendencia_mensual,
        )

    # ─── HR (rol 2) ──────────────────────────────────────
    elif rol == 2:
        return render_template("dashboards/hr.html")

    # ─── USUARIO PERSONAL (rol 3) ────────────────────────
    elif rol == 3:
        db = obtener_conexion()
        ultima_evaluacion = None
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT puntuacion_total, dim_agotamiento, dim_distanciamiento,
                       dim_cognitivo, dim_emocional, fecha, consejos
                FROM evaluaciones
                WHERE usuario_id = %s
                ORDER BY fecha DESC LIMIT 1
            """, (user_id,))
            ultima_evaluacion = cursor.fetchone()
            cursor.close()
            db.close()
        return render_template("dashboards/personal.html", evaluacion=ultima_evaluacion)

    # ─── EMPLEADO EMPRESA (rol 4) ────────────────────────
    elif rol == 4:
        db = obtener_conexion()
        ultima_evaluacion = None
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT puntuacion_total, dim_agotamiento, dim_distanciamiento,
                       dim_cognitivo, dim_emocional, fecha, consejos
                FROM evaluaciones
                WHERE usuario_id = %s
                ORDER BY fecha DESC LIMIT 1
            """, (user_id,))
            ultima_evaluacion = cursor.fetchone()
            cursor.close()
            db.close()
        return render_template("dashboards/empleado.html", evaluacion=ultima_evaluacion)

    else:
        session.clear()
        flash("Error de permisos. Rol no reconocido.", "error")
        return redirect(url_for("login"))


# --------------------------------------------------------
# LOGOUT
# --------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------------------
# HISTORIAL
# --------------------------------------------------------
@app.route("/historial")
def historial():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = obtener_conexion()
    evaluaciones = []

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, puntuacion_total, dim_agotamiento, dim_distanciamiento,
                   dim_cognitivo, dim_emocional, fecha, consejos
            FROM evaluaciones
            WHERE usuario_id = %s
            ORDER BY fecha DESC
        """, (user_id,))
        evaluaciones = cursor.fetchall()

        cursor.execute("SELECT id, texto FROM preguntas WHERE es_activo = 1 ORDER BY id")
        preguntas = {fila["id"]: fila["texto"] for fila in cursor.fetchall()}

        for eval in evaluaciones:
            cursor.execute("""
                SELECT pregunta_id, valor
                FROM respuestas_evaluacion
                WHERE evaluacion_id = %s
                ORDER BY pregunta_id
            """, (eval["id"],))
            respuestas = cursor.fetchall()
            eval["detalles"] = [
                {
                    "pregunta_id": r["pregunta_id"],
                    "texto": preguntas.get(r["pregunta_id"], f"Pregunta {r['pregunta_id']}"),
                    "valor": r["valor"],
                }
                for r in respuestas
            ]

    except Exception as e:
        flash(f"Error al cargar el historial: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("historial.html", evaluaciones=evaluaciones)


# --------------------------------------------------------
# CONFIGURACION
# --------------------------------------------------------
@app.route("/configuracion")
def configuracion():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("configuracion.html")


# --------------------------------------------------------
# REGISTRO
# --------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        password_plana = request.form["password"]
        codigo_empresa = request.form.get("codigo_empresa", "").strip()
        password_hasheada = generate_password_hash(password_plana)

        db = obtener_conexion()
        if db is None:
            flash("Error crítico: No se pudo conectar a la base de datos.", "error")
            return redirect(url_for("register"))

        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Este email ya está registrado. Por favor, inicia sesión.", "error")
                return redirect(url_for("register"))

            rol_id = 3
            empresa_id = None

            if codigo_empresa:
                cursor.execute(
                    "SELECT id FROM empresas WHERE codigo_registro = %s",
                    (codigo_empresa,),
                )
                empresa = cursor.fetchone()
                if empresa:
                    empresa_id = empresa["id"]
                    rol_id = 4
                else:
                    flash("El código de empresa no es válido.", "error")
                    return redirect(url_for("register"))

            cursor.execute(
                "INSERT INTO usuarios (rol_id, empresa_id, nombre, apellidos, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
                (rol_id, empresa_id, nombre, apellidos, email, password_hasheada),
            )
            db.commit()
            flash("¡Cuenta creada con éxito! Ya puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            if db:
                db.rollback()
            flash(f"Error al crear la cuenta: {e}", "error")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template("register.html")


# --------------------------------------------------------
# TEST
# --------------------------------------------------------
@app.route("/test", methods=["GET"])
def realizar_test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = obtener_conexion()
    preguntas = []
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, texto, dimension_id FROM preguntas WHERE es_activo = 1 ORDER BY id"
        )
        preguntas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al cargar el test: {e}", "error")
        return redirect(url_for("dashboard"))
    finally:
        if "cursor" in locals() and cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("test.html", preguntas=preguntas)


# --------------------------------------------------------
# PROCESAR TEST
# --------------------------------------------------------
@app.route("/procesar_test", methods=["POST"])
def procesar_test():
    if "user_id" not in session:
        flash("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = obtener_conexion()

    if db is None:
        flash("Error de conexión al procesar tu test.", "error")
        return redirect(url_for("realizar_test"))

    try:
        exito, resultado = calcular_y_guardar_bat12(user_id, request.form, db)
        if exito:
            flash(f"Test procesado con éxito! Tu puntuación global es: {resultado}/5", "success")
        else:
            flash(f"Error al procesar: {resultado}", "error")
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "error")
    finally:
        if db:
            db.close()

    return redirect(url_for("dashboard"))


# ================================================
# INICIAR EL SERVIDOR
# ================================================
if __name__ == "__main__":
    app.run(debug=True)