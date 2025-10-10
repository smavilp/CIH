from sheets_services import find_sheet_by_name, copy_sheet
from create_nested_lists import create_nested_lists
from folders_services import find_folder_by_name, create_folder

# Crear la arquitectura de carpetas en el drive basada en la hoja de Google Sheets

def create_folder_architecture(drive_service, sheet_service):

    EE_sheet_id = find_sheet_by_name(drive_service, "Establecimientos Educativos")

    nested_lists = create_nested_lists(sheet_service, EE_sheet_id, "A:Z")

    root_folder_id = find_folder_by_name(drive_service, "Centros de Interés")

    attendance_students_template = find_sheet_by_name(drive_service, "Formato Listado de Asistencia Estudiantes")

    student_report_template = find_sheet_by_name(drive_service, "Formato Reporte de Estudiantes")

    for dep_node in nested_lists:
        dep_name = dep_node["departamento"].strip()
        if not dep_name:
            continue
        dep_id = create_folder(drive_service, dep_name, root_folder_id)

        for mun_node in dep_node.get("municipios", []):
            mun_name = mun_node["municipio"].strip()
            if not mun_name:
                continue
            mun_id = create_folder(drive_service, mun_name, dep_id)

            for est_name in mun_node.get("establecimientos", []):
                est_name = str(est_name).strip()
                if not est_name:
                    continue
                est_id = create_folder(drive_service, est_name, mun_id)

                for subfolder in ["Acuerdo de Cobertura", "Consentimientos Informados","Ficha Centro de Interés","Seguimiento a Estudiantes", "Sesiones Pedagógicas"]:
                    subfolder_id = create_folder(drive_service, subfolder, est_id)

                    if subfolder == "Seguimiento a Estudiantes":
                        # Copiar la plantilla de "Formato Reporte de Estudiantes" aquí
                        copy_sheet(
                            drive_service,
                            student_report_template,
                            "Formato Reporte de Estudiantes",
                            subfolder_id)
                        
                        print(f" Copiada plantilla de reporte en: {est_name}/{subfolder}")

                        # Copiar la plantilla de "Formato Listado de Asistencia Estudiantes"
                        copy_sheet(
                            drive_service,
                            attendance_students_template,
                            "Formato Listado de Asistencia Estudiantes",
                            subfolder_id)
                        
                        print(f" Copiada plantilla de asistencia en: {est_name}/{subfolder}")

                    if subfolder == "Sesiones Pedagógicas":
                        for sesion in range(1, 8):  # 1 a 7 inclusive
                            sesion_name = f"Sesión {sesion}"
                            sesion_id = create_folder(drive_service, sesion_name, subfolder_id)
                            print(f" Creada carpeta: {sesion_name}")

                            #  Dentro de cada Sesión, crear 3 subcarpetas
                            for sub_subfolder in [
                            "Listado Asistencia",
                            "Evidencias Fotográficas",
                            "Registro Didáctico",]:
                                create_folder(drive_service, sub_subfolder, sesion_id)
                                print(f"Creada subcarpeta: {sesion_name}/{sub_subfolder}")

    print("Estructura creada correctamente.")
    

   

    
