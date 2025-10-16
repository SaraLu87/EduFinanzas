# EDUFINANZAS

## Introducción al Proyecto

**EDUFINANZAS** es una aplicación web educativa diseñada como un juego interactivo para enseñar conceptos de finanzas personales a usuarios de todas las edades. El objetivo es ayudar a los usuarios a aprender sobre ahorro, inversión, presupuestos, créditos y educación financiera avanzada a través de retos, progresos y tips periódicos.

La app consta de un **frontend** (interfaz de usuario) y un **backend** (servidor y base de datos) que interactúan mediante APIs. El frontend muestra datos como retos y perfiles, mientras que el backend maneja la lógica de datos con una base de datos MySQL.

### Para Nuevos Usuarios (Jugadores)

- **¿Qué puedes hacer?**

  - Registrarte como usuario y crear un perfil.
  - Explorar temas financieros (e.g., "Ahorro Personal", "Inversión Básica").
  - Completar retos (preguntas de selección única, verdadero/falso, etc.) para ganar monedas virtuales y avanzar en tu progreso.
  - Ver tu saldo, monedas y tips financieros personalizados.
  - Administradores pueden gestionar contenido (si tienes rol de admin).

- **Cómo empezar como usuario:**

  1. Abre el frontend en tu navegador (una vez que el proyecto esté corriendo localmente o desplegado).
  2. Regístrate con un correo y contraseña.
  3. Crea un perfil y comienza a explorar temas y retos.
  4. Responde retos para ganar recompensas y rastrear tu progreso.

- **Beneficios:**
  - Aprendizaje gamificado: Gana monedas por respuestas correctas.
  - Progreso personalizado: Ve qué retos has completado y tus tips semanales.
  - Vistas útiles: Resúmenes de perfiles, retos por temas y progresos completados.

Si eres un nuevo usuario, no necesitas instalar nada; solo accede a la app una vez que esté hospedada. Para probar localmente, sigue las instrucciones de instalación abajo.

## Requisitos Previos

Para correr el proyecto localmente (como desarrollador o para probar):

