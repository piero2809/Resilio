"""
RESILIO - Aplicación para Detectar el Burnout
"""

from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), "API-KEY.env"))

import io
import csv
import calendar
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from conexion.conexion_bbdd import obtener_conexion
from servicios.test_service import calcular_y_guardar_bat12
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ─── UTILIDADES ────────────────────────────────────────────────────────────────

def solo_admin(f):
    """Decorador: redirige si el usuario no es admin (rol 1)."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("rol") != 1:
            flash("Acceso restringido a administradores.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

def solo_hr(f):
    """Decorador: restringe acceso a usuarios HR (rol 2)."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("rol") != 2:
            flash("Acceso restringido a usuarios HR.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

def tiempo_relativo(fecha):
    """Devuelve una cadena como 'hace 5 min', 'hace 2h', etc."""
    if not fecha:
        return "—"
    diff = datetime.now() - fecha.replace(tzinfo=None)
    sec = int(diff.total_seconds())
    if sec < 60:
        return "ahora mismo"
    if sec < 3600:
        return f"hace {sec // 60} min"
    if sec < 86400:
        return f"hace {sec // 3600}h"
    return f"hace {sec // 86400}d"


# ─── AUTENTICACIÓN ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_candidata = request.form["password"]

        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, e.nombre AS empresa_nombre, d.nombre AS departamento_nombre
            FROM usuarios u
            LEFT JOIN empresas e ON u.empresa_id = e.id
            LEFT JOIN departamentos d ON u.departamento_id = d.id
            WHERE u.email = %s
        """, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        db.close()

        if usuario and check_password_hash(usuario["password"], password_candidata):
            session["user_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol_id"]
            session["empresa_id"] = usuario["empresa_id"]
            session["departamento_id"] = usuario["departamento_id"]
            session["nombre_empresa"] = usuario["empresa_nombre"]
            session["nombre_dept"] = usuario["departamento_nombre"]
            return redirect(url_for("dashboard"))
        else:
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


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
        if not db:
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
                cursor.execute("SELECT id FROM empresas WHERE codigo_registro = %s", (codigo_empresa,))
                empresa = cursor.fetchone()
                if empresa:
                    empresa_id = empresa["id"]
                    rol_id = 4
                else:
                    flash("El código de empresa no es válido.", "error")
                    return redirect(url_for("register"))

            cursor.execute(
                "INSERT INTO usuarios (rol_id, empresa_id, nombre, apellidos, email, password) VALUES (%s,%s,%s,%s,%s,%s)",
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


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    rol = session["rol"]
    user_id = session["user_id"]

    # ── ADMIN ──────────────────────────────────────────
    if rol == 1:
        db = obtener_conexion()
        if not db:
            flash("Error de conexión.", "error")
            return redirect(url_for("login"))

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS t FROM usuarios")
            total_usuarios = cursor.fetchone()["t"]

            cursor.execute("SELECT COUNT(*) AS t FROM empresas")
            total_empresas = cursor.fetchone()["t"]

            cursor.execute("SELECT COUNT(*) AS t FROM evaluaciones")
            total_evaluaciones = cursor.fetchone()["t"]

            cursor.execute("SELECT COUNT(*) AS t FROM usuarios WHERE MONTH(fecha_registro)=MONTH(NOW()) AND YEAR(fecha_registro)=YEAR(NOW())")
            nuevos_usuarios_mes = cursor.fetchone()["t"]

            cursor.execute("SELECT COUNT(*) AS t FROM evaluaciones WHERE MONTH(fecha)=MONTH(NOW()) AND YEAR(fecha)=YEAR(NOW())")
            evaluaciones_mes = cursor.fetchone()["t"]

            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) AS t FROM (
                    SELECT usuario_id, puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                    FROM evaluaciones
                ) x WHERE rn=1 AND puntuacion_total>=3.5
            """)
            usuarios_riesgo_alto = cursor.fetchone()["t"]
            pct_riesgo_alto = round(usuarios_riesgo_alto / total_usuarios * 100, 1) if total_usuarios else 0

            stats = dict(
                total_usuarios=total_usuarios, total_empresas=total_empresas,
                total_evaluaciones=total_evaluaciones, nuevos_usuarios_mes=nuevos_usuarios_mes,
                evaluaciones_mes=evaluaciones_mes, usuarios_riesgo_alto=usuarios_riesgo_alto,
                pct_riesgo_alto=pct_riesgo_alto,
            )

            cursor.execute("""
                SELECT u.id, u.nombre, u.apellidos, u.email, u.rol_id, u.fecha_registro,
                       e.nombre AS empresa_nombre, COUNT(ev.id) AS total_evaluaciones
                FROM usuarios u
                LEFT JOIN empresas e ON u.empresa_id = e.id
                LEFT JOIN evaluaciones ev ON ev.usuario_id = u.id
                GROUP BY u.id, u.nombre, u.apellidos, u.email, u.rol_id, u.fecha_registro, e.nombre
                ORDER BY u.fecha_registro DESC LIMIT 10
            """)
            usuarios = cursor.fetchall()

            cursor.execute("""
                SELECT e.id, e.nombre, e.sector, e.codigo_registro,
                       COUNT(u.id) AS total_empleados
                FROM empresas e
                LEFT JOIN usuarios u ON u.empresa_id = e.id
                GROUP BY e.id, e.nombre, e.sector, e.codigo_registro
                ORDER BY e.id DESC
            """)
            empresas = cursor.fetchall()

            cursor.execute("""
                SELECT u.nombre, u.apellidos, emp.nombre AS empresa_nombre, t.puntuacion_total AS ultima_puntuacion
                FROM (
                    SELECT usuario_id, puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                    FROM evaluaciones
                ) t
                JOIN usuarios u ON u.id = t.usuario_id
                LEFT JOIN empresas emp ON emp.id = u.empresa_id
                WHERE t.rn=1 AND t.puntuacion_total>=2.5
                ORDER BY t.puntuacion_total DESC LIMIT 8
            """)
            usuarios_riesgo = cursor.fetchall()

            cursor.execute("""
                (SELECT 'registro' AS tipo, u.nombre, u.apellidos, NULL AS puntuacion, u.fecha_registro AS fecha
                 FROM usuarios u ORDER BY fecha_registro DESC LIMIT 5)
                UNION ALL
                (SELECT 'evaluacion', u.nombre, u.apellidos, ev.puntuacion_total, ev.fecha
                 FROM evaluaciones ev JOIN usuarios u ON u.id=ev.usuario_id ORDER BY ev.fecha DESC LIMIT 5)
                ORDER BY fecha DESC LIMIT 8
            """)
            actividad = []
            for item in cursor.fetchall():
                if item["tipo"] == "registro":
                    actividad.append(dict(
                        titulo="Nuevo usuario registrado",
                        descripcion=f"{item['nombre']} {item['apellidos'] or ''}".strip(),
                        tiempo=tiempo_relativo(item["fecha"]),
                        icon="user-plus", color="green",
                    ))
                else:
                    p = float(item["puntuacion"]) if item["puntuacion"] else 0
                    actividad.append(dict(
                        titulo="Evaluación completada",
                        descripcion=f"{item['nombre']} — {p:.2f}/5",
                        tiempo=tiempo_relativo(item["fecha"]),
                        icon="clipboard-check",
                        color="red" if p >= 3.5 else ("yellow" if p >= 2.5 else "green"),
                    ))

            cursor.execute("""
                SELECT DATE_FORMAT(fecha,'%b %Y') AS mes, COUNT(*) AS total,
                       SUM(CASE WHEN puntuacion_total>=3.5 THEN 1 ELSE 0 END) AS riesgo_alto
                FROM evaluaciones
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(fecha,'%Y-%m'), DATE_FORMAT(fecha,'%b %Y')
                ORDER BY MIN(fecha) ASC
            """)
            tendencia_mensual = [{"mes": r["mes"], "total": int(r["total"]), "riesgo_alto": int(r["riesgo_alto"])} for r in cursor.fetchall()]

            if not tendencia_mensual:
                today = date.today()
                for i in range(5, -1, -1):
                    m = today.month - i
                    y = today.year
                    while m <= 0:
                        m += 12
                        y -= 1
                    tendencia_mensual.append({"mes": f"{calendar.month_abbr[m]} {y}", "total": 0, "riesgo_alto": 0})

        except Exception as e:
            flash(f"Error al cargar el panel: {e}", "error")
            stats = {k: 0 for k in ["total_usuarios","total_empresas","total_evaluaciones","nuevos_usuarios_mes","evaluaciones_mes","usuarios_riesgo_alto","pct_riesgo_alto"]}
            usuarios = empresas = usuarios_riesgo = actividad = tendencia_mensual = []
        finally:
            cursor.close()
            db.close()

        return render_template(
            "dashboards/admin.html",
            stats=stats, usuarios=usuarios, empresas=empresas,
            usuarios_riesgo=usuarios_riesgo, actividad=actividad,
            tendencia_mensual=tendencia_mensual
        )

    # ── HR ─────────────────────────────────────────────
    elif rol == 2:
        empresa_id = session.get("empresa_id")

        if not empresa_id:
            flash("Tu usuario HR no tiene una empresa asignada.", "error")
            return redirect(url_for("logout"))

        db = obtener_conexion()
        if not db:
            flash("Error de conexión.", "error")
            return redirect(url_for("login"))

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT COUNT(*) AS t
                FROM usuarios
                WHERE empresa_id = %s AND rol_id = 4
            """, (empresa_id,))
            total_empleados = cursor.fetchone()["t"]

            cursor.execute("""
                SELECT COUNT(ev.id) AS t
                FROM evaluaciones ev
                JOIN usuarios u ON u.id = ev.usuario_id
                WHERE u.empresa_id = %s AND u.rol_id = 4
            """, (empresa_id,))
            total_evaluaciones = cursor.fetchone()["t"]

            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) AS t
                FROM (
                    SELECT ev.usuario_id, ev.puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY ev.usuario_id ORDER BY ev.fecha DESC) AS rn
                    FROM evaluaciones ev
                    JOIN usuarios u ON u.id = ev.usuario_id
                    WHERE u.empresa_id = %s AND u.rol_id = 4
                ) x
                WHERE rn = 1 AND puntuacion_total >= 3.5
            """, (empresa_id,))
            empleados_riesgo_alto = cursor.fetchone()["t"]
            pct_riesgo_alto = round((empleados_riesgo_alto / total_empleados) * 100, 1) if total_empleados else 0

            stats = dict(
                total_empleados=total_empleados,
                total_evaluaciones=total_evaluaciones,
                empleados_riesgo_alto=empleados_riesgo_alto,
                pct_riesgo_alto=pct_riesgo_alto
            )

            cursor.execute("""
                SELECT
                    ROUND(AVG(ev.puntuacion_total), 2) AS media_global,
                    ROUND(AVG(ev.dim_agotamiento), 2) AS agotamiento,
                    ROUND(AVG(ev.dim_distanciamiento), 2) AS distanciamiento,
                    ROUND(AVG(ev.dim_cognitivo), 2) AS cognitivo,
                    ROUND(AVG(ev.dim_emocional), 2) AS emocional
                FROM evaluaciones ev
                JOIN usuarios u ON u.id = ev.usuario_id
                WHERE u.empresa_id = %s AND u.rol_id = 4
            """, (empresa_id,))
            medias = cursor.fetchone()

            cursor.execute("""
                SELECT
                    SUM(CASE WHEN t.puntuacion_total < 2.5 THEN 1 ELSE 0 END) AS bajo,
                    SUM(CASE WHEN t.puntuacion_total >= 2.5 AND t.puntuacion_total < 3.5 THEN 1 ELSE 0 END) AS medio,
                    SUM(CASE WHEN t.puntuacion_total >= 3.5 THEN 1 ELSE 0 END) AS alto
                FROM (
                    SELECT ev.usuario_id, ev.puntuacion_total,
                           ROW_NUMBER() OVER (PARTITION BY ev.usuario_id ORDER BY ev.fecha DESC) AS rn
                    FROM evaluaciones ev
                    JOIN usuarios u ON u.id = ev.usuario_id
                    WHERE u.empresa_id = %s AND u.rol_id = 4
                ) t
                WHERE t.rn = 1
            """, (empresa_id,))
            riesgo = cursor.fetchone()

            cursor.execute("""
                SELECT
                    COALESCE(d.nombre, 'Sin departamento') AS departamento,
                    COUNT(DISTINCT u.id) AS empleados,
                    COUNT(ev.id) AS evaluaciones,
                    ROUND(AVG(ev.puntuacion_total), 2) AS media_global
                FROM usuarios u
                LEFT JOIN departamentos d ON d.id = u.departamento_id
                LEFT JOIN evaluaciones ev ON ev.usuario_id = u.id
                WHERE u.empresa_id = %s AND u.rol_id = 4
                GROUP BY d.id, d.nombre
                ORDER BY media_global DESC
            """, (empresa_id,))
            departamentos = cursor.fetchall()

            cursor.execute("""
                SELECT DATE_FORMAT(ev.fecha,'%b %Y') AS mes,
                       COUNT(*) AS total,
                       SUM(CASE WHEN ev.puntuacion_total >= 3.5 THEN 1 ELSE 0 END) AS riesgo_alto
                FROM evaluaciones ev
                JOIN usuarios u ON u.id = ev.usuario_id
                WHERE u.empresa_id = %s
                  AND u.rol_id = 4
                  AND ev.fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(ev.fecha,'%Y-%m'), DATE_FORMAT(ev.fecha,'%b %Y')
                ORDER BY MIN(ev.fecha) ASC
            """, (empresa_id,))
            tendencia_mensual = [{"mes": r["mes"], "total": int(r["total"]), "riesgo_alto": int(r["riesgo_alto"])} for r in cursor.fetchall()]

            if not tendencia_mensual:
                today = date.today()
                for i in range(5, -1, -1):
                    m = today.month - i
                    y = today.year
                    while m <= 0:
                        m += 12
                        y -= 1
                    tendencia_mensual.append({"mes": f"{calendar.month_abbr[m]} {y}", "total": 0, "riesgo_alto": 0})

            cursor.execute("""
                SELECT
                    DATE_FORMAT(MAX(ev.fecha), '%d/%m/%Y') AS fecha,
                    CONCAT('Empleado ', LPAD(
                        ROW_NUMBER() OVER (ORDER BY MAX(ev.fecha) DESC, u.id ASC), 2, '0'
                    )) AS alias,
                    ROUND(MAX(CASE
                        WHEN ev.fecha = ult.ultima_fecha THEN ev.puntuacion_total
                        ELSE NULL
                    END), 2) AS puntuacion_total
                FROM usuarios u
                JOIN (
                    SELECT ev.usuario_id, MAX(ev.fecha) AS ultima_fecha
                    FROM evaluaciones ev
                    JOIN usuarios ux ON ux.id = ev.usuario_id
                    WHERE ux.empresa_id = %s AND ux.rol_id = 4
                    GROUP BY ev.usuario_id
                ) ult ON ult.usuario_id = u.id
                JOIN evaluaciones ev ON ev.usuario_id = u.id
                WHERE u.empresa_id = %s AND u.rol_id = 4
                GROUP BY u.id
                ORDER BY ult.ultima_fecha DESC
                LIMIT 10
            """, (empresa_id, empresa_id))
            evaluaciones_recientes = cursor.fetchall()

        except Exception as e:
            flash(f"Error al cargar el panel HR: {e}", "error")
            stats = dict(total_empleados=0, total_evaluaciones=0, empleados_riesgo_alto=0, pct_riesgo_alto=0)
            medias = dict(media_global=0, agotamiento=0, distanciamiento=0, cognitivo=0, emocional=0)
            riesgo = dict(bajo=0, medio=0, alto=0)
            departamentos = []
            tendencia_mensual = []
            evaluaciones_recientes = []
        finally:
            cursor.close()
            db.close()

        return render_template(
            "dashboards/hr.html",
            stats=stats,
            medias=medias,
            riesgo=riesgo,
            departamentos=departamentos,
            tendencia_mensual=tendencia_mensual,
            evaluaciones_recientes=evaluaciones_recientes
        )

    # ── PERSONAL / EMPRESA ─────────────────────────────
    else:
        db = obtener_conexion()
        ultima_evaluacion = None
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT puntuacion_total, dim_agotamiento, dim_distanciamiento,
                       dim_cognitivo, dim_emocional, fecha, consejos
                FROM evaluaciones WHERE usuario_id=%s ORDER BY fecha DESC LIMIT 1
            """, (user_id,))
            ultima_evaluacion = cursor.fetchone()
            cursor.close()
            db.close()
        template = "dashboards/personal.html" if rol == 3 else "dashboards/empleado.html"
        return render_template(template, evaluacion=ultima_evaluacion)


# ─── ADMIN: NUEVA EMPRESA ──────────────────────────────────────────────────────

@app.route("/admin/nueva_empresa", methods=["POST"])
@solo_admin
def nueva_empresa():
    nombre = request.form.get("nombre", "").strip()
    sector = request.form.get("sector", "").strip()
    codigo = request.form.get("codigo_registro", "").strip()

    if not nombre or not codigo:
        flash("El nombre y el código de registro son obligatorios.", "error")
        return redirect(url_for("dashboard"))

    db = obtener_conexion()
    if not db:
        flash("Error de conexión.", "error")
        return redirect(url_for("dashboard"))

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM empresas WHERE codigo_registro = %s", (codigo,))
        if cursor.fetchone():
            flash(f"El código '{codigo}' ya está en uso. Elige otro.", "error")
            return redirect(url_for("dashboard"))

        cursor.execute(
            "INSERT INTO empresas (nombre, sector, codigo_registro) VALUES (%s, %s, %s)",
            (nombre, sector or None, codigo),
        )
        db.commit()
        flash(f"✓ Empresa '{nombre}' creada con código {codigo}.", "success")
    except Exception as e:
        if db:
            db.rollback()
        flash(f"Error al crear empresa: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for("dashboard"))


# ─── ADMIN: NUEVO USUARIO ──────────────────────────────────────────────────────

@app.route("/admin/nuevo_usuario", methods=["POST"])
@solo_admin
def nuevo_usuario():
    nombre = request.form.get("nombre", "").strip()
    apellidos = request.form.get("apellidos", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    rol_id = int(request.form.get("rol_id", 3))
    empresa_id = request.form.get("empresa_id") or None
    departamento_id = request.form.get("departamento_id") or None

    if empresa_id:
        empresa_id = int(empresa_id)
    if departamento_id:
        departamento_id = int(departamento_id)

    if not nombre or not email or not password:
        flash("Nombre, email y contraseña son obligatorios.", "error")
        return redirect(url_for("dashboard"))

    db = obtener_conexion()
    if not db:
        flash("Error de conexión.", "error")
        return redirect(url_for("dashboard"))

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash(f"El email '{email}' ya está registrado.", "error")
            return redirect(url_for("dashboard"))

        cursor.execute(
            """
            INSERT INTO usuarios (rol_id, empresa_id, departamento_id, nombre, apellidos, email, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (rol_id, empresa_id, departamento_id, nombre, apellidos or None, email, generate_password_hash(password)),
        )
        db.commit()
        flash(f"✓ Usuario '{nombre}' creado correctamente.", "success")
    except Exception as e:
        if db:
            db.rollback()
        flash(f"Error al crear usuario: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for("dashboard"))


# ─── ADMIN: EXPORTAR CSV ───────────────────────────────────────────────────────

@app.route("/admin/exportar_csv")
@solo_admin
def exportar_csv():
    db = obtener_conexion()
    if not db:
        flash("Error de conexión.", "error")
        return redirect(url_for("dashboard"))

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                ev.id AS evaluacion_id,
                ev.fecha,
                u.nombre, u.apellidos, u.email,
                r.nombre AS rol,
                COALESCE(e.nombre, 'Personal') AS empresa,
                COALESCE(d.nombre, '—') AS departamento,
                ev.puntuacion_total,
                ev.dim_agotamiento,
                ev.dim_distanciamiento,
                ev.dim_cognitivo,
                ev.dim_emocional,
                CASE
                    WHEN ev.puntuacion_total >= 3.5 THEN 'Alto'
                    WHEN ev.puntuacion_total >= 2.5 THEN 'Medio'
                    ELSE 'Bajo'
                END AS nivel_riesgo
            FROM evaluaciones ev
            JOIN usuarios u ON u.id = ev.usuario_id
            JOIN roles r ON r.id = u.rol_id
            LEFT JOIN empresas e ON e.id = u.empresa_id
            LEFT JOIN departamentos d ON d.id = u.departamento_id
            ORDER BY ev.fecha DESC
        """)
        rows = cursor.fetchall()
    except Exception as e:
        flash(f"Error al generar CSV: {e}", "error")
        return redirect(url_for("dashboard"))
    finally:
        cursor.close()
        db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID Evaluación", "Fecha", "Nombre", "Apellidos", "Email",
        "Rol", "Empresa", "Departamento",
        "Puntuación Total", "Agotamiento", "Distanciamiento",
        "Deterioro Cognitivo", "Deterioro Emocional", "Nivel de Riesgo"
    ])
    for r in rows:
        writer.writerow([
            r["evaluacion_id"],
            r["fecha"].strftime("%d/%m/%Y %H:%M") if r["fecha"] else "",
            r["nombre"], r["apellidos"] or "",
            r["email"], r["rol"], r["empresa"], r["departamento"],
            r["puntuacion_total"], r["dim_agotamiento"],
            r["dim_distanciamiento"], r["dim_cognitivo"],
            r["dim_emocional"], r["nivel_riesgo"],
        ])

    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=resilio_evaluaciones_{fecha_str}.csv"},
    )


# ─── ADMIN: INFORME GLOBAL ─────────────────────────────────────────────────────

@app.route("/admin/informe_global")
@solo_admin
def informe_global():
    db = obtener_conexion()
    if not db:
        flash("Error de conexión.", "error")
        return redirect(url_for("dashboard"))

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS t FROM usuarios")
        total_usuarios = cursor.fetchone()["t"]
        cursor.execute("SELECT COUNT(*) AS t FROM evaluaciones")
        total_evaluaciones = cursor.fetchone()["t"]
        stats = dict(total_usuarios=total_usuarios, total_evaluaciones=total_evaluaciones)

        cursor.execute("""
            SELECT
                SUM(CASE WHEN puntuacion_total < 2.5 THEN 1 ELSE 0 END) AS bajo,
                SUM(CASE WHEN puntuacion_total >= 2.5 AND puntuacion_total < 3.5 THEN 1 ELSE 0 END) AS medio,
                SUM(CASE WHEN puntuacion_total >= 3.5 THEN 1 ELSE 0 END) AS alto
            FROM (
                SELECT usuario_id, puntuacion_total,
                       ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                FROM evaluaciones
            ) x WHERE rn=1
        """)
        riesgo_row = cursor.fetchone()
        riesgo = dict(
            bajo=int(riesgo_row["bajo"] or 0),
            medio=int(riesgo_row["medio"] or 0),
            alto=int(riesgo_row["alto"] or 0),
        )

        cursor.execute("""
            SELECT
                ROUND(AVG(dim_agotamiento), 2) AS agotamiento,
                ROUND(AVG(dim_distanciamiento), 2) AS distanciamiento,
                ROUND(AVG(dim_cognitivo), 2) AS cognitivo,
                ROUND(AVG(dim_emocional), 2) AS emocional,
                ROUND(AVG(puntuacion_total), 2) AS global
            FROM evaluaciones
        """)
        medias_row = cursor.fetchone()
        medias = {k: float(v) if v else 0 for k, v in medias_row.items()} if medias_row["global"] else None

        cursor.execute("""
            SELECT e.nombre,
                   COUNT(DISTINCT u.id) AS empleados,
                   COUNT(ev.id) AS evaluaciones,
                   ROUND(AVG(ev.puntuacion_total), 2) AS media_global,
                   ROUND(AVG(ev.dim_agotamiento), 2) AS media_agotamiento
            FROM empresas e
            LEFT JOIN usuarios u ON u.empresa_id = e.id
            LEFT JOIN evaluaciones ev ON ev.usuario_id = u.id
            GROUP BY e.id, e.nombre
            ORDER BY media_global DESC
        """)
        empresas_stats = []
        for r in cursor.fetchall():
            empresas_stats.append({
                "nombre": r["nombre"],
                "empleados": r["empleados"],
                "evaluaciones": r["evaluaciones"],
                "media_global": float(r["media_global"]) if r["media_global"] else None,
                "media_agotamiento": float(r["media_agotamiento"]) if r["media_agotamiento"] else None,
            })

        cursor.execute("""
            SELECT u.nombre, u.apellidos, emp.nombre AS empresa_nombre, t.puntuacion_total
            FROM (
                SELECT usuario_id, puntuacion_total,
                       ROW_NUMBER() OVER (PARTITION BY usuario_id ORDER BY fecha DESC) AS rn
                FROM evaluaciones
            ) t
            JOIN usuarios u ON u.id = t.usuario_id
            LEFT JOIN empresas emp ON emp.id = u.empresa_id
            WHERE t.rn=1
            ORDER BY t.puntuacion_total DESC LIMIT 10
        """)
        top_riesgo = cursor.fetchall()

        cursor.execute("""
            SELECT DATE_FORMAT(fecha,'%b %Y') AS mes,
                   ROUND(AVG(puntuacion_total), 2) AS media
            FROM evaluaciones
            WHERE fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha,'%Y-%m'), DATE_FORMAT(fecha,'%b %Y')
            ORDER BY MIN(fecha) ASC
        """)
        evolucion_mensual = [{"mes": r["mes"], "media": float(r["media"])} for r in cursor.fetchall()]
        if not evolucion_mensual:
            today = date.today()
            for i in range(5, -1, -1):
                m = today.month - i
                y = today.year
                while m <= 0:
                    m += 12
                    y -= 1
                evolucion_mensual.append({"mes": f"{calendar.month_abbr[m]} {y}", "media": 0})

    except Exception as e:
        flash(f"Error al generar el informe: {e}", "error")
        stats = riesgo = medias = empresas_stats = top_riesgo = evolucion_mensual = None
        riesgo = dict(bajo=0, medio=0, alto=0)
        empresas_stats = top_riesgo = evolucion_mensual = []
    finally:
        cursor.close()
        db.close()

    return render_template(
        "dashboards/informe_global.html",
        stats=stats, riesgo=riesgo, medias=medias,
        empresas_stats=empresas_stats, top_riesgo=top_riesgo,
        evolucion_mensual=evolucion_mensual
    )


# ─── HISTORIAL ─────────────────────────────────────────────────────────────────

@app.route("/historial")
def historial():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = obtener_conexion()
    evaluaciones = []
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, puntuacion_total, dim_agotamiento, dim_distanciamiento,
                   dim_cognitivo, dim_emocional, fecha, consejos
            FROM evaluaciones WHERE usuario_id=%s ORDER BY fecha DESC
        """, (user_id,))
        evaluaciones = cursor.fetchall()

        cursor.execute("SELECT id, texto FROM preguntas WHERE es_activo=1 ORDER BY id")
        preguntas = {f["id"]: f["texto"] for f in cursor.fetchall()}

        for ev in evaluaciones:
            cursor.execute("SELECT pregunta_id, valor FROM respuestas_evaluacion WHERE evaluacion_id=%s ORDER BY pregunta_id", (ev["id"],))
            ev["detalles"] = [{"pregunta_id": r["pregunta_id"], "texto": preguntas.get(r["pregunta_id"], f"Pregunta {r['pregunta_id']}"), "valor": r["valor"]} for r in cursor.fetchall()]
    except Exception as e:
        flash(f"Error al cargar el historial: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("historial.html", evaluaciones=evaluaciones)


# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────

@app.route("/configuracion")
def configuracion():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("configuracion.html")


# ─── TEST ──────────────────────────────────────────────────────────────────────

@app.route("/test", methods=["GET"])
def realizar_test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = obtener_conexion()
    preguntas = []
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, texto, dimension_id FROM preguntas WHERE es_activo=1 ORDER BY id")
        preguntas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al cargar el test: {e}", "error")
        return redirect(url_for("dashboard"))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("test.html", preguntas=preguntas)


@app.route("/procesar_test", methods=["POST"])
def procesar_test():
    if "user_id" not in session:
        flash("Tu sesión ha expirado.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = obtener_conexion()
    if not db:
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


# ─── INICIO ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug)