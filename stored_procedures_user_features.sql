-- =====================================================
-- STORED PROCEDURES PARA FUNCIONALIDADES DE USUARIO
-- Base de datos: juego_finanzas
-- =====================================================

USE juego_finanzas;

-- =====================================================
-- 1. OBTENER PERFIL POR ID_USUARIO
-- =====================================================
DROP PROCEDURE IF EXISTS obtener_perfil_por_usuario;

DELIMITER $$
CREATE PROCEDURE obtener_perfil_por_usuario(IN p_id_usuario INT)
BEGIN
    SELECT
        id_perfil,
        id_usuario,
        nombre_perfil,
        edad,
        foto_perfil,
        monedas
    FROM perfiles
    WHERE id_usuario = p_id_usuario
    LIMIT 1;
END$$
DELIMITER ;

-- =====================================================
-- 2. INICIAR RETO (COMPRAR Y CREAR PROGRESO)
-- =====================================================
DROP PROCEDURE IF EXISTS iniciar_reto;

DELIMITER $$
CREATE PROCEDURE iniciar_reto(
    IN p_id_perfil INT,
    IN p_id_reto INT
)
BEGIN
    DECLARE v_costo INT;
    DECLARE v_monedas_actuales INT;
    DECLARE v_progreso_existente INT;
    DECLARE v_id_progreso INT;

    -- Obtener costo del reto y monedas del perfil
    SELECT costo_monedas INTO v_costo
    FROM retos
    WHERE id_reto = p_id_reto;

    SELECT monedas INTO v_monedas_actuales
    FROM perfiles
    WHERE id_perfil = p_id_perfil;

    -- Verificar si ya existe progreso para este reto
    SELECT COUNT(*) INTO v_progreso_existente
    FROM progreso
    WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

    -- Si ya existe progreso, retornarlo
    IF v_progreso_existente > 0 THEN
        SELECT
            id_progreso,
            id_perfil,
            id_reto,
            completado,
            fecha_completado,
            respuesta_seleccionada
        FROM progreso
        WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;
    ELSE
        -- Validar que tenga suficientes monedas
        IF v_monedas_actuales < v_costo THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Monedas insuficientes para iniciar este reto';
        END IF;

        -- Descontar monedas
        UPDATE perfiles
        SET monedas = monedas - v_costo
        WHERE id_perfil = p_id_perfil;

        -- Crear progreso con completado = NULL (no completado aún)
        INSERT INTO progreso (id_perfil, id_reto, completado, fecha_completado, respuesta_seleccionada)
        VALUES (p_id_perfil, p_id_reto, NULL, NULL, NULL);

        -- Obtener el ID del progreso recién creado
        SET v_id_progreso = LAST_INSERT_ID();

        -- Retornar el progreso creado
        SELECT
            id_progreso,
            id_perfil,
            id_reto,
            completado,
            fecha_completado,
            respuesta_seleccionada
        FROM progreso
        WHERE id_progreso = v_id_progreso;
    END IF;
END$$
DELIMITER ;

-- =====================================================
-- 3. OBTENER RETOS POR TEMA CON PROGRESO DEL USUARIO
-- =====================================================
DROP PROCEDURE IF EXISTS obtener_retos_por_tema;

DELIMITER $$
CREATE PROCEDURE obtener_retos_por_tema(
    IN p_id_tema INT,
    IN p_id_perfil INT
)
BEGIN
    SELECT
        r.id_reto,
        r.nombre_reto,
        r.id_tema,
        r.descripcion,
        r.pregunta,
        r.img_reto,
        r.recompensa_monedas,
        r.costo_monedas,
        r.respuesta_uno,
        r.respuesta_dos,
        r.respuesta_tres,
        r.respuesta_cuatro,
        -- No incluir respuestaCorrecta por seguridad
        p.id_progreso,
        p.completado,
        p.fecha_completado,
        p.respuesta_seleccionada
    FROM retos r
    LEFT JOIN progreso p ON r.id_reto = p.id_reto AND p.id_perfil = p_id_perfil
    WHERE r.id_tema = p_id_tema
    ORDER BY r.id_reto ASC;
END$$
DELIMITER ;

-- =====================================================
-- 4. MODIFICAR SOLUCIONAR_RETO PARA AGREGAR RECOMPENSA
-- =====================================================
DROP PROCEDURE IF EXISTS solucionar_reto;

