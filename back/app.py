from flask import Flask, render_template, request, redirect, url_for, session, flash
from conexion.conexion_bbdd import obtener_conexion
from servicios.test_service import calcular_y_guardar_bat12
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__) 

# ¡CRÍTICO PARA QUE FUNCIONE SESSION Y FLASH!
app.secret_key = '123123123'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidata = request.form['password']

        db = obtener_conexion()
        # Usamos dictionary=True para que sea más fácil leer las columnas por nombre
        cursor = db.cursor(dictionary=True)

        # Consulta potente: Traemos al usuario y los nombres de su empresa/departamento de una vez
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

        # Validación de la contraseña
        if usuario and check_password_hash(usuario['password'], password_candidata):
            # Guardamos todo en la sesión para que los dashboards no tengan que volver a consultar
            session['user_id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            session['rol'] = usuario['rol_id']
            session['empresa_id'] = usuario['empresa_id']
            session['nombre_empresa'] = usuario['empresa_nombre'] # Será None si es usuario libre
            session['nombre_dept'] = usuario['departamento_nombre'] # Será None si es usuario libre
            
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    rol = session['rol']
    user_id = session['user_id']
    
    # 1. Conectamos a la BD para buscar la última evaluación de este usuario
    db = obtener_conexion()
    ultima_evaluacion = None
    if db:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT puntuacion_total, dim_agotamiento, dim_distanciamiento, dim_cognitivo, dim_emocional, fecha 
            FROM evaluaciones 
            WHERE usuario_id = %s 
            ORDER BY fecha DESC LIMIT 1
        """
        cursor.execute(query, (user_id,))
        ultima_evaluacion = cursor.fetchone()
        cursor.close()
        db.close()
    
    # 2. Renderizamos el dashboard correspondiente pasándole los datos
    if rol == 1: # Admin
        return "<h1>Panel de Control de Administrador</h1>"
    elif rol == 2: # HR
        return render_template('dashboards/hr.html')
    elif rol == 3: # Usuario Personal
        return render_template('dashboards/personal.html', evaluacion=ultima_evaluacion)
    elif rol == 4: # Empleado de Empresa
        return render_template('dashboards/empleado.html', evaluacion=ultima_evaluacion)
    
    else:
        session.clear()
        flash('Error de permisos. Rol no reconocido.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Si el usuario ya está logueado, lo mandamos al dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        password_plana = request.form['password']
        
        #Capturamos el código
        codigo_empresa = request.form.get('codigo_empresa', '').strip()

        # 1. Encriptamos la contraseña inmediatamente
        password_hasheada = generate_password_hash(password_plana)

        db = obtener_conexion()
        if db is None:
            flash('Error crítico: No se pudo conectar a la base de datos.', 'error')
            return redirect(url_for('register'))

        cursor = None
        try:
            cursor = db.cursor(dictionary=True) 
            
            # 2. Verificamos si el email ya existe en la BBDD
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Este email ya está registrado. Por favor, inicia sesión.', 'error')
                return redirect(url_for('register'))

            # --- LÓGICA DE ASIGNACIÓN DE EMPRESA Y ROL ---
            rol_id = 3 # Por defecto: Usuario Personal
            empresa_id = None # Por defecto: Sin empresa

            if codigo_empresa:
                # Buscamos si el código existe en la tabla empresas
                cursor.execute("SELECT id FROM empresas WHERE codigo_registro = %s", (codigo_empresa,))
                empresa = cursor.fetchone()
                
                if empresa:
                    empresa_id = empresa['id']
                    rol_id = 4 # Lo ascendemos a Usuario de Empresa
                else:
                    flash('El código de empresa no es válido.', 'error')
                    return redirect(url_for('register'))

            # 3. Insertamos el nuevo usuario con sus datos dinámicos
            query = """
                INSERT INTO usuarios (rol_id, empresa_id, nombre, apellidos, email, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (rol_id, empresa_id, nombre, apellidos, email, password_hasheada))
            db.commit() 
            
            flash('¡Cuenta creada con éxito! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            if db: db.rollback() 
            flash(f'Error al crear la cuenta: {e}', 'error')
        finally:
            if cursor: cursor.close()
            if db: db.close()

    return render_template('register.html')

@app.route('/test', methods=['GET'])
def realizar_test():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = obtener_conexion()
    preguntas = []
    
    try:
        cursor = db.cursor(dictionary=True)
        # Traemos las 12 preguntas del BAT-12
        cursor.execute("SELECT id, texto, dimension_id FROM preguntas WHERE es_activo = 1 ORDER BY id")
        preguntas = cursor.fetchall()
    except Exception as e:
        flash(f'Error al cargar el test: {e}', 'error')
        return redirect(url_for('dashboard'))
    finally:
        if 'cursor' in locals() and cursor: cursor.close()
        if db: db.close()

    return render_template('test.html', preguntas=preguntas)

@app.route('/procesar_test', methods=['POST'])
def procesar_test():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = obtener_conexion()
    
    if db is None:
        flash('Error de conexión al procesar tu test.', 'error')
        return redirect(url_for('realizar_test'))

    try:
        # Pasamos el form como diccionario (request.form) para que el servicio lo lea
        exito, resultado = calcular_y_guardar_bat12(user_id, request.form, db)

        if exito:
            flash(f'¡Test procesado con éxito! Tu media global de BAT-12 es: {resultado}/5', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(f'Error: {resultado}', 'error')
            return redirect(url_for('realizar_test'))
            
    finally:
        if db: db.close()

if __name__ == '__main__':
    app.run(debug=True)