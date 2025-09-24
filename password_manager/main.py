from .password_manager import PasswordManager
import getpass
from prettytable import PrettyTable
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal que ejecuta la interfaz de usuario."""
    master_password = getpass.getpass("Ingresa tu contraseña maestra: ")

    try:
        manager = PasswordManager(master_password)
        print("¡Acceso concedido!")
    except Exception as e:
        print(f"Error de autenticación o archivo corrupto: {e}")
        return

    while True:
        clear_screen()
        print("\n--- Gestor de Contraseñas ---")
        print("1. Agregar una nueva contraseña")
        print("2. Listar contraseñas guardadas")
        print("3. Obtener una contraseña")
        print("4. Eliminar una contraseña")
        print("5. Cambiar contraseña maestra")
        print("6. Salir")
        
        choice = input("Selecciona una opción: ")

        if choice == '1':
            service = input("Servicio (ej. Google, Facebook): ")
            username = input("Nombre de usuario: ")
            password = getpass.getpass("Contraseña: ")
            manager.add_password(service, username, password)
            print("Contraseña guardada con éxito.")
            input("\nPresiona Enter para continuar...")
        
        elif choice == '2':
            passwords_data = manager.list_passwords()
            if passwords_data:
                print("Servicios guardados:")
                table = PrettyTable()
                table.field_names = ["ID", "Servicio", "Usuario"]
                for item in passwords_data:
                    table.add_row([item['id'], item['servicio'], item['usuario']])
                print(table)
            else:
                print("No hay contraseñas guardadas.")
            input("\nPresiona Enter para continuar...")

        elif choice == '3':
            service = input("¿De qué servicio quieres la contraseña?: ")
            password = manager.get_password(service)
            if password:
                print(f"Contraseña para {service}: {password}")
            else:
                print("Servicio no encontrado.")
            input("\nPresiona Enter para continuar...")
        
        elif choice == '4':
            service = input("¿Qué servicio quieres eliminar?: ")
            if manager.delete_password(service):
                print(f"Contraseña de {service} eliminada.")
            else:
                print("Servicio no encontrado.")
            input("\nPresiona Enter para continuar...")
            
        elif choice == '5':
            print("\n--- Cambio de Contraseña Maestra ---")
            new_pw1 = getpass.getpass("Ingresa la nueva contraseña maestra: ")
            new_pw2 = getpass.getpass("Confirma la nueva contraseña: ")
            
            if new_pw1 == new_pw2:
                try:
                    manager.change_master_password(new_pw1)
                    print("Contraseña maestra cambiada con éxito.")
                except Exception as e:
                    print(f"Error al cambiar la contraseña maestra: {e}")
            else:
                print("Las contraseñas no coinciden. Inténtalo de nuevo.")
            input("\nPresiona Enter para continuar...")
        
        elif choice == '6':
            print("Saliendo del gestor...")
            break
        
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            input("\nPresiona Enter para continuar...")

if __name__ == '__main__':
    main()