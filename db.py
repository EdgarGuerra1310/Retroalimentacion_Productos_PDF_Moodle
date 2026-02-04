import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


def crear_tabla_si_no_existe():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ia_retroalimentaciones_tareas (
        id SERIAL PRIMARY KEY,

        user_id INTEGER,
        course_id INTEGER,
        cmid INTEGER,
        assignid INTEGER,

        archivo TEXT,
        transcripcion TEXT,
        retroalimentacion TEXT,

        modelo VARCHAR(50),

        prompt_tokens INTEGER,
        completion_tokens INTEGER,
        total_tokens INTEGER,

        costo_prompt_usd NUMERIC(10,6),
        costo_completion_usd NUMERIC(10,6),
        costo_total_usd NUMERIC(10,6),

        fecha TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def guardar_retroalimentacion(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ia_retroalimentaciones_tareas (
        user_id, course_id, cmid, assignid,
        archivo, transcripcion, retroalimentacion,
        modelo,
        prompt_tokens, completion_tokens, total_tokens,
        costo_prompt_usd, costo_completion_usd, costo_total_usd
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["user_id"],
        data["course_id"],
        data["cmid"],
        data["assignid"],
        data["archivo"],
        data["transcripcion"],
        data["retroalimentacion"],
        data["modelo"],
        data["prompt_tokens"],
        data["completion_tokens"],
        data["total_tokens"],
        data["costo_prompt_usd"],
        data["costo_completion_usd"],
        data["costo_total_usd"]
    ))

    conn.commit()
    cur.close()
    conn.close()

def obtener_retroalimentacion_existente(user_id, course_id, cmid, assignid):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT retroalimentacion
        FROM ia_retroalimentaciones_tareas
        WHERE user_id = %s
          AND course_id = %s
          AND cmid = %s
          AND assignid = %s
        ORDER BY fecha DESC
        LIMIT 1
    """, (user_id, course_id, cmid, assignid))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return None

def obtener_transcripcion_entrega(
    user_id,
    course_id,
    cmid
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT transcripcion
        FROM ia_retroalimentaciones_tareas
        WHERE user_id = %s
          AND course_id = %s
          AND cmid = %s
        ORDER BY fecha DESC
        LIMIT 1
    """, (user_id, course_id, cmid))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return None