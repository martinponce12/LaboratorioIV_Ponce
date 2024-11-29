import sqlite3
from datetime import datetime

# Conexión a la base de datos
conn = sqlite3.connect("escuela.db")
cursor = conn.cursor()

# Creación de tablas
def crear_tablas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            numero_documento TEXT UNIQUE NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            telefono TEXT,
            domicilio TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER,
            rol TEXT NOT NULL,
            FOREIGN KEY (persona_id) REFERENCES personas (id)
        )
    ''')
    conn.commit()

# Ingresar datos
def ingresar_datos():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    numero_documento = input("Número de Documento: ")
    fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ")
    telefono = input("Teléfono: ")
    domicilio = input("Domicilio: ")
    rol = input("Rol (Alumno/Profesor): ")

    try:
        cursor.execute('''
            INSERT INTO personas (nombre, apellido, numero_documento, fecha_nacimiento, telefono, domicilio)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, numero_documento, fecha_nacimiento, telefono, domicilio))
        persona_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO roles (persona_id, rol)
            VALUES (?, ?)
        ''', (persona_id, rol))
        conn.commit()
        print("Datos ingresados correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El número de documento ya existe.")

# Consultar datos
def consultar_datos():
    print("Consultar por:")
    print("1. Nombre")
    print("2. Apellido")
    print("3. Documento")
    opcion = input("Seleccione una opción (1/2/3): ")

    if opcion == "1":
        columna = "nombre"
    elif opcion == "2":
        columna = "apellido"
    elif opcion == "3":
        columna = "numero_documento"
    else:
        print("Opción inválida.")
        return

    valor = input(f"Ingrese el {columna}: ")
    query = f"SELECT p.*, r.rol FROM personas p JOIN roles r ON p.id = r.persona_id WHERE {columna} LIKE ?"
    
    try:
        cursor.execute(query, (f"%{valor}%",))
        resultados = cursor.fetchall()

        if resultados:
            for persona in resultados:
                print(persona)
        else:
            print("No se encontraron datos.")
    except sqlite3.Error as e:
        print(f"Error al consultar datos: {e}")


# Eliminar datos
def eliminar_datos():
    id_persona = input("Ingrese el ID de la persona a eliminar: ")
    cursor.execute("DELETE FROM personas WHERE id = ?", (id_persona,))
    cursor.execute("DELETE FROM roles WHERE persona_id = ?", (id_persona,))
    conn.commit()
    print("Datos eliminados correctamente.")

# Ordenar y listar datos
def listar_datos_ordenados():
    print("Opciones de ordenamiento: 1. Alfabético 2. Por ID 3. Por Edad")
    opcion = input("Elija una opción (1/2/3): ")
    if opcion == "1":
        cursor.execute("SELECT p.*, r.rol FROM personas p JOIN roles r ON p.id = r.persona_id ORDER BY p.apellido, p.nombre")
    elif opcion == "2":
        cursor.execute("SELECT p.*, r.rol FROM personas p JOIN roles r ON p.id = r.persona_id ORDER BY p.id")
    elif opcion == "3":
        cursor.execute("SELECT p.*, r.rol FROM personas p JOIN roles r ON p.id = r.persona_id ORDER BY p.fecha_nacimiento")
    else:
        print("Opción inválida.")
        return
    resultados = cursor.fetchall()
    for persona in resultados:
        print(persona)

# Menú principal
def menu():
    while True:
        print("\n--- Sistema de intraconsulta academico ---")
        print("1. Ingreso de datos")
        print("2. Consulta de datos")
        print("3. Eliminación de datos")
        print("4. Ordenamiento de datos por criterio")
        print("5. Salida")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ingresar_datos()
        elif opcion == "2":
            consultar_datos()
        elif opcion == "3":
            eliminar_datos()
        elif opcion == "4":
            listar_datos_ordenados()
        elif opcion == "5":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

# Configuración inicial
crear_tablas()
menu()

# Cerrar la conexión
conn.close()
