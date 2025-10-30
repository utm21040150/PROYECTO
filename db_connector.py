import psycopg2
import json
import time
import numpy as np

#  Configuración de conexion
DB_CONFIG = {
    "dbname": "ResultadosDB",
    "user": "postgres",
    "password": "root1234",
    "host": "localhost",
    "port": "5432"
}

METRICS_FILE = "model_metrics.json"


def connect_db():
    """Conecta a la base de datos PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def insert_metric(cursor, metric):
    """Inserta una métrica en la tabla 'metrics'"""
    # Convirtiendo a float normal
    for key, val in metric.items():
        if isinstance(val, np.generic):
            metric[key] = float(val)

    # Matriz de confusión
    tn, fp, fn, tp = (None, None, None, None)
    if "confusion_matrix" in metric and metric["confusion_matrix"]:
        try:
            matrix = metric["confusion_matrix"]
            tn, fp = matrix[0]
            fn, tp = matrix[1]
        except Exception:
            pass

    query = """
        INSERT INTO metrics
        (accuracy, precision, recall, f1_score, auc_roc, ap_pr_curve, tn, fp, fn, tp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        metric.get("accuracy"),
        metric.get("precision"),
        metric.get("recall"),
        metric.get("f1_score"),
        metric.get("auc_roc"),
        metric.get("ap_pr_curve"),
        tn, fp, fn, tp
    )
    cursor.execute(query, values)


def sync_metrics():
    """Lee el archivo JSON y sincroniza con la BD"""
    conn = connect_db()
    cursor = conn.cursor()
    print("Conectado a PostgreSQL")

    last_len = 0

    while True:
        try:
            
            with open(METRICS_FILE, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)

            if len(data) > last_len:
                new_metrics = data[last_len:]
                print(f" Insertando {len(new_metrics)} nuevas métricas...")

                for metric in new_metrics:
                    insert_metric(cursor, metric)

                last_len = len(data)

        except FileNotFoundError:
            print("No se encontro model_metrics.json.")
        except Exception as e:
            print(f" Error: {e}")

        time.sleep(30)  


if __name__ == "__main__":
    sync_metrics()
