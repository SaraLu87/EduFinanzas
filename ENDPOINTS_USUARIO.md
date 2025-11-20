# API Endpoints para Usuario Autenticado

## Resumen
Endpoints creados para la funcionalidad de usuario logueado. Todos estos endpoints requieren el token JWT en el header `Authorization: Bearer <token>`.

---

## 1. Perfil del Usuario

### GET `/api/perfil/me/`
**Descripción:** Obtiene el perfil del usuario autenticado

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Response 200:**
```json
{
  "id_perfil": 1,
  "id_usuario": 1,
  "nombre_perfil": "Juan",
  "edad": 25,
  "foto_perfil": "perfiles/default.png",
  "monedas": 100
}
```

---

### PUT `/api/perfil/me/update/`
**Descripción:** Actualiza nombre_perfil y/o contraseña del usuario autenticado

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Body (JSON):**
```json
{
  "nombre_perfil": "Nuevo Nombre",  // Opcional
  "contrasena": "nueva123"          // Opcional
}
```

**Response 200:**
```json
{
  "message": "Perfil actualizado exitosamente",
  "perfil": {
    "id_perfil": 1,
    "id_usuario": 1,
    "nombre_perfil": "Nuevo Nombre",
    "edad": 25,
    "foto_perfil": "perfiles/default.png",
    "monedas": 100
  }
}
```

---

## 2. Progreso del Usuario

### GET `/api/perfil/me/progreso/`
**Descripción:** Obtiene el progreso general del usuario (retos completados)

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Response 200:**
```json
{
  "total_retos": 10,
  "retos_completados": 3,
  "porcentaje_completado": 30.00
}
```

---

## 3. Retos por Tema

### GET `/api/temas/<id_tema>/retos/`
**Descripción:** Obtiene todos los retos de un tema con el progreso del usuario

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Ejemplo:** `GET /api/temas/1/retos/`

**Response 200:**
```json
[
  {
    "id_reto": 1,
    "nombre_reto": "¿Qué es un presupuesto?",
    "id_tema": 1,
    "descripcion": "Aprende sobre presupuestos",
    "pregunta": "¿Cuál es la definición correcta?",
    "img_reto": "retos/reto1.png",
    "recompensa_monedas": 50,
    "costo_monedas": 10,
    "respuesta_uno": "Opción A",
    "respuesta_dos": "Opción B",
    "respuesta_tres": "Opción C",
    "respuesta_cuatro": "Opción D",
    "id_progreso": 5,        // NULL si no iniciado
    "completado": true,      // NULL si no iniciado, false si iniciado, true si completado
    "fecha_completado": "2025-11-20 10:30:00",  // NULL si no completado
    "respuesta_seleccionada": "Opción A"         // NULL si no ha respondido
  },
  ...
]
```

**Notas:**
- Si `id_progreso` es `null`, el usuario NO ha iniciado el reto
- Si `completado` es `null`, el reto NO ha sido iniciado
- Si `completado` es `false`, el reto está en progreso pero no completado
- Si `completado` es `true`, el reto está completado
- La `respuestaCorrecta` NO se incluye por seguridad

---

## 4. Iniciar Reto

### POST `/api/retos/<id_reto>/iniciar/`
**Descripción:** Compra/inicia un reto descontando las monedas del perfil

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Ejemplo:** `POST /api/retos/1/iniciar/`

**Body:** No requiere body (el id_perfil se obtiene del token)

**Response 201:**
```json
{
  "message": "Reto iniciado exitosamente",
  "progreso": {
    "id_progreso": 10,
    "id_perfil": 1,
    "id_reto": 1,
    "completado": null,
    "fecha_completado": null,
    "respuesta_seleccionada": null
  },
  "perfil": {
    "id_perfil": 1,
    "id_usuario": 1,
    "nombre_perfil": "Juan",
    "edad": 25,
    "foto_perfil": "perfiles/default.png",
    "monedas": 90  // Monedas descontadas
  }
}
```

**Response 400 (Monedas insuficientes):**
```json
{
  "detail": "No tienes suficientes monedas para iniciar este reto"
}
```

**Response 201 (Reto ya iniciado):**
Si el reto ya fue iniciado, retorna el progreso existente sin descontar monedas

---

## 5. Solucionar Reto (Endpoint existente)

### POST `/api/solucionar_reto/`
**Descripción:** Envía la respuesta seleccionada para un reto. Si es correcta, marca como completado y agrega recompensa

**Body (JSON):**
```json
{
  "id_perfil": 1,
  "id_reto": 1,
  "respuesta_seleccionada": "Opción A"
}
```

**Response 200 (Respuesta correcta):**
```json
[
  {
    "id_progreso": 10,
    "id_perfil": 1,
    "id_reto": 1,
    "completado": true,
    "fecha_completado": "2025-11-20 11:30:00",
    "respuesta_seleccionada": "Opción A"
  }
]
```

**Response 400 (Respuesta incorrecta):**
```json
{
  "mensaje": "Respuesta incorrecta o sin cambios en el progreso."
}
```

**Notas:**
- Debe iniciar el reto primero con `/api/retos/<id_reto>/iniciar/`
- Si la respuesta es correcta, agrega `recompensa_monedas` al perfil
- Si ya está completado, retorna el progreso sin cambios

---

## 6. Endpoints Existentes (Sin modificar)

### GET `/api/temas/`
Listar todos los temas

### GET `/api/tips/`
Listar todos los tips periódicos

### POST `/api/login_usuario/`
Login de usuario

### POST `/api/registro/`
Registro de usuario

---

## Flujo Completo del Usuario

1. **Registro:** `POST /api/registro/`
2. **Login:** `POST /api/login_usuario/` → Obtiene token JWT
3. **Ver perfil:** `GET /api/perfil/me/` (con token)
4. **Ver progreso:** `GET /api/perfil/me/progreso/` (con token)
5. **Ver temas:** `GET /api/temas/`
6. **Ver retos de un tema:** `GET /api/temas/1/retos/` (con token)
7. **Iniciar reto:** `POST /api/retos/1/iniciar/` (con token)
8. **Solucionar reto:** `POST /api/solucionar_reto/`
9. **Actualizar perfil:** `PUT /api/perfil/me/update/` (con token)

---

## Stored Procedures Creados

1. `obtener_perfil_por_usuario(id_usuario)` - Obtiene perfil desde id_usuario
2. `iniciar_reto(id_perfil, id_reto)` - Valida monedas y crea progreso
3. `obtener_retos_por_tema(id_tema, id_perfil)` - Lista retos con progreso del usuario
4. `solucionar_reto(id_perfil, id_reto, respuesta)` - Valida respuesta y agrega recompensa
5. `calcular_progreso_usuario(id_perfil)` - Calcula porcentaje de completitud

---

## Autenticación

Todos los endpoints de usuario requieren el token JWT en el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

El token se obtiene del endpoint de login y contiene:
- `id_usuario`: ID del usuario
- `correo`: Email del usuario

El backend extrae automáticamente el perfil asociado al usuario desde el token.
