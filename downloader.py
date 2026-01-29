import os
import requests

TOKEN = "934a5bc65d092299e862902196a6f43b"

def descargar_archivos_submissions(
    submissions,
    course_id,
    assign_id,
    base_dir="app/data/pdfs",
    user_filter=None
):
    os.makedirs(base_dir, exist_ok=True)
    archivos_descargados = []

    for sub in submissions:
        userid = sub["userid"]

        if user_filter and userid != user_filter:
            continue

        for plugin in sub.get("plugins", []):
            for filearea in plugin.get("fileareas", []):
                for f in filearea.get("files", []):
                    filename = f["filename"]

                    filename_safe = f"{userid}_course{course_id}_assign{assign_id}_{filename}"
                    filepath = os.path.join(base_dir, filename_safe)

                    if os.path.exists(filepath):
                        remote_size = f.get("filesize", 0)
                        local_size = os.path.getsize(filepath)
                        if remote_size == local_size:
                            print(f"⏩ Ya descargado: {filename_safe}")
                            archivos_descargados.append(filepath)
                            continue
                        else:
                            print(f"♻️ Archivo actualizado, re-descargando: {filename_safe}")

                    fileurl = f"{f['fileurl']}?token={TOKEN}&forcedownload=1"
                    print(f"⬇️ Descargando {filename_safe}")

                    with requests.get(
                        fileurl,
                        stream=True,
                        verify=False,
                        timeout=60
                    ) as r:
                        r.raise_for_status()
                        with open(filepath, "wb") as out:
                            for chunk in r.iter_content(chunk_size=8192):
                                out.write(chunk)

                    print(f"✅ Guardado en {filepath}")
                    archivos_descargados.append(filepath)

    return archivos_descargados