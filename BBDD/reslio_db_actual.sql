-- 1. LA OPCIÓN NUCLEAR: Destruimos la base de datos vieja y empezamos limpios
DROP DATABASE IF EXISTS resilio_db;
CREATE DATABASE resilio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE resilio_db;

-- ==========================================
-- ESTRUCTURA DEL SISTEMA (B2B SaaS)
-- ==========================================

-- Tabla de Roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Roles exactos para tu app Flask
INSERT INTO roles (id, nombre) VALUES 
(1, 'admin'), 
(2, 'hr'), 
(3, 'user_personal'), 
(4, 'user_empresa');

-- Tabla de Empresas (Con el código de registro para Arquitectura Multi-Tenant)
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sector VARCHAR(100),
    codigo_registro VARCHAR(50) UNIQUE
);

-- Insertamos una empresa de prueba para que puedas probar el registro
INSERT INTO empresas (nombre, sector, codigo_registro) 
VALUES ('TechCorp Innovations', 'Tecnología', 'TECH-2026-VIP');

-- Tabla de Departamentos
CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
);

-- Insertamos departamentos de prueba para TechCorp
INSERT INTO departamentos (empresa_id, nombre) VALUES 
(1, 'Tecnología de la Información (IT)'), 
(1, 'Ventas y Marketing'), 
(1, 'Recursos Humanos');

-- Tabla de Usuarios (Con la columna apellidos incluida)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol_id INT NOT NULL,
    empresa_id INT DEFAULT NULL,
    departamento_id INT DEFAULT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) DEFAULT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE SET NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);

-- ==========================================
-- NÚCLEO CIENTÍFICO (BAT-12)
-- ==========================================

-- Tabla de Dimensiones del BAT-12
CREATE TABLE dimensiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

INSERT INTO dimensiones (id, nombre, descripcion) VALUES 
(1, 'Agotamiento', 'Fatiga física y mental severa.'),
(2, 'Distanciamiento Mental', 'Cinismo y evitación del trabajo.'),
(3, 'Deterioro Cognitivo', 'Problemas de concentración, memoria y atención.'),
(4, 'Deterioro Emocional', 'Falta de control sobre las emociones en el trabajo.');

-- Tabla de Preguntas del BAT-12
CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dimension_id INT NOT NULL,
    texto VARCHAR(255) NOT NULL,
    es_activo TINYINT(1) DEFAULT 1,
    FOREIGN KEY (dimension_id) REFERENCES dimensiones(id)
);

INSERT INTO preguntas (dimension_id, texto) VALUES 
(1, 'En el trabajo, me siento mentalmente agotado/a.'),
(1, 'Después de un día de trabajo, me resulta difícil recuperar mi energía.'),
(1, 'Me siento físicamente agotado/a en el trabajo.'),
(2, 'Me cuesta encontrar entusiasmo por mi trabajo.'),
(2, 'Siento una fuerte aversión hacia mi trabajo.'),
(2, 'Soy cínico/a sobre lo que significa mi trabajo para los demás.'),
(3, 'En el trabajo, me cuesta mantener la concentración.'),
(3, 'Cuando estoy trabajando, cometo errores porque estoy distraído/a.'),
(3, 'En el trabajo, me cuesta pensar con claridad.'),
(4, 'En el trabajo, me siento incapaz de controlar mis emociones.'),
(4, 'No reconozco mi propia forma de reaccionar emocionalmente en el trabajo.'),
(4, 'En mi trabajo me irrito con facilidad sin saber por qué.');

-- ==========================================
-- TABLAS TRANSACCIONALES (Resultados)
-- ==========================================

-- Evaluaciones: Guarda las medias matemáticas del test
CREATE TABLE evaluaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    puntuacion_total DECIMAL(4,2) NOT NULL,
    dim_agotamiento DECIMAL(4,2) NOT NULL,
    dim_distanciamiento DECIMAL(4,2) NOT NULL,
    dim_cognitivo DECIMAL(4,2) NOT NULL,
    dim_emocional DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Respuestas Evaluación: Guarda la respuesta exacta (1 al 5) de cada pregunta (Auditoría)
CREATE TABLE respuestas_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id INT NOT NULL,
    pregunta_id INT NOT NULL,
    valor INT NOT NULL, 
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE
);