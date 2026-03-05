"""
=================================================
RESILIO - Aplicación para Detectar el Burnout
=================================================

Este es el archivo principal de la aplicación Flask.
Aquí definimos todas las rutas (páginas) de nuestra web.

¿CÓMO FUNCIONA ESTE CÓDIGO?
-----------------------------
Flask es un framework web (como una biblioteca grande) que nos ayuda a crear páginas web.
Cada @app.route("/ruta") es como decir "cuando alguien visite esta dirección, haz esto".

Por ejemplo:
- @app.route("/login") → cuando alguien va a "localhost:5000/login"
- return render_template("login.html") → Flask busca el archivo login.html en la carpeta templates

"""

# ================================================
# IMPORTAR LIBRERÍAS (Heramientas que vamos a usar)
# ================================================

# Flask: el framework principal para crear la web
from flask import Flask, render_template, request, redirect, url_for, session, flash

# Nuestra función para conectar con la base de datos MySQL
from conexion.conexion_bbdd import obtener_conexion

# Función especial que calcula el resultado del test BAT-12
from servicios.test_service import calcular_y_guardar_bat12

# Herramientas de seguridad para guardar contraseñas de forma segura
# (nunca guardamos contraseñas texto plano, siempre encriptadas)
from werkzeug.security import check_password_hash, generate_password_hash


# ================================================
# CONFIGURACIÓN INICIAL DE FLASK
# ================================================

# Creamos la aplicación Flask
# __name__ es una variable especial de Python que indica el nombre del archivo
app = Flask(__name__)

# La secret_key es CRÍTICA para usar sesiones y mensajes flash
# Piensa en ella como una contraseña interna de la aplicación
# IMPORTANTE: En producción, esto debería ser una clave aleatoria compleja
app.secret_key = "123123123"


# ================================================
# RUTAS DE LA APLICACIÓN
# ================================================


# --------------------------------------------------------
# RUTA PRINCIPAL (/)
# Redirige directamente al login
# --------------------------------------------------------
@app.route("/")
def index():
    # redirect() envía al navegador a otra página
    # url_for("login") genera la URL correcta para la función login()
    return redirect(url_for("login"))


