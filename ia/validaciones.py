# app/ia/validaciones.py
import hashlib
from db import obtener_transcripcion_entrega
import hashlib
# =========================
# RELACIÓN DE ENTREGAS
# =========================

SECUENCIA_ENTREGAS = {
    2440: {  # Inicial 
        194529: 194464,# segunda depende de la primera, 194529 se compara con 194464
        194532: 194473 #“Si estoy en este cmid, ¿con cuál anterior me comparo?”
    }#,

    #2443: {  # Primaria
    #    195100: 195080,  # segunda planificación
    #    195150: 195100
    #},
#
    #2446: {  # Secundaria
    #    196200: 196180
    #}
}

# =========================
# REGLAS PEDAGÓGICAS POR CURSO
# =========================

NIVELES_POR_CURSO = {
    2440: {  # EDUCACIÓN INICIAL
        "nivel": "Inicial",
        "edad": "0-5",

        "palabras_clave_validas": [
            "niños", "niñas", "juego", "exploración",
            "psicomotricidad", "lenguaje oral",
            "rutinas", "aprendizaje a través del juego","infancia",
            "primera infancia", "bienestar infantil", "aprendizaje lúdico", "expresión de emociones"
        ],
 

        "indicadores_prohibidos": [
            "matemática","primaria",
            "secundaria", "bachillerato",
            "3°", "4°", "5°",
            "educación superior","primer grado","segundo grado","tercer grado",
            "cuarto grado","quinto grado","sexto grado","1°","2°","asignatura","clase magistral"
        ],

        # 🔥 CLAVE: tipo de producto por cmid
        "tipo_producto": {
            194464: {  # U1 S1
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194529: {  # U1 S1 opcional
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194473: {  # U2 S1
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194532: {  # U2 S1 opcional
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194521: {  # U2 S2 unidad didáctica
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "unidad didáctica"              
                ]
            },

            194522: {  # U2 S2 Sesión de aprendizaje
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "sesión de aprendizaje"              
                ]
            }
        }
    },

    2443: {  # EDUCACIÓN PRIMARIA
        "nivel": "Primaria",
        "edad": "6-11",

        "palabras_clave_validas": [
            "Primaria","3° grado","4° grado","5° grado","6° grado","educación básica regular", "primeros ciclos", 
            "aprendizajes fundamentales", "desarrollo integral", "formación básica", 
            "iniciación académica", "acompañamiento docente", "aprendizaje guiado", 
            "atención a la diversidad"
        ],
 

        "indicadores_prohibidos": [
            "inicial","secundaria"
        ],

        # 🔥 CLAVE: tipo de producto por cmid
        "tipo_producto": {
            194770: {  # U1 S1
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194772: {  # U1 S1 opcional
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194788: {  # U2 S1
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194790: {  # U2 S1 opcional
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194799: {  # U2 S2 unidad didáctica
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "unidad didáctica"              
                ]
            },

            194801: {  # U2 S2 Sesión de aprendizaje
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "sesión de aprendizaje"              
                ]
            }
        }
    },

    2446: {  # EDUCACIÓN SECUNDARIA
        "nivel": "Secundaria",
        "edad": "11-16",

        "palabras_clave_validas": [
            "Secundaria", "Ciclo VII", "educación física", "vida saludable", "3° de secundaria",
            "tercer grado de secundaria","4° grado de secundaria","cuarto grado de secundaria",
            "5° grado de secundaria","quinto grado de secundaria",
            "autonomía del estudiante", "sedentarismo", "inclusión", "diversidad de habilidades",
            "uso de TIC", "bienestar socioemocional"
        ],
 

        "indicadores_prohibidos": [
            "inicial","primaria"            
        ],

        # 🔥 CLAVE: tipo de producto por cmid
        "tipo_producto": {
            194822: {  # U1 S1
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194824: {  # U1 S1 opcional
                "nombre": "diagnóstico al inicio del año escolar",
                "palabras_clave": [
                    "diagnóstico al inicio del año escolar"
                ]
            },

            194840: {  # U2 S1
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194842: {  # U2 S1 opcional
                "nombre": "planificación anual",
                "palabras_clave": [
                    "planificación anual"
                ]
            },

            194851: {  # U2 S2 unidad didáctica
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "unidad didáctica"              
                ]
            },

            194853: {  # U2 S2 Sesión de aprendizaje
                "nombre": "unidad didáctica",
                "palabras_clave": [
                    "sesión de aprendizaje"              
                ]
            }
        }
    }
}



# =========================
# VALIDA DUPLICIDAD
# =========================
def _hash_texto(texto):
    texto_limpio = " ".join(texto.lower().split())
    return hashlib.md5(texto_limpio.encode("utf-8")).hexdigest()

def validar_mejora_producto(
    texto_actual,
    user_id,
    course_id,
    cmid
):
    curso = SECUENCIA_ENTREGAS.get(course_id)
    if not curso:
        return {"es_valido": True}

    cmid_anterior = curso.get(cmid)
    if not cmid_anterior:
        return {"es_valido": True}

    # 🔎 Obtener transcripción anterior desde BD
    transcripcion_anterior = obtener_transcripcion_entrega(
        user_id=user_id,
        course_id=course_id,
        cmid=cmid_anterior
    )

    if not transcripcion_anterior:
        return {"es_valido": True}

    hash_anterior = _hash_texto(transcripcion_anterior)
    hash_actual = _hash_texto(texto_actual)

    if hash_anterior == hash_actual:
        return {
            "es_valido": False,
            "mensaje": (
                "Has vuelto a subir el mismo producto que en la entrega anterior, "
                "sin evidenciar mejoras o ajustes. Para poder brindarte una "
                "retroalimentación formativa, te invitamos a revisar las "
                "observaciones previas, mejorar tu trabajo y volver a subirlo."
            )
        }

    return {"es_valido": True}
# =========================
# FUNCIONES DE VALIDACIÓN
# =========================

def validar_pertinencia_pedagogica(texto, course_id, cmid):
    reglas = NIVELES_POR_CURSO.get(course_id)

    if not reglas:
        return {
            "es_valido": False,
            "mensaje": "No se pudo determinar el nivel educativo del curso."
        }

    texto_lower = texto.lower()
    print(texto_lower)
    # 1️⃣ Indicadores prohibidos (nivel incorrecto)
    for palabra in reglas["indicadores_prohibidos"]:
        print(palabra)
        if palabra in texto_lower:            
            return _mensaje_reconduccion_nivel(reglas["nivel"])

    # 2️⃣ Lenguaje propio del nivel
    coincidencias = sum(
        1 for p in reglas["palabras_clave_validas"]
        if p in texto_lower
    )

    if coincidencias < 2:
        return _mensaje_reconduccion_nivel(reglas["nivel"])

    # 3️⃣ Validar tipo de producto según CMID
    productos = reglas.get("tipo_producto", {})
    producto = productos.get(cmid)

    if not producto:
        return {
            "es_valido": False,
            "mensaje": (
                "He notado que aún no se ha cargado el producto solicitado para esta actividad. Esta tarea forma parte del proceso formativo y está diseñada para acompañarte en la reflexión y planificación de tu práctica pedagógica. Para poder continuar y ofrecerte una orientación formativa pertinente, es necesario que subas el producto solicitado, según la consigna. Te invito a revisar nuevamente la actividad y cargar tu trabajo cuando lo tengas listo. Estoy aquí para acompañarte en ese proceso. "
            )
        }

    if not _detectar_producto_por_cmid(
        texto_lower,
        producto["palabras_clave"]
    ):
        return _mensaje_reconduccion_producto(
            reglas["nivel"],
            producto["nombre"]
        )

    return {"es_valido": True}

def _detectar_producto_por_cmid(texto, palabras_clave):
    for palabra in palabras_clave:
        if palabra in texto:
            return True
    return False
# =========================
# FUNCIONES AUXILIARES
# =========================

def _mensaje_reconduccion_producto(nivel, producto):
    return {
        "es_valido": False,
        "mensaje": (
            f"El producto presentado no corresponde al tipo de producto "
            f"({producto}) solicitado para el nivel de educación {nivel}. "
            "Revisa la consigna de la actividad y ajusta tu archivo para "
            "poder recibir una retroalimentación formativa."
        )
    }


def _mensaje_reconduccion_nivel(nivel):
    return {
        "es_valido": False,
        "mensaje": (
            f"El producto presentado no corresponde al nivel de educación {nivel} "
            "solicitado en esta actividad. Para poder brindarte una retroalimentación "
            "formativa, es importante que el archivo responda al nivel indicado en la consigna."
        )
    }