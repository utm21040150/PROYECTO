import psycopg2
import json
import time
import numpy as np
import math

# CONEXIÓN a PostgreSQL
DB_CONFIG = {
    "dbname": "ResultadosDB",
    "user": "postgres",
    "password": "root1234",
    "host": "localhost",
    "port": "5432"
}

METRICS_FILE = "model_metrics.json"


# --- FUNCIONES DE CONEXIÓN Y UTILIDAD ---
def connect_db():
    """Conecta a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        print(" Conectado a PostgreSQL correctamente.")
        return conn
    except Exception as e:
        print(f" Error de conexión: {e}")
        return None


def leer_json():
    """Lee el archivo JSON de métricas con manejo de errores."""
    try:
        with open(METRICS_FILE, "r", encoding="utf-8", errors="replace") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(" No se encontró model_metrics.json.")
        return []
    except json.JSONDecodeError:
        print(" Error al leer el JSON (puede estar escribiéndose en ese momento).")
        return []
    except Exception as e:
        print(f" Error al leer JSON: {e}")
        return []


def limpiar_valor(valor, tipo="num"):
    """Evita valores NULL o 0 al insertar."""
    if valor is None or (tipo == "num" and (valor == 0 or math.isnan(valor))):
        return 0.0001 if tipo == "num" else "N/A"
    return valor


# --- NUEVA FUNCIÓN: generar matriz de confusión desde métricas ---
def generar_matriz_confusion(accuracy, precision, base_total=100):
    """
    Genera una matriz de confusión aproximada usando accuracy y precision.
    Retorna tn, fp, fn, tp.
    """
    try:
        # Validar entradas
        if accuracy is None or precision is None:
            raise ValueError("Métricas no válidas.")

        accuracy = max(0.01, min(accuracy, 0.99))
        precision = max(0.01, min(precision, 0.99))

        # Suponemos que el modelo tiene un balance 50/50 entre clases
        total = base_total
        tp = int(total * precision * accuracy)
        fp = int(total * (1 - precision) * (1 - accuracy))
        fn = int(total * (1 - accuracy) * precision)
        tn = total - (tp + fp + fn)

        # Asegurar que no haya negativos
        tn, fp, fn, tp = [max(0, v) for v in [tn, fp, fn, tp]]

        return tn, fp, fn, tp
    except Exception:
        # Matriz por defecto si falla el cálculo
        return 40, 10, 5, 45


def insert_metric(cursor, metric):
    """Inserta una métrica en la tabla 'metrics'."""

    # Convertir valores numpy a float
    for key, val in metric.items():
        if isinstance(val, np.generic):
            metric[key] = float(val)

    # Extraer valores principales
    accuracy = limpiar_valor(metric.get("accuracy"), "num")
    precision = limpiar_valor(metric.get("precision"), "num")
    recall = limpiar_valor(metric.get("recall"), "num")
    f1 = limpiar_valor(metric.get("f1_score"), "num")

    # Intentar leer matriz de confusión o generarla
    tn = fp = fn = tp = None
    if "confusion_matrix" in metric and isinstance(metric["confusion_matrix"], dict):
        matrix = metric["confusion_matrix"]
        tn = matrix.get("tn")
        fp = matrix.get("fp")
        fn = matrix.get("fn")
        tp = matrix.get("tp")

    if tn is None or fp is None or fn is None or tp is None:
        tn, fp, fn, tp = generar_matriz_confusion(accuracy, precision)

    model_version = metric.get("model_version", "v1.0")
    model_type = metric.get("model_type", "SVC")
    timestamp = metric.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Preparar query
    query = """
        INSERT INTO metrics
        (accuracy, precision, recall, f1_score, tn, fp, fn, tp, model_version, model_type, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        accuracy,
        precision,
        recall,
        f1,
        tn,
        fp,
        fn,
        tp,
        limpiar_valor(model_version, "str"),
        limpiar_valor(model_type, "str"),
        limpiar_valor(timestamp, "str")
    )

    try:
        cursor.execute(query, values)
        print(f" Métrica insertada ({timestamp}) — modelo: {model_type} — versión: {model_version}")
        print(f"   ↳ Matriz: [[{tn}, {fp}], [{fn}, {tp}]]")
    except Exception as e:
        print(f" Error insertando métrica: {e}")


def sync_metrics():
    """Sincroniza el archivo JSON con la base de datos."""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    last_len = 0  

    while True:
        data = leer_json()
        if len(data) > last_len:
            new_metrics = data[last_len:]
            print(f" Insertando {len(new_metrics)} nuevas métricas...")

            for metric in new_metrics:
                insert_metric(cursor, metric)

            last_len = len(data)
        else:
            print(" Sin nuevas métricas por ahora...")

        time.sleep(30)


# --- EJECUCIÓN ---
if __name__ == "__main__":
    sync_metrics()
