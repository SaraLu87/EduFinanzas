#!/usr/bin/env python
"""
Script para crear o actualizar usuario administrador en EduFinanzas

Uso:
    python crear_admin.py
"""

import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.contrib.auth.hashers import make_password
import MySQLdb

def crear_admin():
    """Crear o actualizar usuario administrador"""

    print("\n" + "="*50)
    print("   CREAR USUARIO ADMINISTRADOR - EduFinanzas")
    print("="*50 + "\n")

    # Solicitar datos
    correo = input("📧 Ingresa el correo del admin [admin@edufinanzas.com]: ").strip()
    if not correo:
        correo = "admin@edufinanzas.com"
        print(f"   → Usando: {correo}")

    contrasena = input("🔑 Ingresa la contraseña [admin123]: ").strip()
    if not contrasena:
        contrasena = "admin123"
        print(f"   → Usando: {contrasena}")

    print("\n" + "-"*50)

    # Hashear contraseña
    print("🔐 Hasheando contraseña...")
    contrasena_hash = make_password(contrasena)
    print(f"   Hash generado: {contrasena_hash[:40]}...")

    # Conectar a MySQL
    print("\n📡 Conectando a MySQL...")
    try:
        db = MySQLdb.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="123456789",
            db="juego_finanzas"
        )
        cursor = db.cursor()
        print("   ✅ Conexión establecida")

        # Verificar si el correo ya existe
        print(f"\n🔍 Verificando si {correo} ya existe...")
        cursor.execute(
            "SELECT id_usuario, rol FROM usuarios WHERE correo = %s",
            (correo,)
        )
        resultado = cursor.fetchone()

        if resultado:
            id_usuario, rol_actual = resultado
            print(f"   ⚠️  El usuario ya existe (ID: {id_usuario}, Rol: {rol_actual})")
            print("\n¿Qué deseas hacer?")
            print("1. Actualizar contraseña")
            print("2. Actualizar contraseña y cambiar rol a Administrador")
            print("3. Cancelar")

            opcion = input("\nSelecciona una opción [1/2/3]: ").strip()

            if opcion == "1":
                cursor.execute(
                    "UPDATE usuarios SET contrasena = %s WHERE correo = %s",
                    (contrasena_hash, correo)
                )
                db.commit()
                print(f"\n✅ Contraseña actualizada exitosamente!")

            elif opcion == "2":
                cursor.execute(
                    """UPDATE usuarios
                       SET contrasena = %s, rol = 'Administrador'
                       WHERE correo = %s""",
                    (contrasena_hash, correo)
                )
                db.commit()
                print(f"\n✅ Contraseña y rol actualizados exitosamente!")

            elif opcion == "3":
                print("\n❌ Operación cancelada")
                cursor.close()
                db.close()
                return
            else:
                print("\n❌ Opción inválida. Operación cancelada.")
                cursor.close()
                db.close()
                return
        else:
            # Insertar nuevo usuario
            print("   ℹ️  El usuario no existe. Creando nuevo...")
            cursor.execute(
                """INSERT INTO usuarios (correo, contrasena, rol)
                   VALUES (%s, %s, 'Administrador')""",
                (correo, contrasena_hash)
            )
            db.commit()

            # Obtener ID del usuario creado
            id_usuario = cursor.lastrowid
            print(f"\n✅ Usuario administrador creado exitosamente!")
            print(f"   ID: {id_usuario}")

        # Resumen
        print("\n" + "="*50)
        print("   📝 RESUMEN DE CREDENCIALES")
        print("="*50)
        print(f"\n📧 Correo:     {correo}")
        print(f"🔑 Contraseña: {contrasena}")
        print(f"👤 Rol:        Administrador")
        print(f"\n🌐 URL Login:  http://localhost:5173/login")
        print("\n🎉 ¡Puedes iniciar sesión ahora!")
        print("="*50 + "\n")

        cursor.close()
        db.close()

    except MySQLdb.Error as e:
        print(f"\n❌ Error de MySQL: {e}")
        print("\n💡 Verifica que:")
        print("   - MySQL esté corriendo")
        print("   - La base de datos 'juego_finanzas' exista")
        print("   - Las credenciales de conexión sean correctas")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        crear_admin()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(0)