DELIMITER $$
CREATE PROCEDURE solucionar_reto(
    IN p_id_perfil INT,
    IN p_id_reto INT,
    IN p_respuesta_seleccionada VARCHAR(100)
)
BEGIN
    DECLARE v_respuesta VARCHAR(100);
    DECLARE v_completado BOOLEAN;
    DECLARE v_fecha_completado TIMESTAMP;
    DECLARE v_progreso_existente INT DEFAULT 0;
    DECLARE v_recompensa_monedas INT DEFAULT 0;
    DECLARE v_ya_completado BOOLEAN DEFAULT FALSE;

    -- Obtener respuesta correcta y recompensa del reto
    SELECT respuestaCorrecta, recompensa_monedas
    INTO v_respuesta, v_recompensa_monedas
    FROM retos
    WHERE id_reto = p_id_reto;

    -- Verificar si existe progreso
    SELECT COUNT(*), COALESCE(MAX(completado), FALSE)
    INTO v_progreso_existente, v_ya_completado
    FROM progreso
    WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

    -- Si no existe progreso, salir (debe iniciar el reto primero)
    IF v_progreso_existente = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe iniciar el reto antes de solucionarlo';
    END IF;

    -- Si ya está completado, retornar el progreso actual sin cambios
    IF v_ya_completado = TRUE THEN
        SELECT
            id_progreso,
            id_perfil,
            id_reto,
            completado,
            fecha_completado,
            respuesta_seleccionada
        FROM progreso
        WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;
    ELSE
        -- Verificar si la respuesta es correcta
        IF v_respuesta = p_respuesta_seleccionada THEN
            SET v_completado = TRUE;
            SET v_fecha_completado = NOW();

            -- Actualizar progreso como completado
            UPDATE progreso
            SET
                completado = v_completado,
                fecha_completado = v_fecha_completado,
                respuesta_seleccionada = p_respuesta_seleccionada
            WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

            -- Agregar recompensa de monedas al perfil
            UPDATE perfiles
            SET monedas = monedas + v_recompensa_monedas
            WHERE id_perfil = p_id_perfil;

            -- Retornar el progreso actualizado
            SELECT
                id_progreso,
                id_perfil,
                id_reto,
                completado,
                fecha_completado,
                respuesta_seleccionada
            FROM progreso
            WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;
        ELSE
            -- Respuesta incorrecta: actualizar respuesta pero no marcar como completado
            UPDATE progreso
            SET respuesta_seleccionada = p_respuesta_seleccionada
            WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

            -- No retornar nada para indicar respuesta incorrecta
            SELECT NULL AS id_progreso;
        END IF;
    END IF;
END$$
DELIMITER ;

-- =====================================================
-- 5. CALCULAR PROGRESO GENERAL DEL USUARIO
-- =====================================================
DROP PROCEDURE IF EXISTS calcular_progreso_usuario;

DELIMITER $$
CREATE PROCEDURE calcular_progreso_usuario(IN p_id_perfil INT)
BEGIN
    DECLARE v_total_retos INT DEFAULT 0;
    DECLARE v_retos_completados INT DEFAULT 0;
    DECLARE v_porcentaje DECIMAL(5,2) DEFAULT 0.0;

    -- Contar total de retos disponibles
    SELECT COUNT(*) INTO v_total_retos FROM retos;

    -- Contar retos completados por el usuario
    SELECT COUNT(*) INTO v_retos_completados
    FROM progreso
    WHERE id_perfil = p_id_perfil AND completado = TRUE;

    -- Calcular porcentaje
    IF v_total_retos > 0 THEN
        SET v_porcentaje = (v_retos_completados * 100.0) / v_total_retos;
    END IF;

    -- Retornar estadísticas
    SELECT
        v_total_retos AS total_retos,
        v_retos_completados AS retos_completados,
        v_porcentaje AS porcentaje_completado;
END$$
DELIMITER ;

-- =====================================================
-- VERIFICACIÓN: Listar todos los procedimientos creados
-- =====================================================
SHOW PROCEDURE STATUS WHERE Db = 'juego_finanzas' AND Name IN (
    'obtener_perfil_por_usuario',
    'iniciar_reto',
    'obtener_retos_por_tema',
    'solucionar_reto',
    'calcular_progreso_usuario'
);
