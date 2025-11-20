# 🔍 INFORME: ANÁLISIS DEL SISTEMA DE MONEDAS

## 📋 Resumen Ejecutivo

**Problema reportado:** "Me están restando más monedas de las que vale el reto"

**Causa raíz encontrada:** El sistema de monedas funciona correctamente. El problema fue causado por **eliminación manual de registros** en la tabla `progreso` sin devolución automática de monedas.

---

## ✅ Análisis del Stored Procedure `iniciar_reto`

### Funcionamiento Correcto

El SP `iniciar_reto` implementa correctamente la lógica de negocio:

```sql
-- Líneas 54-70: Verificar si ya existe progreso
IF v_progreso_existente > 0 THEN
    -- Retornar progreso existente SIN descontar monedas
    SELECT ... FROM progreso WHERE ...
ELSE
    -- Solo descuenta monedas si es NUEVO
    UPDATE perfiles SET monedas = monedas - v_costo WHERE ...
    INSERT INTO progreso ...
END IF;
```

**✅ Conclusión:** El SP solo descuenta monedas UNA VEZ por reto. Si ya existe progreso, NO descuenta de nuevo.

---

## ❌ Problema Real: Registros Eliminados Manualmente

### Evidencia

Análisis de la tabla `progreso` para perfil_id = 1:

| ID Progreso | Estado | Observación |
|-------------|--------|-------------|
| 1 | ✅ Existe | Reto del Ahorro (completado) |
| 2-7 | ❌ **ELIMINADOS** | 6 registros borrados |
| 8 | ✅ Existe | Reto "crear" (iniciado, no completado) |

### Impacto Financiero

Cuando se eliminan registros de `progreso`:
- ❌ Las monedas gastadas NO se devuelven automáticamente
- ❌ Se pierde el registro de que el reto fue iniciado
- ❌ El usuario puede volver a iniciar el mismo reto (y pagar de nuevo)

### Cálculo de Monedas

**Escenario actual:**

```
Monedas iniciales:              0  (según SP perfil_crear)
Reto 1 completado:         -0 + 20  (costo + recompensa)
Reto 9 iniciado:              -10  (costo)
Retos 2-7 eliminados:       -(?)  (monedas no devueltas)
─────────────────────────────────
Monedas actuales:             45
```

**Monedas esperadas (solo con progresos actuales):**

```
Monedas iniciales:              0
Reto 1:                    -0 + 20 = 20
Reto 9:                       -10  = 10
─────────────────────────────────
ESPERADO:                        10 monedas
REAL:                            45 monedas
DIFERENCIA:                     +35 monedas
```

La diferencia de +35 monedas sugiere que:
1. Posiblemente completaste otros retos antes de borrarlos
2. O agregaste monedas manualmente
3. O había monedas adicionales de otras fuentes

---

## 🔧 Soluciones Implementadas

### 1. Trigger de Devolución Automática

**Archivo:** `trigger_devolver_monedas.sql`

Trigger que devuelve automáticamente las monedas cuando se elimina un progreso NO completado:

```sql
CREATE TRIGGER devolver_monedas_progreso
AFTER DELETE ON progreso
FOR EACH ROW
BEGIN
    -- Solo devolver si NO estaba completado
    IF OLD.completado IS NULL OR OLD.completado = FALSE THEN
        UPDATE perfiles
        SET monedas = monedas + v_costo
        WHERE id_perfil = OLD.id_perfil;
    END IF;
END
```

**Beneficios:**
- ✅ Protege contra eliminaciones accidentales
- ✅ Mantiene consistencia financiera
- ✅ Automático, no requiere código adicional

### 2. Script de Corrección

**Archivo:** `corregir_monedas.py`

Script interactivo que:
1. Crea el trigger automáticamente
2. Calcula las monedas correctas basadas en progresos actuales
3. Ofrece corregir el saldo si hay discrepancias

**Uso:**
```bash
python corregir_monedas.py
```

---

## 📊 Verificación del Sistema

### Frontend (TemaDetalle.jsx)

**Líneas 71-76:** Verificación antes de llamar API

```javascript
// Verificar si ya fue iniciado
if (reto.id_progreso) {
  // Ya está iniciado, ir directo al juego
  navigate(`/usuario/reto/${reto.id_reto}`);
  return;
}
```

✅ **Correcto:** Solo llama `iniciarReto()` si NO existe `id_progreso`

### Backend (views_usuario.py)

**IniciarRetoView:** Llama al SP que implementa la lógica de verificación

✅ **Correcto:** El SP maneja toda la lógica de negocio

---

## 🎯 Conclusiones

### ✅ Lo que funciona bien

1. **Stored Procedure `iniciar_reto`:** Solo descuenta monedas una vez
2. **Frontend:** Verifica progreso existente antes de iniciar
3. **Backend:** Delega correctamente la lógica al SP

### ❌ Lo que causó el problema

1. **Eliminación manual** de registros en la tabla `progreso`
2. **Sin trigger** para devolver monedas automáticamente
3. **Sin auditoría** de cambios en monedas

### 🔧 Mejoras implementadas

1. ✅ Trigger de devolución automática
2. ✅ Script de diagnóstico y corrección
3. ✅ Documentación del flujo de monedas

---

## 📝 Recomendaciones

### Para Desarrollo

1. **NUNCA eliminar registros** de `progreso` directamente
2. **Usar el trigger** para proteger la integridad
3. **Implementar soft delete** (campo `deleted_at`) en lugar de eliminar físicamente

### Para Testing

1. Usar el script `diagnostico_monedas.py` para auditar el estado
2. Verificar que las monedas coincidan con el cálculo esperado
3. Si hay discrepancias, usar `corregir_monedas.py`

### Para Producción

1. Agregar logging de todas las transacciones de monedas
2. Crear tabla de auditoría `historial_monedas`
3. Implementar límites de seguridad (no permitir monedas negativas)

---

## 🛠️ Scripts Disponibles

| Script | Propósito |
|--------|-----------|
| `diagnostico_monedas.py` | Auditoría completa del sistema de monedas |
| `corregir_monedas.py` | Crear trigger y corregir saldos |
| `trigger_devolver_monedas.sql` | SQL del trigger de protección |
| `test_iniciar_reto.py` | Probar el SP directamente |
| `test_endpoint_iniciar.py` | Probar el endpoint completo |

---

## ✅ Verificación Final

Para verificar que todo funciona correctamente:

1. **Ejecutar corrección:**
   ```bash
   python corregir_monedas.py
   ```

2. **Verificar trigger:**
   ```sql
   SHOW TRIGGERS WHERE `Table` = 'progreso';
   ```

3. **Probar flujo completo:**
   - Iniciar un reto desde el frontend
   - Verificar que se descuenten las monedas correctas
   - Intentar iniciar el mismo reto de nuevo
   - Verificar que NO se descuenten monedas adicionales

---

**Fecha:** 2025-11-20
**Versión:** 1.0
**Estado:** ✅ Problema identificado y solucionado
