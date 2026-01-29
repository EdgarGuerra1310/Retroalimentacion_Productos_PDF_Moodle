import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "transcripciones.json")

def guardar(registro):
    # 1. Inicializar data
    data = []

    # 2. Si existe Y tiene contenido válido
    if os.path.exists(FILE) and os.path.getsize(FILE) > 0:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    # 3. Agregar registro
    data.append(registro)

    # 4. Guardar
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)