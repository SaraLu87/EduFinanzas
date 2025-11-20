# 🔍 INFORME COMPLETO: BUG DE MONEDAS DUPLICADAS

**Fecha:** 2025-11-20
**Usuario afectado:** sara.munoz.q@uniautonoma.edu.co
**Problema reportado:** "Al realizar el segundo reto me resta 10 monedas cuando deberían ser solo 5"

---

## 📋 RESUMEN EJECUTIVO

**Problema:** El sistema restaba monedas **DOS VECES** al iniciar un reto.

**Causa raíz:** Trigger duplicado `trg_restar_monedas_al_jugar_reto` que se ejecutaba además del stored procedure `iniciar_reto`.

**Solución:** Eliminar el trigger `trg_restar_monedas_al_jugar_reto`.

**Estado:** ✅ **RESUELTO Y VERIFICADO**

---

## 🔴 REPRODUCCIÓN DEL PROBLEMA

### Escenario de Prueba

**Usuario:** Sara (ID Perfil: 15)
**Estado inicial:** 0 monedas, sin progresos

### Flujo Ejecutado

1. **Primer reto (ID 1 - "Reto del Ahorro")**
   - Costo: 0 monedas
   - Recompensa: 20 monedas
   - Resultado: ✅ Funcionó correctamente
   - Monedas finales: 20

2. **Segundo reto (ID 8 - "reto 2")**
   - Costo esperado: 5 monedas
   - **Monedas descontadas: 10** ❌
   - Monedas finales: 10 (debería ser 15)

3. **Tercer reto (ID 9 - "crear", Tema 2)**
   - Costo: 10 monedas
   - Monedas disponibles: 10
   - Resultado: ❌ Error "No tienes suficientes monedas"
   - Causa: Faltaban 5 monedas por el descuento duplicado anterior

---

## 🔎 ANÁLISIS DE LA CAUSA RAÍZ

### Investigación Paso a Paso

#### 1. Verificación de costos en BD
```sql
SELECT id_reto, nombre_reto, costo_monedas FROM retos WHERE id_reto = 8;
```
**Resultado:** Costo correcto = 5 monedas ✅

#### 2. Debug del Stored Procedure
Ejecuté `iniciar_reto(15, 8)` con trazas:
- Variable `v_costo` dentro del SP: **5** ✅
- Monedas antes del INSERT: 20
- Monedas después del INSERT: **10** ❌
- **Conclusión:** El SP descuenta correctamente, pero algo más descuenta 5 adicionales

#### 3. Búsqueda de Triggers
```sql
SHOW TRIGGERS;
```

**ENCONTRADO:** Trigger `trg_restar_monedas_al_jugar_reto`

```sql
CREATE TRIGGER trg_restar_monedas_al_jugar_reto
BEFORE INSERT ON progreso
FOR EACH ROW
BEGIN
  DECLARE v_costo INT DEFAULT 0;

  SELECT costo_monedas INTO v_costo
  FROM retos
  WHERE id_reto = NEW.id_reto;

  UPDATE perfiles
  SET monedas = monedas - v_costo
  WHERE id_perfil = NEW.id_perfil;
END
```

### Flujo del Bug

```
1. Usuario llama endpoint POST /api/retos/8/iniciar/
                ↓
2. Backend llama iniciar_reto_service(15, 8)
                ↓
3. SP iniciar_reto ejecuta:
   a. Obtiene costo del reto: v_costo = 5
   b. Verifica monedas suficientes: OK
   c. UPDATE perfiles SET monedas = monedas - 5  [20 → 15] ✅
   d. INSERT INTO progreso (...)
                ↓
4. Trigger trg_restar_monedas_al_jugar_reto SE DISPARA:
   a. Obtiene costo del reto: v_costo = 5
   b. UPDATE perfiles SET monedas = monedas - 5  [15 → 10] ❌
                ↓
5. RESULTADO: Se restaron 10 monedas en total
```

---

## 🎯 CAUSA RAÍZ IDENTIFICADA

**Responsabilidad Duplicada:**

