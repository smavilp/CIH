def create_nested_lists(sheets_service, sheet_id, cell_range="A:Z"):
    # Obtener los datos de la hoja
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=cell_range
    ).execute()

    # Extraer las filas
    values = res.get("values", [])
    if not values:
        print("La hoja está vacía.")
        return []

    headers = values[1] # Encabezados (nombres de columnas)
    rows = values[2:] # Datos 

    print(f"Estos son los encabezados: {headers}")              

    # Índices de columna por nombres de columna
    idx_dep = headers.index("DEPARTAMENTO")
    idx_mun = headers.index("MUNICIPIO")
    idx_est = headers.index("NOMBRE_ESTABLECIMIENTO")

    # Mapa anidado: dep -> mun -> est
    tree_map = {}

    for r in rows:
        # Saltar filas incompletas
        if len(r) <= max(idx_dep, idx_mun, idx_est):
            continue
        dep = r[idx_dep].strip()
        mun = r[idx_mun].strip()
        est = r[idx_est].strip()
        if not (dep and mun and est):
            continue

        # Construir anidación en un map
        tree_map.setdefault(dep, {})
        tree_map[dep].setdefault(mun, set())
        tree_map[dep][mun].add(est)

    # Convertir a lista anidada
    nested = []
    for dep, mun_dict in sorted(tree_map.items()):
        dep_node = {"departamento": dep, "municipios": []}
        for mun, est_set in sorted(mun_dict.items()):
            dep_node["municipios"].append({
                "municipio": mun,
                "establecimientos": sorted(est_set)
            })
        nested.append(dep_node)

    print("✅ Árbol anidado construido en una sola pasada.")
    return nested
