CREATE DATABASE juego_finanzas;
-- DROP DATABASE juego_finanzas;
USE juego_finanzas;

-- =====================================
CREATE TABLE usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  correo VARCHAR(100) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  rol ENUM('Usuario', 'Administrador') DEFAULT 'Usuario',
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE temas(
  id_tema INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  descripcion TEXT,
  precio int default 0
);

CREATE TABLE perfiles (
  id_perfil INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT,
  nombre_perfil VARCHAR(50) NOT NULL UNIQUE,
  foto_perfil VARCHAR(255) DEFAULT 'default.png',
  tema_actual INT DEFAULT 1,
  monedas INT DEFAULT 0,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE retos (
  id_reto INT AUTO_INCREMENT PRIMARY KEY,
  tipo_pregunta varchar(50),
  nombre_reto VARCHAR(100),
  id_tema int,
  descripcion TEXT,
  recompensa_monedas INT DEFAULT 0,
  respuesta_uno VARCHAR(100),
  respuesta_dos VARCHAR(100),
  respuesta_tres VARCHAR(100),
  respuesta_cuatro VARCHAR(100),
  respuestaCorrecta VARCHAR(100),
  foreign key (id_tema) references temas(id_tema)
);

CREATE TABLE progreso (
  id_progreso INT AUTO_INCREMENT PRIMARY KEY,
  id_perfil INT,
  id_reto INT,
  completado BOOLEAN DEFAULT FALSE,
  fecha_completado TIMESTAMP NULL,
  respuesta_seleccionada VARCHAR(100),
  FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil) ON DELETE CASCADE,
  FOREIGN KEY (id_reto) REFERENCES retos(id_reto) ON DELETE CASCADE
);


CREATE TABLE tips_periodicas (
  id_recompensa INT AUTO_INCREMENT PRIMARY KEY,
  id_perfil INT,
  nombre VARCHAR(100),
  descripcion TEXT,
  FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
);

-- ................................. vistas ................................................
-- vista para ver la informacion retos y a que temas estan asociaddos
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

-- Vista para ver usuario y reto en el que se encuentra
-- CREATE OR REPLACE VIEW vista_progreso_detallado AS
-- SELECT
--     p.id_progreso,
--     per.id_perfil,
--     per.nombre_perfil,
--     r.id_reto,
--     r.nombre_reto,
--     p.completado,
--     p.fecha_completado
-- FROM progreso p
-- INNER JOIN perfiles per ON p.id_perfil = per.id_perfil
-- INNER JOIN retos r ON p.id_reto = r.id_reto
-- ORDER BY p.id_progreso DESC;


-- Vista para ver solo retos completados para el progreso del usuario
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

-- vista para ver al usuario con la informacion correspondiente de su perfil y saber en que tema se encuentra
CREATE OR REPLACE VIEW vista_resumen_perfiles AS
SELECT
    p.id_perfil,
    p.nombre_perfil,
    u.correo AS usuario_correo,
    p.monedas,
    p.tema_actual
FROM perfiles p
INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
ORDER BY p.monedas DESC;

-- vista para el perfil del administrador
CREATE OR REPLACE VIEW vista_administradores_perfiles AS
SELECT
    u.id_usuario,
    u.correo,
    p.id_perfil,
    p.nombre_perfil,
    p.monedas
FROM usuarios u
INNER JOIN perfiles p ON u.id_usuario = p.id_usuario
WHERE u.rol = 'Administrador'
ORDER BY u.id_usuario;

CREATE OR REPLACE VIEW vista_usuarios_perfiles AS
SELECT
    u.id_usuario,
    u.correo,
    p.id_perfil,
    p.nombre_perfil,
    p.monedas
FROM usuarios u
INNER JOIN perfiles p ON u.id_usuario = p.id_usuario
WHERE u.rol = 'Usuario'
ORDER BY u.id_usuario;

-- ------------------------------- Procedimientos -----------------------------------------------
DELIMITER $$
-- ................................... tabla temas ...............................................
-- CREATE
DROP PROCEDURE IF EXISTS temas_crear $$
CREATE PROCEDURE temas_crear(
  IN p_nombre VARCHAR(100),
  IN p_descripcion TEXT,
  IN p_precio INT
)
BEGIN
  INSERT INTO temas(nombre, descripción, precio) VALUES (p_nombre, p_descripción, p_precio);
  SELECT LAST_INSERT_ID() AS id_usuario;