| Componente | Acción | Estado |
|------------|--------|--------|
| **SP `iniciar_reto`** (línea 39-40) | `UPDATE perfiles SET monedas = monedas - v_costo` | ✅ Correcto |
| **Trigger `trg_restar_monedas_al_jugar_reto`** | `UPDATE perfiles SET monedas = monedas - v_costo` | ❌ Duplicado |

**Ambos** componentes restaban las monedas, causando el descuento doble.

---

## ✅ SOLUCIÓN IMPLEMENTADA

### Acción Correctiva

**Eliminar el trigger duplicado:**

```sql
DROP TRIGGER IF EXISTS trg_restar_monedas_al_jugar_reto;
```

### Justificación

El stored procedure `iniciar_reto` **YA TIENE** toda la lógica necesaria:

1. ✅ Verificar si el progreso ya existe
2. ✅ Verificar monedas suficientes
3. ✅ Descontar monedas
4. ✅ Insertar registro de progreso
5. ✅ Retornar progreso creado o existente

**El trigger es redundante y causa el bug.**

### Triggers Mantenidos

| Trigger | Propósito | Estado |
|---------|-----------|--------|
| `trg_sumar_monedas_al_completar_reto` | Agregar recompensa al completar reto | ✅ Mantener |
| `devolver_monedas_progreso` | Devolver monedas al eliminar progreso | ✅ Mantener |

---

## 🧪 VERIFICACIÓN DE LA SOLUCIÓN

### Prueba Completa Post-Corrección

**Usuario:** Sara (ID Perfil: 15)
**Estado inicial:** 0 monedas, sin progresos

| Paso | Reto | Costo | Monedas Antes | Monedas Después | Descuento | Estado |
|------|------|-------|---------------|-----------------|-----------|--------|
| 1 | Reto 1 (Ahorro) | 0 | 0 | 0 | 0 | ✅ OK |
| 1 (completar) | Reto 1 | +20 | 0 | 20 | +20 | ✅ OK |
| 2 | Reto 8 (reto 2) | 5 | 20 | 15 | **5** ✅ | ✅ **CORREGIDO** |
| 3 | Reto 9 (crear) | 10 | 15 | 5 | 10 | ✅ OK |

**Resultado:** ✅ Todos los descuentos son correctos

---

## 📊 IMPACTO Y ALCANCE

### Usuarios Afectados

**Todos los usuarios** que hayan iniciado retos desde la creación del trigger.

### Cálculo del Impacto

Para cada reto iniciado:
- Monedas esperadas descontadas: `costo_reto`
- Monedas realmente descontadas: `costo_reto * 2` ❌
- **Pérdida por reto:** `costo_reto` monedas

**Ejemplo con Sara:**
- Reto 8: Perdió 5 monedas extra
- Total acumulado de sobrecosto: 5 monedas

### Acciones Recomendadas

1. ✅ **Inmediato:** Trigger eliminado
2. ⚠️ **Pendiente:** Auditar cuentas de todos los usuarios
3. ⚠️ **Pendiente:** Compensar monedas perdidas

---

## 🔧 SCRIPT DE COMPENSACIÓN

Para corregir las cuentas de los usuarios afectados:

```sql
-- Calcular monedas que deberían tener basado en progresos actuales
SELECT
    p.id_perfil,
    perf.nombre_perfil,
    perf.monedas AS monedas_actuales,
    -- Monedas iniciales (0) - gastado + ganado
    (0 - COALESCE(SUM(CASE WHEN pr.completado IS NULL OR pr.completado = FALSE THEN r.costo_monedas ELSE 0 END), 0)
       + COALESCE(SUM(CASE WHEN pr.completado = TRUE THEN r.recompensa_monedas ELSE 0 END), 0)) AS monedas_esperadas,
    (perf.monedas - (0 - COALESCE(SUM(CASE WHEN pr.completado IS NULL OR pr.completado = FALSE THEN r.costo_monedas ELSE 0 END), 0)
       + COALESCE(SUM(CASE WHEN pr.completado = TRUE THEN r.recompensa_monedas ELSE 0 END), 0))) AS diferencia
FROM perfiles perf
LEFT JOIN progreso pr ON perf.id_perfil = pr.id_perfil
LEFT JOIN retos r ON pr.id_reto = r.id_reto
LEFT JOIN usuarios u ON perf.id_usuario = u.id_usuario
WHERE u.rol = 'Usuario'
GROUP BY p.id_perfil, perf.nombre_perfil, perf.monedas
HAVING diferencia <> 0;
```

