from flask import Flask, request, render_template
from moodle import get_assignid, get_submissions
import os
from downloader import descargar_archivos_submissions
from transcriber import transcribir_pdf
from dotenv import load_dotenv
from ia.feedback import generar_retroalimentacion
from ia.validaciones import validar_pertinencia_pedagogica
from ia.validaciones import (
    validar_pertinencia_pedagogica,
    validar_mejora_producto
)

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
        return "He notado que aún no se ha cargado el producto solicitado para esta actividad. Esta tarea forma parte del proceso formativo y está diseñada para acompañarte en la reflexión y planificación de tu práctica pedagógica. Para poder continuar y ofrecerte una orientación formativa pertinente, es necesario que subas el producto solicitado, según la consigna. Te invito a revisar nuevamente la actividad y cargar tu trabajo cuando lo tengas listo. Estoy aquí para acompañarte en ese proceso."

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

    # 1️⃣ Validación pedagógica (nivel + tipo)
    validacion = validar_pertinencia_pedagogica(
        texto=transcripcion_final,
        course_id=course_id,
        cmid=cmid
    )

    if not validacion["es_valido"]:
        return validacion["mensaje"]

    # 2️⃣ Validación de mejora (solo segundas entregas)
    mejora = validar_mejora_producto(
        texto_actual=transcripcion_final,
        user_id=user_id,
        course_id=course_id,
        cmid=cmid
    )
    if not mejora["es_valido"]:
        return mejora["mensaje"]

    # 3️⃣ RECIÉN retroalimentar

    # ✅ SOLO SI PASA, RETROALIMENTA

    resultado = generar_retroalimentacion(
        transcripcion=transcripcion_final,
        course_id=course_id,
        cmid=cmid,
        user_id=user_id
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