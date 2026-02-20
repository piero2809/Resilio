from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from conexion.conexion_bbdd import obtener_conexion

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

        # Validación Crítica
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
    
    # Aquí es donde ocurre la magia de los dashboards que mencionaste
    rol = session['rol']
    
    if rol == 2: # HR
        return render_template('dashboards/hr.html')
    elif rol == 4: # Trabajador Empresa
        return render_template('dashboards/empleado.html')
    else: # Usuario Libre (Rol 3)
        return render_template('dashboards/personal.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)