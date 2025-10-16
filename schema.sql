CREATE DATABASE IF NOT EXISTS juego_finanzas_version_2;
USE juego_finanzas_version_2;

-- =====================================
-- TABLA USUARIOS
-- =====================================
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  correo VARCHAR(100) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  rol ENUM('Usuario', 'Administrador') DEFAULT 'Usuario',
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- TABLA TEMAS
-- =====================================
CREATE TABLE IF NOT EXISTS temas(
  id_tema INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  descripcion TEXT
);

-- =====================================
-- TABLA PERFILES
-- =====================================
CREATE TABLE IF NOT EXISTS perfiles (
  id_perfil INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT,
  nombre_perfil VARCHAR(50) NOT NULL UNIQUE,
  foto_perfil VARCHAR(255) DEFAULT 'default.png',
  tema_actual INT DEFAULT 1,
  monedas INT DEFAULT 0,
  saldo DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =====================================
-- TABLA RETOS
-- =====================================
CREATE TABLE IF NOT EXISTS retos (
  id_reto INT AUTO_INCREMENT PRIMARY KEY,
  tipo_pregunta VARCHAR(50),
  nombre_reto VARCHAR(100),
  id_tema INT,
  descripcion TEXT,
  recompensa_monedas INT DEFAULT 0,
  respuesta_uno VARCHAR(100),
  respuesta_dos VARCHAR(100),
  respuesta_tres VARCHAR(100),
  respuesta_cuatro VARCHAR(100),
  respuestaCorrecta VARCHAR(100),
  FOREIGN KEY (id_tema) REFERENCES temas(id_tema)
);

-- =====================================
-- TABLA PROGRESO
-- =====================================
CREATE TABLE IF NOT EXISTS progreso (
  id_progreso INT AUTO_INCREMENT PRIMARY KEY,
  id_perfil INT,
  id_reto INT,
  completado BOOLEAN DEFAULT FALSE,
  fecha_completado TIMESTAMP NULL,
  respuesta_seleccionada VARCHAR(100),
  FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil) ON DELETE CASCADE,
  FOREIGN KEY (id_reto) REFERENCES retos(id_reto) ON DELETE CASCADE
);

-- =====================================
-- TABLA TIPS PERIÓDICAS
-- =====================================
CREATE TABLE IF NOT EXISTS tips_periodicas (
  id_recompensa INT AUTO_INCREMENT PRIMARY KEY,
  id_perfil INT,
  nombre VARCHAR(100),
  descripcion TEXT,
  FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
);

-- =====================================
-- VISTAS
-- =====================================

-- Vista para ver retos con sus temas asociados
CREATE OR REPLACE VIEW vista_retos_temas AS
SELECT
    r.id_reto,
    r.nombre_reto,
    r.tipo_pregunta,
    r.descripcion AS descripcion_reto,
    r.recompensa_monedas,
    r.respuesta_uno,
    r.respuesta_dos,
    r.respuesta_tres,
    r.respuesta_cuatro,
    r.respuestaCorrecta,
    t.id_tema,
    t.nombre AS nombre_tema,
    t.descripcion AS descripcion_tema
FROM retos r
INNER JOIN temas t ON r.id_tema = t.id_tema
ORDER BY r.id_reto DESC;

-- Vista para ver progreso detallado
CREATE OR REPLACE VIEW vista_progreso_detallado AS
SELECT
    p.id_progreso,
    per.id_perfil,
    per.nombre_perfil,
    r.id_reto,
    r.nombre_reto,
    p.completado,
    p.fecha_completado
FROM progreso p
INNER JOIN perfiles per ON p.id_perfil = per.id_perfil
INNER JOIN retos r ON p.id_reto = r.id_reto
ORDER BY p.id_progreso DESC;

-- Vista para ver solo retos completados
CREATE OR REPLACE VIEW vista_progreso_completado AS
SELECT
    p.id_progreso,
    per.nombre_perfil AS perfil,
    r.nombre_reto AS reto,
    p.fecha_completado