- **Sistema Operativo:** Windows, macOS o Linux.
- **Node.js:** Versión 18 o superior (descárgalo desde [nodejs.org](https://nodejs.org/)).
- **MySQL:** Instalado y corriendo (e.g., MySQL Community Server, XAMPP o MAMP). Puerto default: 3306.
- **Git:** Opcional, para clonar el repositorio.
- **Herramientas de prueba:** Postman o un navegador para probar APIs.
- **Base de Datos:** MySQL Workbench (opcional, para visualizar y ejecutar scripts SQL).

No se requieren dependencias adicionales para el usuario final; todo se maneja en el backend.

## Instalación Paso a Paso

Sigue estos pasos para configurar y correr el proyecto localmente. Asumimos que estás empezando desde cero.

### 1. Clona o Descarga el Proyecto

- Si usas Git:
  ```
  git clone https://github.com/tu-usuario/EDUFINANZAS.git
  cd EDUFINANZAS
  ```
- O descarga el ZIP del repositorio y extrae en una carpeta.

### 2. Configura la Base de Datos (MySQL)

- Inicia tu servidor MySQL (e.g., en XAMPP, inicia MySQL).
- Abre MySQL Workbench o la terminal de MySQL:
  ```
  mysql -u root -p
  ```
  (Ingresa tu contraseña de MySQL).
- Ejecuta el script SQL para crear la base de datos y cargar datos iniciales:

  ```
  SOURCE /ruta/a/EDUFINANZAS/backend/database/schema.sql;
  ```

  - Reemplaza `/ruta/a/` con la ruta absoluta de tu archivo `schema.sql`.
  - Esto crea la base `juego_finanzas_version_2` con tablas como `usuarios`, `temas`, `perfiles`, `retos`, `progreso` y `tips_periodicas`, más datos de prueba y vistas.

- Verifica:
  ```
  USE juego_finanzas_version_2;
  SHOW TABLES;
  SELECT * FROM usuarios;  -- Deberías ver 5 usuarios de prueba.
  ```

### 3. Instala Dependencias del Backend

- Navega al directorio backend:
  ```
  cd backend
  ```
- Instala las dependencias con npm:
  ```
  npm install
  ```
  - Esto instalará `express` y `mysql2` (y cualquier otra en `package.json`).

### 4. Configura el Backend

- Abre `backend/server.js` y ajusta la conexión a MySQL:
  ```javascript
  const db = mysql.createConnection({
    host: "localhost",
    user: "root", // Tu usuario de MySQL
    password: "tu_password", // Tu contraseña de MySQL
    database: "juego_finanzas_version_2",
  });
  ```
- Opcional: Usa un archivo `.env` para credenciales seguras (instala `dotenv` con `npm install dotenv` y ajusta el código).

### 5. Corre el Backend

- En la terminal, desde `backend`:
  ```
  node server.js
  ```
- Verifica: Abre un navegador y ve a `http://localhost:3001/api/test`. Deberías ver `{"message":"Conexión exitosa","result":2}`.
- Prueba APIs GET: e.g., `http://localhost:3001/api/usuarios` para ver usuarios.

### 6. Configura y Corre el Frontend

- Navega al directorio principal (si no estás ahí):
  ```
  cd ..
  ```
- Instala dependencias del frontend (asumiendo que usa Next.js o React, basado en carpetas como `app`, `components`):
  ```
  npm install
  ```
- Corre el frontend:
  ```
  npm run dev
  ```
- Abre `http://localhost:3000` en tu navegador. El frontend debería conectar con el backend (e.g., fetch a `http://localhost:3001/api/retos` para mostrar retos).

### 7. Prueba las APIs POST (para Desarrolladores)

- Usa Postman:
  - Método: POST
  - URL: e.g., `http://localhost:3001/api/usuarios`
  - Body (JSON): `{"correo": "test@mail.com", "contrasena": "pass123", "rol": "Usuario"}`
  - Deberías recibir `{"message":"Usuario creado","id":X}`.
- Similar para otras rutas POST.

## Estructura del Proyecto

- **app/**: Código del frontend (páginas, componentes, etc.).
- **backend/**: Código del servidor.
  - **config/**: Configuraciones.
  - **controllers/**: Lógica de controladores (si se usa MVC).
  - **database/**: Archivos relacionados con la DB.
    - `schema.sql`: Estructura SQL completa (tablas, inserts, vistas).
  - **middleware/**: Middlewares de Express.
  - **models/**: Modelos de datos (si se usa ORM).
  - **routes/**: Definiciones de rutas API.
  - `server.js`: Archivo principal del servidor.
- **components/**, **lib/**, **public/**, **styles/**: Recursos del frontend.
- **.gitignore**, **package.json**, etc.: Archivos de configuración.

## APIs Disponibles

El backend expone APIs REST en `http://localhost:3001/api/`:

### GET (Obtener Datos)

- `/usuarios`: Lista todos los usuarios.
- `/temas`: Lista todos los temas.
- `/perfiles`: Lista todos los perfiles.
- `/retos`: Lista todos los retos.
- `/progreso`: Lista todo el progreso.
- `/tips_periodicas`: Lista todos los tips periódicos.
- `/vista_retos_temas`: Vista de retos con temas asociados.

### POST (Crear Datos)

- `/usuarios`: Crea un usuario (body: {correo, contrasena, rol}).
- `/temas`: Crea un tema (body: {nombre, descripcion}).
- `/perfiles`: Crea un perfil (body: {id_usuario, nombre_perfil, foto_perfil, tema_actual, monedas, saldo}).
- `/retos`: Crea un reto (body: {tipo_pregunta, nombre_reto, id_tema, descripcion, recompensa_monedas, respuesta_uno, ...}).
- `/progreso`: Crea un progreso (body: {id_perfil, id_reto, completado, fecha_completado, respuesta_seleccionada}).
- `/tips_periodicas`: Crea un tip (body: {id_perfil, nombre, descripcion}).

## Notas Adicionales

- **Seguridad:** En producción, hashea contraseñas (agrega `bcrypt`). Usa HTTPS.
- **Despliegue:** Para hospedar, usa Vercel para frontend/backend y PlanetScale para MySQL.
- **Problemas Comunes:** Si falla la conexión, verifica MySQL corriendo y credenciales correctas.
- **Contribuciones:** Si eres desarrollador, agrega rutas PUT/DELETE para updates/eliminaciones.
- **Versión:** Basado en desarrollo hasta octubre 2025.