---

## 📝 LECCIONES APRENDIDAS

### Problemas Identificados

1. **Duplicación de lógica** entre SP y triggers
2. **Falta de pruebas unitarias** para verificar transacciones
3. **Sin auditoría** de cambios en monedas

### Mejoras Recomendadas

#### 1. Arquitectura

- ✅ **Centralizar lógica de negocio** en stored procedures
- ✅ **Triggers solo para auditoría**, no para lógica de negocio
- ⚠️ Implementar **tabla de auditoría** `historial_monedas`

```sql
CREATE TABLE historial_monedas (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_perfil INT NOT NULL,
    monto_anterior INT NOT NULL,
    monto_nuevo INT NOT NULL,
    diferencia INT NOT NULL,
    motivo ENUM('iniciar_reto', 'completar_reto', 'eliminar_progreso', 'admin_ajuste'),
    id_reto INT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
);
```

#### 2. Testing

- ⚠️ Crear **suite de pruebas** para flujos de monedas
- ⚠️ Verificar que cada operación descuente/agregue monedas **UNA SOLA VEZ**
- ⚠️ Pruebas de integración para SP + triggers

#### 3. Monitoreo

- ⚠️ Alertas cuando las monedas no coincidan con el cálculo esperado
- ⚠️ Dashboard de auditoría para administradores
- ⚠️ Logs detallados de todas las transacciones de monedas

---

## 🎯 ACCIONES PENDIENTES

### Prioridad Alta

- [ ] Auditar cuentas de todos los usuarios
- [ ] Crear script de compensación automática
- [ ] Ejecutar compensación para usuarios afectados
- [ ] Notificar a usuarios sobre la corrección

### Prioridad Media

- [ ] Implementar tabla `historial_monedas`
- [ ] Crear trigger de auditoría (solo logging)
- [ ] Suite de pruebas automatizadas
- [ ] Dashboard de auditoría

### Prioridad Baja

- [ ] Documentar arquitectura de transacciones
- [ ] Guía de mejores prácticas para triggers
- [ ] Review de todos los triggers existentes

---

## 📚 ARCHIVOS RELACIONADOS

### Scripts Creados

| Archivo | Propósito |
|---------|-----------|
| `test_flujo_sara.py` | Test completo que reproduce el bug |
| `debug_sp_iniciar_reto.py` | Debug paso a paso del SP |
| `crear_sp_debug.py` | Verificar valores dentro del SP |
| `corregir_trigger_duplicado.py` | Script de corrección del bug |
| `INFORME_BUG_TRIGGER_DUPLICADO.md` | Este documento |

### Componentes Afectados

| Componente | Archivo | Estado |
|------------|---------|--------|
| SP `iniciar_reto` | `stored_procedures_user_features.sql` | ✅ Correcto |
| Trigger `trg_restar_monedas_al_jugar_reto` | Base de datos | ❌ Eliminado |
| Endpoint `IniciarRetoView` | `retos/views_usuario.py` | ✅ Sin cambios |
| Service `iniciar_reto_service` | `progresos/services.py` | ✅ Sin cambios |

---

## ✅ CONCLUSIÓN

**Bug identificado, corregido y verificado con éxito.**

El problema fue causado por un **trigger duplicado** que restaba monedas además del stored procedure. La solución fue **eliminar el trigger** ya que el SP maneja correctamente toda la lógica.

**Próximos pasos:**
1. Auditar y compensar usuarios afectados
2. Implementar mejoras de arquitectura y monitoreo
3. Crear suite de pruebas para prevenir regresiones

---

**Responsable:** Claude Code
**Revisado:** Pendiente
**Aprobado:** Pendiente

---

## 🔗 REFERENCIAS

- [stored_procedures_user_features.sql](stored_procedures_user_features.sql) - Definición del SP `iniciar_reto`
- [retos/views_usuario.py](retos/views_usuario.py) - Endpoint que llama al SP
- [test_flujo_sara.py](test_flujo_sara.py) - Test de reproducción y verificación