FROM progreso p
INNER JOIN perfiles per ON p.id_perfil = per.id_perfil
INNER JOIN retos r ON p.id_reto = r.id_reto
WHERE p.completado = TRUE
ORDER BY p.fecha_completado DESC;

-- Vista resumen de perfiles
CREATE OR REPLACE VIEW vista_resumen_perfiles AS
SELECT
    p.id_perfil,
    p.nombre_perfil,
    u.correo AS usuario_correo,
    p.monedas,
    p.saldo,
    p.tema_actual
FROM perfiles p
INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
ORDER BY p.monedas DESC;

-- Vista para administradores
CREATE OR REPLACE VIEW vista_administradores_perfiles AS
SELECT
    u.id_usuario,
    u.correo,
    p.id_perfil,
    p.nombre_perfil,
    p.monedas,
    p.saldo
FROM usuarios u
INNER JOIN perfiles p ON u.id_usuario = p.id_usuario
WHERE u.rol = 'Administrador'
ORDER BY u.id_usuario;

-- =====================================
-- DATOS DE EJEMPLO
-- =====================================

-- Insertar temas
INSERT INTO temas (nombre, descripcion) VALUES
('Ahorro Personal', 'Aprende a manejar tus finanzas personales y crear un hábito de ahorro.'),
('Inversión Básica', 'Conceptos introductorios sobre inversiones seguras y rentables.'),
('Presupuesto Familiar', 'Cómo organizar tus gastos y priorizar necesidades en el hogar.'),
('Créditos y Deudas', 'Conoce cómo funcionan los préstamos, intereses y deudas responsables.'),
('Educación Financiera Avanzada', 'Conceptos financieros complejos para alcanzar libertad económica.');

-- Insertar retos de ejemplo
INSERT INTO retos (tipo_pregunta, nombre_reto, id_tema, descripcion, recompensa_monedas,
                   respuesta_uno, respuesta_dos, respuesta_tres, respuesta_cuatro, respuestaCorrecta)
VALUES
('Selección Única', '¿Qué porcentaje de tus ingresos se recomienda ahorrar?', 1,
 'Descubre cuánto deberías guardar para emergencias.', 50,
 '10%', '30%', '50%', '5%', '2'),

('Verdadero o Falso', 'Invertir siempre implica riesgo.', 2,
 'Evalúa tu conocimiento sobre los riesgos financieros.', 40,
 'Verdadero', 'Falso', NULL, NULL, '1'),

('Selección Única', '¿Cuál de los siguientes es un gasto fijo?', 3,
 'Identifica los gastos que se repiten mes a mes.', 30,
 'Cine', 'Almuerzo en restaurante', 'Arriendo', 'Vacaciones', '3'),

('Selección Única', '¿Qué significa tener deuda buena?', 4,
 'Entiende cuándo una deuda puede ser útil.', 60,
 'Deuda que aumenta tu patrimonio', 'Deuda que no pagas', 'Deuda con alto interés', 'Deuda innecesaria', '1'),

('Selección Múltiple', 'Selecciona hábitos financieros saludables.', 5,
 'Evalúa tus hábitos financieros positivos.', 100,
 'Ahorrar mensualmente', 'Invertir sin informarte', 'Llevar un presupuesto', 'Gastar sin control', '1');
 
USE juego_finanzas_version_2;
SHOW TABLES;  -- Deberías ver tablas como usuarios, temas, perfiles, retos, progreso, tips_periodicas
SELECT * FROM usuarios;  -- Deberías ver los 5 usuarios insertados (ana.gomez@mail.com, etc.)
SELECT * FROM temas;  -- Ver los 5 temas
SELECT * FROM perfiles;  -- Ver los perfiles
SELECT * FROM retos;  -- Ver los retos
SELECT * FROM progreso;  -- Ver el progreso
SELECT * FROM tips_periodicas;  -- Ver los tips

