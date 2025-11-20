-- =====================================================
-- STORED PROCEDURE: VERIFICAR SI UN TEMA ESTÁ COMPLETADO
-- Retorna cuántos retos tiene el tema y cuántos completó el usuario
-- =====================================================

USE juego_finanzas;

DROP PROCEDURE IF EXISTS verificar_tema_completado;

DELIMITER $$
CREATE PROCEDURE verificar_tema_completado(
    IN p_id_tema INT,
    IN p_id_perfil INT
)
BEGIN
    DECLARE v_total_retos INT DEFAULT 0;
    DECLARE v_retos_completados INT DEFAULT 0;
    DECLARE v_esta_completado BOOLEAN DEFAULT FALSE;

    -- Contar total de retos del tema
    SELECT COUNT(*) INTO v_total_retos
    FROM retos
    WHERE id_tema = p_id_tema;

    -- Contar retos completados por el usuario en este tema
    SELECT COUNT(*) INTO v_retos_completados
    FROM progreso p
    INNER JOIN retos r ON p.id_reto = r.id_reto
    WHERE r.id_tema = p_id_tema
      AND p.id_perfil = p_id_perfil
      AND p.completado = TRUE;

    -- Determinar si el tema está completado
    IF v_total_retos > 0 AND v_retos_completados = v_total_retos THEN
        SET v_esta_completado = TRUE;
    END IF;

    -- Retornar estadísticas
    SELECT
        p_id_tema AS id_tema,
        v_total_retos AS total_retos,
        v_retos_completados AS retos_completados,
        v_esta_completado AS esta_completado;
END$$
DELIMITER ;

-- =====================================================
-- STORED PROCEDURE: OBTENER PROGRESO POR TEMA PARA USUARIO
-- Retorna el progreso de todos los temas para un usuario
-- =====================================================

DROP PROCEDURE IF EXISTS obtener_progreso_por_temas;

DELIMITER $$
CREATE PROCEDURE obtener_progreso_por_temas(
    IN p_id_perfil INT
)
BEGIN
    SELECT
        t.id_tema,
        t.nombre AS nombre_tema,
        COUNT(r.id_reto) AS total_retos,
        SUM(CASE WHEN p.completado = TRUE THEN 1 ELSE 0 END) AS retos_completados,
        CASE
            WHEN COUNT(r.id_reto) > 0 AND
                 SUM(CASE WHEN p.completado = TRUE THEN 1 ELSE 0 END) = COUNT(r.id_reto)
            THEN TRUE
            ELSE FALSE
        END AS esta_completado
    FROM temas t
    LEFT JOIN retos r ON t.id_tema = r.id_tema
    LEFT JOIN progreso p ON r.id_reto = p.id_reto AND p.id_perfil = p_id_perfil
    GROUP BY t.id_tema, t.nombre
    ORDER BY t.id_tema ASC;
END$$
DELIMITER ;

-- Verificar que los procedimientos se crearon correctamente
SHOW PROCEDURE STATUS WHERE Db = 'juego_finanzas' AND Name IN (
    'verificar_tema_completado',
    'obtener_progreso_por_temas'
);