# --------------------------------------------------------
# RUTA DE LOGIN (/login)
# Muestra el formulario de inicio de sesión
# --------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Esta ruta funciona de dos formas:
    - GET: Cuando el usuario escribe la URL o llega por primera vez
    - POST: Cuando el usuario envía el formulario

    request.method nos dice qué tipo de petición llegó
    """

    # Si es POST, el usuario envió el formulario de login
    if request.method == "POST":
        # request.form es un diccionario con todos los datos del formulario
        # Obtenemos el email y contraseña que escribió el usuario
        email = request.form["email"]
        password_candidata = request.form["password"]

        # ----- CONEXIÓN A LA BASE DE DATOS -----
        db = obtener_conexion()  # Intentamos conectar a MySQL

        # Creamos un "cursor" que es como un puntero para ejecutar consultas SQL
        # dictionary=True hace que los resultados vengan como diccionarios {columna: valor}
        cursor = db.cursor(dictionary=True)

        # ----- CONSULTA SQL -----
        # Esta consulta hace varias cosas a la vez:
        # 1. SELECT u.* → selecciona todas las columnas del usuario
        # 2. LEFT JOIN empresas → añade el nombre de la empresa (si existe)
        # 3. LEFT JOIN departamentos → añade el nombre del departamento (si existe)
        # 4. WHERE u.email = %s → busca por el email que nos pasaron
        query = """
            SELECT u.*, e.nombre AS empresa_nombre, d.nombre AS departamento_nombre
            FROM usuarios u
            LEFT JOIN empresas e ON u.empresa_id = e.id
            LEFT JOIN departamentos d ON u.departamento_id = d.id
            WHERE u.email = %s
        """

        # execute() ejecuta la consulta SQL
        # El segundo argumento (%) es una tupla con los valores que reemplazan las %
        # Esto protege contra SQL Injection (ataques de hackers)
        cursor.execute(query, (email,))

        # fetchone() obtiene una sola fila (el usuario encontrado)
        usuario = cursor.fetchone()

        # Cerramos la conexión (siempre hay que cerrar para liberar recursos)
        cursor.close()
        db.close()

        # ----- VALIDACIÓN DE CONTRASEÑA -----
        # check_password_hash() compara la contraseña escrita con el hash guardado
        # Si coinciden y el usuario existe, el login es exitoso
        if usuario and check_password_hash(usuario["password"], password_candidata):
            # ----- GUARDAR SESIÓN -----
            # La sesión es como una memoria temporal del navegador
            # Guardamos datos del usuario para usarlos en otras páginas
            # Esto nos permite saber quién está logueado
            session["user_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol_id"]
            session["empresa_id"] = usuario["empresa_id"]
            session["nombre_empresa"] = usuario["empresa_nombre"]  # Puede ser None
            session["nombre_dept"] = usuario["departamento_nombre"]  # Puede ser None

            # Redirigimos al dashboard
            return redirect(url_for("dashboard"))

        else:
            # Login fallido: mostrar mensaje de error
            # flash() guarda un mensaje para mostrarlo en la siguiente página
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for("login"))

    # Si es GET, simplemente mostramos el formulario de login
    return render_template("login.html")


# --------------------------------------------------------
# RUTA DEL DASHBOARD (/dashboard)
# Muestra diferentes paneles según el rol del usuario
# --------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    """
    El dashboard es diferente para cada tipo de usuario:
    - Admin (rol 1): Panel de administración
    - HR (rol 2): Panel de recursos humanos
    - Usuario Personal (rol 3): Panel individual
    - Empleado Empresa (rol 4): Panel de empleado
    """

    # ----- PROTECCIÓN DE RUTA -----
    # Si no hay user_id en la sesión, el usuario no ha hecho login
    # Lo mandamos al login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Obtenemos el rol y ID del usuario de la sesión
    rol = session["rol"]
    user_id = session["user_id"]

    # ----- OBTENER EVALUACIÓN DEL USUARIO -----
    # Buscamos la última evaluación (test) que ha hecho el usuario
    db = obtener_conexion()
    ultima_evaluacion = None

    if db:
        cursor = db.cursor(dictionary=True)

        # Esta consulta obtiene la última evaluación del usuario
        # ORDER BY fecha DESC → ordena por fecha, la más reciente primero
        # LIMIT 1 → solo cogemos la primera (la más reciente)
        query = """
            SELECT puntuacion_total, dim_agotamiento, dim_distanciamiento, 
                   dim_cognitivo, dim_emocional, fecha 
            FROM evaluaciones 
            WHERE usuario_id = %s 
            ORDER BY fecha DESC LIMIT 1
        """
        cursor.execute(query, (user_id,))
        ultima_evaluacion = cursor.fetchone()

        cursor.close()
        db.close()

    # ----- RENDERIZAR SEGÚN EL ROL -----
    # render_template() busca el archivo HTML en la carpeta templates
    # Le pasamos "evaluacion" para que el HTML pueda mostrar los datos

    if rol == 1:  # Administrador
        return render_template("dashboards/admin.html")

    elif rol == 2:  # Recursos Humanos
        return render_template("dashboards/hr.html")

    elif rol == 3:  # Usuario Personal
        return render_template("dashboards/personal.html", evaluacion=ultima_evaluacion)

    elif rol == 4:  # Empleado de Empresa
        return render_template("dashboards/empleado.html", evaluacion=ultima_evaluacion)

    else:
        # Si el rol no es válido, cerramos sesión y avisamos
        session.clear()
        flash("Error de permisos. Rol no reconocido.", "error")
        return redirect(url_for("login"))


# --------------------------------------------------------
# RUTA DE LOGOUT (/logout)
# Cierra la sesión del usuario
# --------------------------------------------------------
@app.route("/logout")
def logout():
    """
    Cerrar sesión es muy simple:
    - session.clear() borra todos los datos de la sesión
    - Redirect al login
    """
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------------------
# RUTA DE REGISTRO (/register)
# Permite crear una cuenta nueva
# --------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    El registro tiene lógica especial para empresas:
    - Sin código de empresa → rol 3 (Usuario Personal)
    - Con código válido → rol 4 (Empleado de Empresa)
    """

    # Si ya está logueado, no puede registrarse de nuevo
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    # Si el usuario envió el formulario (POST)
    if request.method == "POST":
        # Obtenemos todos los datos del formulario
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        password_plana = request.form["password"]  # Contraseña sin encriptar

        # Obtenemos el código de empresa (si lo hay)
        # .get() devuelve "" si no existe el campo, y .trim() elimina espacios
        codigo_empresa = request.form.get("codigo_empresa", "").strip()

        # ----- ENCRIPTAR CONTRASEÑA -----
        # generate_password_hash() transforma la contraseña en una cadena ilegible
        # Esto es MUY IMPORTANTE por seguridad
        password_hasheada = generate_password_hash(password_plana)

        # ----- CONEXIÓN A LA BASE DE DATOS -----
        db = obtener_conexion()

        if db is None:
            flash("Error crítico: No se pudo conectar a la base de datos.", "error")
            return redirect(url_for("register"))

        cursor = None
        try:
            cursor = db.cursor(dictionary=True)

            # ----- VERIFICAR SI EL EMAIL YA EXISTE -----
            # Si el email ya está en la base de datos, no dejamos registrar
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash(
                    "Este email ya está registrado. Por favor, inicia sesión.", "error"
                )
                return redirect(url_for("register"))

            # ----- LÓGICA DE ROL Y EMPRESA -----
            # Por defecto: usuario personal sin empresa
            rol_id = 3
            empresa_id = None

            # Si el usuario introdujo un código de empresa
            if codigo_empresa:
                # Buscamos si el código existe en la tabla empresas
                cursor.execute(
                    "SELECT id FROM empresas WHERE codigo_registro = %s",
                    (codigo_empresa,),
                )
                empresa = cursor.fetchone()

                # Si encontramos la empresa con ese código
                if empresa:
                    empresa_id = empresa["id"]
                    rol_id = 4  # Cambiamos a empleado de empresa
                else:
                    flash("El código de empresa no es válido.", "error")
                    return redirect(url_for("register"))

            # ----- INSERTAR EL NUEVO USUARIO -----
            query = """
                INSERT INTO usuarios (rol_id, empresa_id, nombre, apellidos, email, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query, (rol_id, empresa_id, nombre, apellidos, email, password_hasheada)
            )

            # commit() guarda los cambios en la base de datos
            # Sin esto, los cambios no se aplican
            db.commit()

            flash("¡Cuenta creada con éxito! Ya puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            # Si hay cualquier error, deshacemos los cambios
            if db:
                db.rollback()
            flash(f"Error al crear la cuenta: {e}", "error")

        finally:
            # Siempre cerramos cursor y conexión, aunque haya errores
            if cursor:
                cursor.close()
            if db:
                db.close()

    # Si es GET, mostrar el formulario de registro
    return render_template("register.html")


# --------------------------------------------------------
# RUTA DEL TEST (/test)
# Muestra el cuestionario BAT-12
# --------------------------------------------------------
@app.route("/test", methods=["GET"])
def realizar_test():
    """
    Esta ruta carga las preguntas de la base de datos
    y las pasa al template test.html para mostrarlas
    """

    # Solo usuarios logueados pueden hacer el test
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = obtener_conexion()
    preguntas = []

    try:
        cursor = db.cursor(dictionary=True)

        # Obtenemos las preguntas activas ordenadas por ID
        # es_activo = 1 significa que la pregunta está habilitada
        cursor.execute(
            "SELECT id, texto, dimension_id FROM preguntas WHERE es_activo = 1 ORDER BY id"
        )

        # fetchall() devuelve todas las filas como una lista
        preguntas = cursor.fetchall()

    except Exception as e:
        flash(f"Error al cargar el test: {e}", "error")
        return redirect(url_for("dashboard"))

    finally:
        # Cerrar conexiones
        if "cursor" in locals() and cursor:
            cursor.close()
        if db:
            db.close()

    # Renderizamos el test pasándole las preguntas
    return render_template("test.html", preguntas=preguntas)


# --------------------------------------------------------
# RUTA PARA PROCESAR EL TEST (/procesar_test)
# Calcula el resultado y lo guarda en la base de datos
# --------------------------------------------------------
@app.route("/procesar_test", methods=["POST"])
def procesar_test():
    """
    Aquí llegan las respuestas del formulario del test
    Las pasamos a la función calcular_y_guardar_bat12()
    que hace todos los cálculos y guarda el resultado
    """

    # Solo usuarios logueados
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Obtenemos el ID del usuario de la sesión
    user_id = session["user_id"]
    db = obtener_conexion()

    if db is None:
        flash("Error de conexión al procesar tu test.", "error")
        return redirect(url_for("realizar_test"))

    try:
        # ----- PROCESAR LAS RESPUESTAS -----
        # request.form contiene todas las respuestas como: {pregunta_1: "3", pregunta_2: "2", ...}
        # Llamamos a la función del servicio que hace todo el trabajo pesado
        exito, resultado = calcular_y_guardar_bat12(user_id, request.form, db)

        if exito:
            # Si todo fue bien, mostrar resultado
            flash(
                f"¡Test procesado con éxito! Tu media global de BAT-12 es: {resultado}/5",
                "success",
            )
            return redirect(url_for("dashboard"))
        else:
            # Si hubo error en el procesamiento
            flash(f"Error: {resultado}", "error")
            return redirect(url_for("realizar_test"))

    finally:
        # Cerrar conexión
        if db:
            db.close()


# ================================================
# INICIAR EL SERVIDOR
# ================================================

# Este bloque solo se ejecuta si ejecutamos este archivo directamente
# (no cuando se importa desde otro archivo)
if __name__ == "__main__":
    # app.run() inicia el servidor web de desarrollo
    # debug=True permite ver errores y recargar automáticamente
    app.run(debug=True)
