"""
Comando de Django para crear los stored procedures necesarios
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Crea los stored procedures necesarios para las funcionalidades de usuario'

    def handle(self, *args, **options):
        self.stdout.write("="*60)
        self.stdout.write("CREANDO STORED PROCEDURES")
        self.stdout.write("="*60)

        procedures = [
            self.crear_obtener_perfil_por_usuario,
            self.crear_iniciar_reto,
            self.crear_obtener_retos_por_tema,
            self.crear_solucionar_reto,
            self.crear_calcular_progreso_usuario
        ]

        for i, proc in enumerate(procedures, 1):
            try:
                self.stdout.write(f"\n{i}. {proc.__name__.replace('crear_', '').replace('_', ' ').title()}...")
                proc()
                self.stdout.write(self.style.SUCCESS("   [OK] Creado exitosamente"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   [ERROR] Error: {e}"))

        # Verificar procedimientos
        self.verificar_procedimientos()

        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("PROCESO COMPLETADO"))
        self.stdout.write("="*60)

    def crear_obtener_perfil_por_usuario(self):
        """Crea el SP para obtener perfil por id_usuario"""
        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS obtener_perfil_por_usuario")
            cursor.execute("""
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
                END
            """)

    def crear_iniciar_reto(self):
        """Crea el SP para iniciar un reto"""
        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS iniciar_reto")
            cursor.execute("""
                CREATE PROCEDURE iniciar_reto(
                    IN p_id_perfil INT,
                    IN p_id_reto INT
                )
                BEGIN
                    DECLARE v_costo INT;
                    DECLARE v_monedas_actuales INT;
                    DECLARE v_progreso_existente INT;
                    DECLARE v_id_progreso INT;

                    SELECT costo_monedas INTO v_costo
                    FROM retos
                    WHERE id_reto = p_id_reto;

                    SELECT monedas INTO v_monedas_actuales
                    FROM perfiles
                    WHERE id_perfil = p_id_perfil;

                    SELECT COUNT(*) INTO v_progreso_existente
                    FROM progreso
                    WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

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
                        IF v_monedas_actuales < v_costo THEN
                            SIGNAL SQLSTATE '45000'
                            SET MESSAGE_TEXT = 'Monedas insuficientes para iniciar este reto';
                        END IF;

                        UPDATE perfiles
                        SET monedas = monedas - v_costo
                        WHERE id_perfil = p_id_perfil;

                        INSERT INTO progreso (id_perfil, id_reto, completado, fecha_completado, respuesta_seleccionada)
                        VALUES (p_id_perfil, p_id_reto, NULL, NULL, NULL);

                        SET v_id_progreso = LAST_INSERT_ID();

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
                END
            """)

    def crear_obtener_retos_por_tema(self):
        """Crea el SP para obtener retos por tema con progreso"""
        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS obtener_retos_por_tema")
            cursor.execute("""
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
                        p.id_progreso,
                        p.completado,
                        p.fecha_completado,
                        p.respuesta_seleccionada
                    FROM retos r
                    LEFT JOIN progreso p ON r.id_reto = p.id_reto AND p.id_perfil = p_id_perfil
                    WHERE r.id_tema = p_id_tema
                    ORDER BY r.id_reto ASC;
                END
            """)

    def crear_solucionar_reto(self):
        """Crea/actualiza el SP para solucionar reto (con recompensa de monedas)"""
        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS solucionar_reto")
            cursor.execute("""
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

                    SELECT respuestaCorrecta, recompensa_monedas
                    INTO v_respuesta, v_recompensa_monedas
                    FROM retos
                    WHERE id_reto = p_id_reto;

                    SELECT COUNT(*), COALESCE(MAX(completado), FALSE)
                    INTO v_progreso_existente, v_ya_completado
                    FROM progreso
                    WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

                    IF v_progreso_existente = 0 THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Debe iniciar el reto antes de solucionarlo';
                    END IF;

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
                        IF v_respuesta = p_respuesta_seleccionada THEN
                            SET v_completado = TRUE;
                            SET v_fecha_completado = NOW();

                            UPDATE progreso
                            SET
                                completado = v_completado,
                                fecha_completado = v_fecha_completado,
                                respuesta_seleccionada = p_respuesta_seleccionada
                            WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

                            UPDATE perfiles
                            SET monedas = monedas + v_recompensa_monedas
                            WHERE id_perfil = p_id_perfil;

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
                            UPDATE progreso
                            SET respuesta_seleccionada = p_respuesta_seleccionada
                            WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

                            SELECT NULL AS id_progreso;
                        END IF;
                    END IF;
                END
            """)

    def crear_calcular_progreso_usuario(self):
        """Crea el SP para calcular progreso del usuario"""
        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS calcular_progreso_usuario")
            cursor.execute("""
                CREATE PROCEDURE calcular_progreso_usuario(IN p_id_perfil INT)
                BEGIN
                    DECLARE v_total_retos INT DEFAULT 0;
                    DECLARE v_retos_completados INT DEFAULT 0;
                    DECLARE v_porcentaje DECIMAL(5,2) DEFAULT 0.0;

                    SELECT COUNT(*) INTO v_total_retos FROM retos;

                    SELECT COUNT(*) INTO v_retos_completados
                    FROM progreso
                    WHERE id_perfil = p_id_perfil AND completado = TRUE;

                    IF v_total_retos > 0 THEN
                        SET v_porcentaje = (v_retos_completados * 100.0) / v_total_retos;
                    END IF;

                    SELECT
                        v_total_retos AS total_retos,
                        v_retos_completados AS retos_completados,
                        v_porcentaje AS porcentaje_completado;
                END
            """)

    def verificar_procedimientos(self):
        """Verifica que los procedimientos fueron creados"""
        self.stdout.write("\n" + "="*60)
        self.stdout.write("VERIFICANDO STORED PROCEDURES:")
        self.stdout.write("="*60 + "\n")

        procedures = [
            'obtener_perfil_por_usuario',
            'iniciar_reto',
            'obtener_retos_por_tema',
            'solucionar_reto',
            'calcular_progreso_usuario'
        ]

        with connection.cursor() as cursor:
            for proc in procedures:
                cursor.execute(f"""
                    SELECT ROUTINE_NAME
                    FROM information_schema.ROUTINES
                    WHERE ROUTINE_SCHEMA = DATABASE()
                    AND ROUTINE_TYPE = 'PROCEDURE'
                    AND ROUTINE_NAME = '{proc}'
                """)
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS(f"  [OK] {proc}"))
                else:
                    self.stdout.write(self.style.ERROR(f"  [X] {proc} - NO ENCONTRADO"))
