-- =====================================================
-- TRIGGER PARA DEVOLVER MONEDAS AL BORRAR PROGRESO
-- =====================================================
-- Este trigger devuelve las monedas gastadas cuando se elimina
-- un registro de progreso que NO haya sido completado

USE juego_finanzas;

-- Eliminar trigger si existe
DROP TRIGGER IF EXISTS devolver_monedas_progreso;

DELIMITER $$

CREATE TRIGGER devolver_monedas_progreso
AFTER DELETE ON progreso
FOR EACH ROW
BEGIN
    DECLARE v_costo INT;

    -- Solo devolver monedas si el reto NO estaba completado
    -- (si estaba completado, ya ganó la recompensa, no se devuelve el costo)
    IF OLD.completado IS NULL OR OLD.completado = FALSE THEN
        -- Obtener el costo del reto eliminado
        SELECT costo_monedas INTO v_costo
        FROM retos
        WHERE id_reto = OLD.id_reto;

        -- Devolver las monedas al perfil
        UPDATE perfiles
        SET monedas = monedas + v_costo
        WHERE id_perfil = OLD.id_perfil;
    END IF;
END$$

DELIMITER ;

-- Verificar que el trigger fue creado
SELECT
    TRIGGER_NAME,
    EVENT_MANIPULATION,
    EVENT_OBJECT_TABLE,
    ACTION_TIMING
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = 'juego_finanzas'
AND TRIGGER_NAME = 'devolver_monedas_progreso';
