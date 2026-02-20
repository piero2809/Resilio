USE resilio_db;

-- 1. Gestión de Roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE -- 'admin', 'hr', 'user_personal', 'user_empresa'
);

INSERT INTO roles (nombre) VALUES ('admin'), ('hr'), ('user_personal'), ('user_empresa');

-- 2. Estructura Corporativa (B2B)
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    cif VARCHAR(20) UNIQUE,
    codigo_acceso VARCHAR(50) UNIQUE, -- La clave para que los empleados se vinculen al registrarse
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
);

-- 3. Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    empresa_id INT NULL, -- NULL si es usuario libre
    departamento_id INT NULL, -- NULL si es usuario libre
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE SET NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);

-- 4. Estructura del Test (Neurociencia - Maslach)
CREATE TABLE dimensiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL -- 'Agotamiento', 'Cinismo', 'Eficacia'
);

INSERT INTO dimensiones (nombre) VALUES ('Agotamiento'), ('Cinismo'), ('Eficacia');

CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dimension_id INT NOT NULL,
    texto TEXT NOT NULL,
    FOREIGN KEY (dimension_id) REFERENCES dimensiones(id)
);

-- 5. Resultados e Historial
CREATE TABLE test_intentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    puntos_agotamiento DECIMAL(5,2),
    puntos_cinismo DECIMAL(5,2),
    puntos_eficacia DECIMAL(5,2),
    resultado_final VARCHAR(100), -- 'Bajo', 'Medio', 'Alto Burnout'
    fecha_test TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Para análisis detallado de neurociencia
CREATE TABLE respuestas_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intento_id INT NOT NULL,
    pregunta_id INT NOT NULL,
    valor INT NOT NULL, -- 0 a 6 según escala Maslach
    FOREIGN KEY (intento_id) REFERENCES test_intentos(id) ON DELETE CASCADE,
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id)
);