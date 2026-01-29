from flask import Flask, request, render_template
from moodle import get_assignid, get_submissions
import os
from downloader import descargar_archivos_submissions
from transcriber import transcribir_pdf
from dotenv import load_dotenv
from ia.feedback import generar_retroalimentacion
from db import (
    crear_tabla_si_no_existe,
    guardar_retroalimentacion,
    obtener_retroalimentacion_existente
)

crear_tabla_si_no_existe()

app = Flask(__name__)
load_dotenv()

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "✅ Servicio Moodle IA activo"

# =========================
# SOLO MUESTRA LOADER
# =========================

@app.route("/procesar_producto")
def procesar_producto():
    user_id = request.args.get("user_id")
    course_id = request.args.get("course_id")
    cmid = request.args.get("cmid")
    nombre_estudiante = request.args.get("nombre")

    return render_template(
        "resultado.html",
        user_id=user_id,
        course_id=course_id,
        cmid=cmid,
        nombre_estudiante=nombre_estudiante
    )

# =========================
# PROCESO PESADO
# =========================

@app.route("/generar")
def generar():

    user_id = request.args.get("user_id", type=int)
    course_id = request.args.get("course_id", type=int)
    cmid = request.args.get("cmid", type=int)

    if not all([user_id, course_id, cmid]):
        return "Faltan parámetros", 400

    assignid = get_assignid(course_id, cmid)
    if not assignid:
        return "No se encontró assignid", 404

    data = get_submissions(assignid)
    submissions = data["assignments"][0].get("submissions", [])

    pdfs = descargar_archivos_submissions(
        submissions=submissions,
        course_id=course_id,
        assign_id=assignid,
        user_filter=user_id
    )

    if not pdfs:
        return "El usuario no tiene archivos"

    # 🔍 Verificar BD
    existente = obtener_retroalimentacion_existente(
        user_id, course_id, cmid, assignid
    )

    if existente:
        # 🧹 Borrar PDFs descargados
        for pdf in pdfs:
            if os.path.exists(pdf):
                os.remove(pdf)

        return existente

    textos = []

    for pdf in pdfs:
        texto = transcribir_pdf(pdf)
        textos.append(texto)

        # 🧹 Borrar PDF luego de usarlo
        if os.path.exists(pdf):
            os.remove(pdf)

    transcripcion_final = "\n\n".join(textos)

    resultado = generar_retroalimentacion(
        transcripcion=transcripcion_final,
        course_id=course_id,
        cmid=cmid
    )

    guardar_retroalimentacion({
        "user_id": user_id,
        "course_id": course_id,
        "cmid": cmid,
        "assignid": assignid,
        "archivo": ",".join(pdfs),
        "transcripcion": transcripcion_final,
        "retroalimentacion": resultado["texto"],
        "modelo": resultado["modelo"],
        "prompt_tokens": resultado["prompt_tokens"],
        "completion_tokens": resultado["completion_tokens"],
        "total_tokens": resultado["total_tokens"],
        "costo_prompt_usd": resultado["costo_prompt_usd"],
        "costo_completion_usd": resultado["costo_completion_usd"],
        "costo_total_usd": resultado["costo_total_usd"]
    })

    return resultado["texto"]


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7001)