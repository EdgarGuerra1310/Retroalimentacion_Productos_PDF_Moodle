import os
from openai import OpenAI

from dotenv import load_dotenv

# ======================
# CONFIGURACIÓN BASE
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)

PROMPT_PATH = os.path.join(APP_DIR, "prompts", "PROMPT_IA.txt")
RUBRICAS_DIR = os.path.join(APP_DIR, "rubricas")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ======================
# UTILIDADES
# ======================
def leer_archivo(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def cargar_rubrica(course_id, cmid):
    rubrica_path = os.path.join(
        RUBRICAS_DIR,
        f"course_{course_id}",
        f"cmid_{cmid}.txt"
    )

    if not os.path.exists(rubrica_path):
        raise FileNotFoundError(f"No existe rúbrica para course={course_id}, cmid={cmid}")

    return leer_archivo(rubrica_path)

# ======================
# FUNCIÓN PRINCIPAL
# ======================
def generar_retroalimentacion(transcripcion, course_id, cmid):
    prompt_maestro = leer_archivo(PROMPT_PATH)
    rubrica = cargar_rubrica(course_id, cmid)

    prompt_final = f"""
{prompt_maestro}

--- RÚBRICA ---
{rubrica}

--- TRANSCRIPCIÓN DEL ESTUDIANTE ---
{transcripcion}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un evaluador pedagógico experto."},
            {"role": "user", "content": prompt_final}
        ],
        temperature=0.3
    )

    usage = response.usage

    # Tarifas referenciales (ajustables)
    COSTO_PROMPT = 0.00015 / 1000
    COSTO_COMPLETION = 0.00060 / 1000

    prompt_cost = usage.prompt_tokens * COSTO_PROMPT
    completion_cost = usage.completion_tokens * COSTO_COMPLETION

    return {
        "texto": response.choices[0].message.content,
        "modelo": "gpt-4o-mini",
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "costo_prompt_usd": round(prompt_cost, 6),
        "costo_completion_usd": round(completion_cost, 6),
        "costo_total_usd": round(prompt_cost + completion_cost, 6)
    }