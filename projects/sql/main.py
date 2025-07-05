from db import SessionLocal, init_db
from auth import register_user, authenticate_user

def main():
    init_db()
    db = SessionLocal()

    print("Bienvenido al sistema de registro y autenticación")
    while True:
        print("\nOpciones:")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            username = input("Nombre de usuario: ")
            email = input("Correo electrónico: ")
            password = input("Contraseña: ")
            if register_user(db, username, email, password):
                print("Usuario registrado exitosamente.")
            else:
                print("El usuario o correo ya existe.")
        elif opcion == "2":
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            if authenticate_user(db, username, password):
                print("¡Inicio de sesión exitoso!")
            else:
                print("Usuario o contraseña incorrectos.")
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

    db.close()

if __name__ == "__main__":
    main()