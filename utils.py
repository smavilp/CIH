"""
def parse_path_info(path: str):
  
    Extrae departamento, municipio, institución y sesión a partir del path.
    Ejemplo:
    Mi unidad/Proyecto.../Sucre/Sincelejo/I. E. SAN ISIDRO DE CHOCHO/Acuerdo de Cobertura
    
    parts = [p.strip() for p in path.split("/") if p.strip()]

    dept, muni, inst, sess = None, None, None, None

    if len(parts) >= 4:
        dept = parts[4]
        muni = parts[5]
        inst = parts[6]
        sess = parts[-2] if "Sesión" in parts[-2] else None

    return dept, muni, inst, sess
"""

def parse_path_info(path: str):
    """
    Extrae departamento, municipio, institución y sesión a partir del path.
    Ejemplo:
    Mi unidad/Proyecto.../Sucre/Sincelejo/I. E. SAN ISIDRO DE CHOCHO/Acuerdo de Cobertura

    Devuelve (dept, muni, inst, sess)
    Si el path es None, no es string o no tiene suficientes partes, devuelve None en los campos faltantes.
    """
    # Validar que el path exista y sea texto
    if not path or not isinstance(path, str):
        print(f"[WARN] parse_path_info recibió un path inválido: {path}")
        return None, None, None, None

    # Dividir la ruta en partes limpias
    parts = [p.strip() for p in path.split("/") if p.strip()]

    # Inicializar variables
    dept = muni = inst = sess = None

    try:
        # Evitar IndexError con rutas cortas
        if len(parts) > 4:
            dept = parts[4] if len(parts) > 4 else None
            muni = parts[5] if len(parts) > 5 else None
            inst = parts[6] if len(parts) > 6 else None

            # Buscar la palabra “Sesión” en las partes finales
            if len(parts) > 7 and "Sesión" in parts[-2]:
                sess = parts[-2]

        else:
            print(f"[WARN] Ruta con pocas partes: {path}")

    except Exception as e:
        print(f"[WARN] Error al procesar path='{path}': {e}")

    return dept, muni, inst, sess
