def update_file_name(drive_service, file_id: str, new_name: str):

    print(f"Actualizando nombre del archivo ID: {file_id} a '{new_name}'")
    updated_file = {
        "name": new_name,
    }
    updated = drive_service.files().update(
        fileId=file_id,
        body=updated_file,
        supportsAllDrives=True,
    ).execute()
    return updated.get("id")


   