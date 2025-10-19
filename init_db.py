# init_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("CIH_folders.db")

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS folders (
  id           TEXT PRIMARY KEY,      -- ID de Drive
  name         TEXT NOT NULL,
  parent_id    TEXT,                  -- padre directo (ID Drive)
  path         TEXT,                  -- ruta legible cacheada
  code_name    TEXT,                  -- nombre corto o código generado
  last_seen    TEXT,                  -- última vez que se actualizó desde Drive
  last_checked TEXT,                   -- última vez que se revisó manual o programadamente
  department   TEXT,                  -- departamento donde pertenece el establecimiento educativa a la que pertenece la carpeta
  municipality TEXT,                  -- municipio donde pertenece el establecimiento educativa a la que pertenece la carpeta
  educational_institution TEXT,       -- nombre del establecimiento educativo al que pertenece la carpeta
  session       TEXT                  -- sesión a la que pertenece la carpeta
);

CREATE INDEX IF NOT EXISTS idx_folders_parent_name ON folders(parent_id, name);

CREATE TABLE IF NOT EXISTS folder_sets (
  set_name  TEXT NOT NULL,
  folder_id TEXT NOT NULL,
  UNIQUE(set_name, folder_id),
  FOREIGN KEY(folder_id) REFERENCES folders(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sets_name ON folder_sets(set_name);
"""


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(DB_PATH)
    try:
        cx.executescript(SCHEMA)
        cx.commit()
        print(f"Base creada: {DB_PATH}")
    finally:
        cx.close()

if __name__ == "__main__":
    main()
