Apis creadas

---

## 🧩 1️⃣ AUTH (Autenticación)

| Método   | Endpoint        | Descripción                                   | Body JSON                                                                                                     |
| -------- | --------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **GET**  | `/api/test-db`  | Verifica la conexión a la base de datos MySQL | —                                                                                                             |
| **POST** | `/api/register` | Registra un nuevo usuario y crea su perfil    | `json { "correo": "usuario@ejemplo.com", "contrasena": "1234", "rol": "Usuario", "nombre_perfil": "Bicho" } ` |
| **POST** | `/api/login`    | Inicia sesión de un usuario                   | `json { "correo": "usuario@ejemplo.com", "contrasena": "1234" } `                                             |

---

## 🧩 2️⃣ PERFIL (Perfil del jugador)

| Método   | Endpoint                          | Descripción                            | Body JSON                                                                |
| -------- | --------------------------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| **GET**  | `/api/perfil/<id_usuario>`        | Obtiene el perfil de un usuario        | —                                                                        |
| **PUT**  | `/api/perfil/editar/<id_usuario>` | Edita el nombre del perfil o el correo | `json { "nombre_perfil": "NuevoNombre", "correo": "nuevo@correo.com" } ` |
| **POST** | `/api/monedas/agregar`            | Agrega monedas al perfil               | `json { "id_usuario": 1, "cantidad": 100 } `                             |
| **POST** | `/api/saldo/actualizar`           | Actualiza el saldo del perfil          | `json { "id_usuario": 1, "nuevo_saldo": 250.50 } `                       |

---

## 🧩 3️⃣ TEMAS (Gestión de temas)

| Método   | Endpoint     | Descripción                        | Body JSON                                                                                  |
| -------- | ------------ | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| **GET**  | `/api/temas` | Obtiene todos los temas existentes | —                                                                                          |
| **POST** | `/api/temas` | Crea un nuevo tema                 | `json { "nombre": "Finanzas Personales", "descripcion": "Aprende a manejar tu dinero." } ` |

---

## 🧩 4️⃣ RETOS (Preguntas y desafíos)

| Método   | Endpoint     | Descripción                                  | Body JSON                                                                                                                                                                                                                                                                                                                                                     |
| -------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GET**  | `/api/retos` | Obtiene todos los retos con su tema asociado | —                                                                                                                                                                                                                                                                                                                                                             |
| **POST** | `/api/retos` | Crea un nuevo reto                           | `json { "tipo_pregunta": "opcion_multiple", "nombre_reto": "Ahorro inteligente", "id_tema": 1, "descripcion": "Elige la mejor opción de ahorro", "recompensa_monedas": 20, "respuesta_uno": "Gastar todo", "respuesta_dos": "Ahorrar el 10%", "respuesta_tres": "Ahorrar el 50%", "respuesta_cuatro": "No ahorrar", "respuestaCorrecta": "Ahorrar el 10%" } ` |

---

## 🧩 5️⃣ PROGRESO (Seguimiento de retos)

| Método   | Endpoint                    | Descripción                                          | Body JSON                                                                            |
| -------- | --------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **GET**  | `/api/progreso/<id_perfil>` | Obtiene el progreso (retos completados) de un perfil | —                                                                                    |
| **POST** | `/api/progreso/actualizar`  | Marca un reto como completado                        | `json { "id_perfil": 1, "id_reto": 2, "respuesta_seleccionada": "Ahorrar el 10%" } ` |

---

## 🧩 6️⃣ TIPS (Consejos o recompensas periódicas)

| Método   | Endpoint                | Descripción                            | Body JSON                                                                                                                      |
| -------- | ----------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **GET**  | `/api/tips/<id_perfil>` | Obtiene los tips asociados a un perfil | —                                                                                                                              |
| **POST** | `/api/tips`             | Crea un nuevo tip                      | `json { "id_perfil": 1, "nombre": "Ahorra cada semana", "descripcion": "Guarda al menos el 10% de tus ingresos semanales." } ` |

---

## 🌐 RESUMEN GLOBAL

✅ **Total de endpoints:** 16
📦 **Módulos:** 6
💾 **Base de datos:** `juego_finanzas_version_2`
🧠 **Estructura:** `routes/` + `controllers/` con conexión desde `db.py`

---

¿Quieres que ahora te genere el archivo `.json` de **Postman Collection** con todos estos endpoints listos para importar y probar directamente (ya con los `body` preconfigurados)?
Así solo haces:

> 🧠 _“Import → Postman → EduFinanzas API v1.json”_
> y empiezas a testear de una.
