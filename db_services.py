import sqlite3
from datetime import datetime


def db_connect():

    cx = sqlite3.connect("CIH_folders.db")
    cx.execute("PRAGMA journal_mode=WAL;")
    cx.execute("PRAGMA foreign_keys=ON;")

    print("Conexión a la base de datos establecida")

    return cx

from datetime import datetime

def insert_folder_in_db(db, target_folders, parse_path_info):
    now = datetime.utcnow().isoformat()

    for folder in target_folders:
        path = folder.get("path")
        dept = muni = inst = sess = None  # valores por defecto

        if path:
            try:
                parsed = parse_path_info(path)
                if isinstance(parsed, (list, tuple)) and len(parsed) == 4:
                    dept, muni, inst, sess = parsed
                else:
                    print(f"[WARN] parse_path_info no devolvió 4 valores para path='{path}'. Se guardan NULLs.")
            except Exception as e:
                print(f"[WARN] Error parseando path='{path}' ({folder.get('id')} - {folder.get('name')}): {e}. Se guardan NULLs.")
        else:
            print(f"[WARN] Carpeta sin path: {folder.get('name')} (id={folder.get('id')}). Se guardan NULLs.")

        row = {
            "id": folder["id"],
            "name": folder["name"],
            "parent_id": None,
            "path": path,  # puede ser None si tu columna lo permite
            "code_name": None,
            "last_seen": now,
            "last_checked": now,
            "department": dept,
            "municipality": muni,
            "educational_institution": inst,
            "session": sess,
        }

        db.execute("""
            INSERT INTO folders(
                id, name, parent_id, path, code_name, last_seen, last_checked,
                department, municipality, educational_institution, session
            )
            VALUES(
                :id, :name, :parent_id, :path, :code_name, :last_seen, :last_checked,
                :department, :municipality, :educational_institution, :session
            )
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                path=excluded.path,
                code_name=excluded.code_name,
                last_seen=excluded.last_seen,
                last_checked=excluded.last_checked,
                department=excluded.department,
                municipality=excluded.municipality,
                educational_institution=excluded.educational_institution,
                session=excluded.session
        """, row)

    # Mejor rendimiento: un solo commit al final
    db.commit()
    print(f"Insertadas/actualizadas {len(target_folders)} carpetas en la base de datos.")

def add_column_to_db(db, table_name, column_name, column_type="TEXT", default_value=None):
        
        """
        Agrega una nueva columna a una tabla existente en la base de datos SQLite.

        Parámetros:
        db: conexión activa a la base de datos.
        table_name (str): nombre de la tabla a modificar.
        column_name (str): nombre de la nueva columna.
        column_type (str): tipo de dato (por defecto TEXT).
        default_value: valor por defecto opcional (None = sin valor por defecto).
        """

        cursor = db.cursor()

    # Verificar si la columna ya existe
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [col[1] for col in cursor.fetchall()]
        if column_name in existing_columns:
            print(f"[INFO] La columna '{column_name}' ya existe en la tabla '{table_name}'.")
            return

    # Construir sentencia ALTER TABLE
        alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        if default_value is not None:
        # Si el valor por defecto es texto, ponerlo entre comillas
            if isinstance(default_value, str):
                alter_query += f" DEFAULT '{default_value}'"
            else:
                alter_query += f" DEFAULT {default_value}"

        try:
            cursor.execute(alter_query)
            db.commit()
            print(f"[OK] Columna '{column_name}' agregada a la tabla '{table_name}'.")
        except sqlite3.OperationalError as e:
         print(f"[ERROR] No se pudo agregar la columna '{column_name}' a '{table_name}': {e}")

def get_folders_by_param(db, column_name, value):
    """
    Obtiene las carpetas de la tabla 'folders' que coincidan con un valor en una columna específica.

    Parámetros:
        db: conexión activa a la base de datos SQLite.
        column_name (str): nombre de la columna por la cual filtrar (por ejemplo: 'department', 'municipality', 'session').
        value: valor exacto que debe tener la columna (por ejemplo: 'Sucre', 'Sesión 1', etc.)

    Retorna:
        Una lista de diccionarios con la información de las carpetas encontradas.
    """

    cursor = db.cursor()

    # Verificar que el nombre de columna no sea malicioso o inexistente
    cursor.execute("PRAGMA table_info(folders)")
    valid_columns = [col[1] for col in cursor.fetchall()]
    if column_name not in valid_columns:
        print(f"[ERROR] La columna '{column_name}' no existe en la tabla 'folders'.")
        return []

    # Consulta parametrizada (segura)
    query = f"""
        SELECT 
            id, name, department, municipality, educational_institution,
            session, path, assigned, last_seen, last_checked
        FROM folders
        WHERE {column_name} = ?;
    """

    cursor.execute(query, (value,))
    rows = cursor.fetchall()

    # Extraer nombres de columnas
    col_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(col_names, row)) for row in rows]

    print(f"[INFO] Se encontraron {len(result)} carpetas donde {column_name} = '{value}'.")
    return result

def get_folder_ids_by_param(db, column_name, value):
    """
    Obtiene únicamente los IDs de las carpetas que cumplen una condición en la tabla 'folders'.

    Parámetros:
        db: conexión activa a la base de datos SQLite.
        column_name (str): nombre de la columna por la cual filtrar (por ejemplo: 'department', 'session', etc.).
        value: valor exacto que debe tener la columna.

    Retorna:
        Una lista con los IDs (str) de las carpetas encontradas.
    """

    cursor = db.cursor()

    # Verificar que la columna exista
    cursor.execute("PRAGMA table_info(folders)")
    valid_columns = [col[1] for col in cursor.fetchall()]
    if column_name not in valid_columns:
        print(f"[ERROR] La columna '{column_name}' no existe en la tabla 'folders'.")
        return []

    # Consulta ligera: solo trae la columna 'id'
    query = f"SELECT id FROM folders WHERE {column_name} = ?;"
    cursor.execute(query, (value,))
    rows = cursor.fetchall()

    # Convertir los resultados a una lista simple
    ids = [row[0] for row in rows]

    print(f"[INFO] Se encontraron {len(ids)} carpetas donde {column_name} = '{value}'.")
    return ids

def set_folders_assigned(db, column_name, value):
    """
    Marca como asignadas (assigned = 1) todas las carpetas que cumplan una condición específica.

    Parámetros:
        db: conexión activa a la base de datos SQLite.
        column_name (str): nombre de la columna por la cual filtrar (por ejemplo: 'department', 'municipality', 'session').
        value: valor que debe tener la columna para actualizar (por ejemplo: 'Sucre', 'Sesión 3', etc.)

    Retorna:
        Número de carpetas actualizadas.
    """

    cursor = db.cursor()

    # Verificar que la columna exista
    cursor.execute("PRAGMA table_info(folders)")
    valid_columns = [col[1] for col in cursor.fetchall()]
    if column_name not in valid_columns:
        print(f"[ERROR] La columna '{column_name}' no existe en la tabla 'folders'.")
        return 0

    # Actualizar carpetas que cumplan la condición
    query = f"UPDATE folders SET assigned = 1 WHERE {column_name} = ?;"
    cursor.execute(query, (value,))
    db.commit()

    updated = cursor.rowcount
    print(f"[OK] Se marcaron {updated} carpetas como asignadas donde {column_name} = '{value}'.")
    return updated



    