END $$

-- READ(UNO)
DROP PROCEDURE IF EXISTS tema_ver $$
CREATE PROCEDURE tema_ver(IN p_id INT)
BEGIN
SELECT * FROM temas WHERE id_tema = p_id;
END $$

-- LIST(TODOS)
DROP PROCEDURE IF EXISTS temas_listar $$
CREATE PROCEDURE temas_listar()
BEGIN
SELECT * FROM temas;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS temas_actualizar $$
CREATE PROCEDURE temas_actualizar(
IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    UPDATE temas SET nombre = p_nombre, descripcion = p_descripcion WHERE id_tema = p_id;
    SELECT ROW_COUNT() AS filas;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS temas_eliminar $$
CREATE PROCEDURE temas_eliminar(IN p_id INT)
BEGIN
DELETE FROM temas WHERE id_tema = p_id;
    SELECT ROW_COUNT() AS filas;
END $$


-- ........................................ tabla retos ........................................
-- CREATE
DROP PROCEDURE IF EXISTS retos_crear $$
CREATE PROCEDURE retos_crear(
  IN p_tipo_pregunta VARCHAR(50),
  IN p_nombre_reto VARCHAR(100),
  IN p_id_tema INT,
  IN p_descripcion TEXT,
  IN p_recompensa_monedas INT,
  IN p_respuesta_uno VARCHAR(100),
  IN p_respuesta_dos VARCHAR(100),
  IN p_respuesta_tres VARCHAR(100),
  IN p_respuesta_cuatro VARCHAR(100),
  IN p_respuestaCorrecta VARCHAR(100)
)
BEGIN
  INSERT INTO retos (
    tipo_pregunta, nombre_reto, id_tema, descripcion,
    recompensa_monedas, respuesta_uno, respuesta_dos,
    respuesta_tres, respuesta_cuatro, respuestaCorrecta
  )
  VALUES (
    p_tipo_pregunta, p_nombre_reto, p_id_tema, p_descripcion,
    p_recompensa_monedas, p_respuesta_uno, p_respuesta_dos,
    p_respuesta_tres, p_respuesta_cuatro, p_respuestaCorrecta
  );

  SELECT LAST_INSERT_ID() AS id_reto;
END $$

-- READ (uno)
DROP PROCEDURE IF EXISTS reto_ver $$
CREATE PROCEDURE reto_ver(IN p_id INT)
BEGIN
  SELECT *
  FROM retos
  WHERE id_reto = p_id;
END $$

-- LIST (todos)
DROP PROCEDURE IF EXISTS retos_listar $$
CREATE PROCEDURE retos_listar()
BEGIN
  SELECT *
  FROM retos
  ORDER BY id_reto DESC;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS retos_actualizar $$
CREATE PROCEDURE retos_actualizar(
  IN p_id INT,
  IN p_tipo_pregunta VARCHAR(50),
  IN p_nombre_reto VARCHAR(100),
  IN p_id_tema INT,
  IN p_descripcion TEXT,
  IN p_recompensa_monedas INT,
  IN p_respuesta_uno VARCHAR(100),
  IN p_respuesta_dos VARCHAR(100),
  IN p_respuesta_tres VARCHAR(100),
  IN p_respuesta_cuatro VARCHAR(100),
  IN p_respuestaCorrecta VARCHAR(100)
)
BEGIN
  UPDATE retos
  SET
    tipo_pregunta = p_tipo_pregunta,
    nombre_reto = p_nombre_reto,
    id_tema = p_id_tema,
    descripcion = p_descripcion,
    recompensa_monedas = p_recompensa_monedas,
    respuesta_uno = p_respuesta_uno,
    respuesta_dos = p_respuesta_dos,
    respuesta_tres = p_respuesta_tres,
    respuesta_cuatro = p_respuesta_cuatro,
    respuestaCorrecta = p_respuestaCorrecta
  WHERE id_reto = p_id;

  SELECT ROW_COUNT() AS filas;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS retos_eliminar $$
CREATE PROCEDURE retos_eliminar(IN p_id INT)
BEGIN
  DELETE FROM retos WHERE id_reto = p_id;
  SELECT ROW_COUNT() AS filas;
END $$


-- ........................................... tabla Progreso ......................................
-- CREATE
DROP PROCEDURE IF EXISTS progresos_crear $$
CREATE PROCEDURE progresos_crear(
  IN p_id_perfil INT,
  IN p_id_reto INT,
  IN p_completado BOOLEAN,
  IN p_fecha_completado TIMESTAMP
)
BEGIN
  INSERT INTO progreso (id_perfil, id_reto, completado, fecha_completado)
  VALUES (p_id_perfil, p_id_reto, p_completado, p_fecha_completado);
  SELECT LAST_INSERT_ID() AS id_progreso;
END $$

-- READ (uno)
DROP PROCEDURE IF EXISTS progreso_ver $$
CREATE PROCEDURE progreso_ver(IN p_id INT)
BEGIN
  SELECT *
  FROM progreso
  WHERE id_progreso = p_id;
END $$

-- LIST (todos)
DROP PROCEDURE IF EXISTS progresos_listar $$
CREATE PROCEDURE progresos_listar()
BEGIN
  SELECT *
  FROM progreso
  ORDER BY id_progreso DESC;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS progresos_actualizar $$
CREATE PROCEDURE progresos_actualizar(
  IN p_id INT,
  IN p_id_perfil INT,
  IN p_id_reto INT,
  IN p_completado BOOLEAN,
  IN p_fecha_completado TIMESTAMP
)
BEGIN
  UPDATE progreso
  SET
    id_perfil = p_id_perfil,
    id_reto = p_id_reto,
    completado = p_completado,
    fecha_completado = p_fecha_completado
  WHERE id_progreso = p_id;

  SELECT ROW_COUNT() AS filas;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS progresos_eliminar $$
CREATE PROCEDURE progresos_eliminar(IN p_id INT)
BEGIN
  DELETE FROM progreso WHERE id_progreso = p_id;
  SELECT ROW_COUNT() AS filas;
END $$


-- ............................................ tabla usuarios .......................................
-- CREATE
DROP PROCEDURE IF EXISTS usuarios_crear $$
CREATE PROCEDURE usuarios_crear(
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(255),
    IN p_rol ENUM('Usuario', 'Administrador')
)
BEGIN
    INSERT INTO usuarios (correo, contrasena, rol)
    VALUES (p_correo, p_contrasena, p_rol);
END $$

-- LIST(TODOS)
DROP PROCEDURE IF EXISTS usuarios_listar $$
CREATE PROCEDURE usuarios_listar()
BEGIN
    SELECT id_usuario, correo, rol, fecha_registro
    FROM usuarios;
END $$

-- READ
DROP PROCEDURE IF EXISTS usuario_ver $$
CREATE PROCEDURE usuario_ver(IN p_id INT)
BEGIN
    SELECT id_usuario, correo, rol, fecha_registro
    FROM usuarios
    WHERE id_usuario = p_id;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS usuarios_actualizar $$
CREATE PROCEDURE usuarios_actualizar(
    IN p_id_usuario INT,
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(255),
    IN p_rol ENUM('Usuario', 'Administrador')
)
BEGIN
    UPDATE usuarios
    SET correo = p_correo,
        contrasena = p_contrasena,
        rol = p_rol
    WHERE id_usuario = p_id_usuario;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS usuarios_eliminar $$
CREATE PROCEDURE usuarios_eliminar(IN p_id INT)
BEGIN
    DELETE FROM usuarios WHERE id_usuario = p_id;
END $$


-- .................................................... tabla perfiles .............................................

-- CREATE
DROP PROCEDURE IF EXISTS perfil_crear $$
CREATE PROCEDURE perfil_crear(
    IN p_id_usuario INT,
    IN p_nombre_perfil VARCHAR(50),
    IN p_foto_perfil VARCHAR(255)
)
BEGIN
    INSERT INTO perfiles (id_usuario, nombre_perfil, foto_perfil)
    VALUES (p_id_usuario, p_nombre_perfil, p_foto_perfil);
END $$

-- LIST(TODOS)
DROP PROCEDURE IF EXISTS perfil_listar $$
CREATE PROCEDURE perfil_listar()
BEGIN
    SELECT p.id_perfil, u.correo, p.nombre_perfil, p.monedas
    FROM perfiles p
    JOIN usuarios u ON p.id_usuario = u.id_usuario;
END $$

-- READ
DROP PROCEDURE IF EXISTS perfil_ver $$
CREATE PROCEDURE perfil_ver(IN p_id INT)
BEGIN
    SELECT * FROM perfiles WHERE id_perfil = p_id;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS perfil_actualizar $$
CREATE PROCEDURE perfil_actualizar(
    IN p_id_perfil INT,
    IN p_nombre_perfil VARCHAR(50),
    IN p_foto_perfil VARCHAR(255),
    IN p_tema_actual INT,
    IN p_monedas INT
)
BEGIN
    UPDATE perfiles
    SET nombre_perfil = p_nombre_perfil,
        foto_perfil = p_foto_perfil,
        tema_actual = p_tema_actual,
        monedas = p_monedas
    WHERE id_perfil = p_id_perfil;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS perfil_eliminar $$
CREATE PROCEDURE perfil_eliminar(IN p_id INT)
BEGIN
    DELETE FROM perfiles WHERE id_perfil = p_id;
END $$



-- ............................................. procedimientos para tips_periodicos ....................................
-- CREATE
DROP PROCEDURE IF EXISTS tip_crear $$
CREATE PROCEDURE tip_crear(
    IN p_id_perfil INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    INSERT INTO tips_periodicas (id_perfil, nombre, descripcion)
    VALUES (p_id_perfil, p_nombre, p_descripcion);
END $$

-- LIST(TODOS)
DROP PROCEDURE IF EXISTS tip_listar $$
CREATE PROCEDURE tip_listar()
BEGIN
    SELECT t.id_recompensa, p.nombre_perfil, t.nombre, t.descripcion
    FROM tips_periodicas t
    JOIN perfiles p ON t.id_perfil = p.id_perfil;
END $$

-- READ
DROP PROCEDURE IF EXISTS tip_ver $$
CREATE PROCEDURE tip_ver(IN p_id INT)
BEGIN
    SELECT * FROM tips_periodicas WHERE id_recompensa = p_id;
END $$

-- UPDATE
DROP PROCEDURE IF EXISTS tip_actualizar $$
CREATE PROCEDURE tip_actualizar(
    IN p_id_recompensa INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    UPDATE tips_periodicas
    SET nombre = p_nombre,
        descripcion = p_descripcion
    WHERE id_recompensa = p_id_recompensa;
END $$

-- DELETE
DROP PROCEDURE IF EXISTS tip_eliminar $$
CREATE PROCEDURE tip_eliminar(IN p_id INT)
BEGIN
    DELETE FROM tips_periodicas WHERE id_recompensa = p_id;
END $$

-- ....................................................procedimiento principal..........................................................
-- ........ solucionar reto .............
DROP PROCEDURE IF EXISTS solucionar_reto $$
CREATE PROCEDURE solucionar_reto(
  IN p_id_perfil INT,
  IN p_id_reto INT,
  IN p_respuesta_seleccionada varchar(100)
)
BEGIN
	declare v_respuesta varchar(100);
    declare v_completado boolean;
    declare v_fecha_completado timestamp;
    declare v_progreso_existente int default 0;
    declare v_monedas int default 0;
   
    select respuestaCorrecta INTO v_respuesta from retos where id_reto = p_id_reto;
    select recompensa_monedas INTO v_monedas from retos where id_reto = p_id_reto;
    select count(*) into v_progreso_existente from progreso where id_perfil = p_id_perfil and id_reto = p_id_reto;
 
    if v_respuesta = p_respuesta_seleccionada then
		set v_completado = TRUE, v_fecha_completado = NOW();
        if v_progreso_existente = 0 then
			INSERT INTO progreso (id_perfil, id_reto, completado, fecha_completado, respuesta_seleccionada) VALUES (p_id_perfil, p_id_reto, v_completado, v_fecha_completado, p_respuesta_seleccionada);
            update perfiles set monedas = (monedas + v_monedas) where id_perfil = p_id_perfil;
            SELECT LAST_INSERT_ID() AS id_progreso;
		else
			update progreso set completado = v_completado, fecha_completado = v_fecha_completado, respuesta_seleccionada = p_respuesta_seleccionada where id_perfil = p_id_perfil and id_reto = p_id_reto;
            update perfiles set monedas = (monedas + v_monedas) where id_perfil = p_id_perfil;
            SELECT * from progreso where id_perfil = p_id_perfil and id_reto = p_id_reto;
		end if;
	end if;
END $$

-- ........... revisar mis retos
DROP PROCEDURE IF EXISTS informacion_retos_solucionados $$
CREATE PROCEDURE informacion_retos_solucionados(IN p_id INT)
BEGIN
  SELECT p.id_progreso, per.nombre_perfil, p.id_reto, p.completado, p.fecha_completado, p.respuesta_seleccionada 
  FROM progreso p
  inner join perfiles per on per.id_perfil = p.id_perfil
  WHERE p.id_perfil = p_id;
END $$


DELIMITER $$
-- =============================================================================

-- -- CREATE
-- CALL temas_crear('Educación Financiera', 'Aprende sobre ahorro, presupuesto y finanzas personales.');
-- CALL temas_crear('Inversión Básica', 'Conceptos fundamentales de inversión.');
-- -- READ (UNO)
-- CALL tema_ver(1);
-- -- LIST (TODOS)
-- CALL temas_listar();
-- -- UPDATE
-- CALL temas_actualizar(1, 'Ahorro Inteligente', 'Consejos prácticos para ahorrar mejor.');
-- -- DELETE
-- CALL temas_eliminar(2);


-- CREATE
-- CALL retos_crear('Selección múltiple','Reto de Ahorro',1,'Selecciona el mejor hábito financiero.',50,
-- 	'Ahorrar 10% del salario','Gastar todo','No llevar presupuesto','Endeudarse','1');
-- -- READ (UNO)
-- CALL reto_ver(1);
-- -- LIST (TODOS)
-- CALL retos_listar();
-- -- UPDATE
-- CALL retos_actualizar(1,'Selección múltiple','Reto de Ahorro Actualizado',1,'Reto mejorado sobre hábitos financieros',75,
-- 	'Ahorrar 15%','No gastar más de lo que ganas','Usar tarjeta de crédito sin control','Ignorar gastos','2');
-- -- DELETE
-- CALL retos_eliminar(3);


-- CREATE
-- CALL progresos_crear(1, 1, TRUE, NOW());
-- CALL progresos_crear(1, 2, FALSE, NULL);
-- -- READ (UNO)
-- CALL progreso_ver(2);
-- -- LIST (TODOS)
-- CALL progresos_listar();
-- CALL solucionar_reto(1,2,'Ahorrar primero y gastar después');
-- CALL informacion_retos_solucionados(1);
-- -- UPDATE
-- CALL progresos_actualizar(1, 1, 1, TRUE, NOW());
-- -- DELETE
-- CALL progresos_eliminar(2);


-- CREATE
-- CALL usuarios_crear('juan.perez@correo.com', 'clave123', 'Usuario');
-- CALL usuarios_crear('admin@gym.com', 'admin123', 'Administrador');
-- -- READ (UNO)
-- CALL usuario_ver(1);
-- -- LIST (TODOS)
-- CALL usuarios_listar();
-- -- UPDATE
-- CALL usuarios_actualizar(1, 'juan.perez@correo.com', 'nuevaClave456', 'Usuario');
-- -- DELETE
-- CALL usuarios_eliminar(3);


-- CREATE
-- CALL perfil_crear(1, 'PerfilJuan', 'juan.png');
-- CALL perfil_crear(2, 'PerfilAdmin', 'admin.png');
-- -- READ (UNO)
-- CALL perfil_ver(1);
-- -- LIST (TODOS)
-- CALL perfil_listar();
-- -- UPDATE
-- CALL perfil_actualizar(1, 'PerfilJuanActualizado', 'juan_new.png', 2, 500);
-- -- DELETE
-- CALL perfil_eliminar(3);


-- CREATE
-- CALL tip_crear(1, 'Tip de ahorro', 'Aparta el 10% de tus ingresos mensualmente.');
-- CALL tip_crear(2, 'Tip de inversión', 'Invierte en productos con bajo riesgo al inicio.');
-- -- READ (UNO)
-- CALL tip_ver(1);
-- -- LIST (TODOS)
-- CALL tip_listar();
-- -- UPDATE
-- CALL tip_actualizar(1, 'Tip de ahorro actualizado', 'Automatiza tus ahorros para hacerlo más fácil.');
-- -- DELETE
-- CALL tip_eliminar(2);


-- ===============================================================
-- LLAMADOS A VISTAS


-- SELECT * FROM vista_retos_temas;
-- SELECT * FROM vista_usuarios_perfiles;
-- SELECT * FROM vista_progreso_completado;
-- SELECT * FROM vista_resumen_perfiles;
-- SELECT * FROM vista_administradores_perfiles;
