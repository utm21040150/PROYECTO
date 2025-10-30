from fastapi import FastAPI, HTTPException, BackgroundTasks
from numpy.f2py.crackfortran import debug
from pydantic import BaseModel
from joblib import load
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

app = FastAPI(
    title="Bank Marketing API",
    description="API for bank marketing predictions",
    version="1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de datos
class Cliente(BaseModel):
    age: int
    balance: float
    campaign: int
    contact: str
    day: int
    default: str
    duration: int
    education: str
    housing: str
    job: str
    loan: str
    marital: str
    month: str
    pdays: int
    poutcome: str
    previous: int


# Cargar modelo
try:
    model = load('modelo_svm.pkl')
    scaler = load('scaler.pkl')
    label_encoders = load('label_encoders.pkl')
    column_info = load('column_info.pkl')
    print(" Model loaded successfully")
except Exception as e:
    print(f" Error loading model: {e}")
    model = scaler = label_encoders = column_info = None

# Variables globales
is_training = False


# Funciones
def preprocesar_datos(data_dict):
    df = pd.DataFrame([data_dict])

    if column_info and 'feature_columns' in column_info:
        df = df[column_info['feature_columns']]

    if label_encoders:
        for col, encoder in label_encoders.items():
            if col in df.columns:
                df[col] = df[col].apply(lambda x: x if x in encoder.classes_ else 'unknown')
                try:
                    df[col] = encoder.transform(df[col])
                except:
                    df[col] = 0
    return df


def calcular_metricas_completas():
    try:
        # Simular métricas
        y_true = np.random.randint(0, 2, 100)
        y_pred = np.random.randint(0, 2, 100)

        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        metrics = {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(precision_score(y_true, y_pred, average='weighted'), 4),
            "recall": round(recall_score(y_true, y_pred, average='weighted'), 4),
            "f1_score": round(f1_score(y_true, y_pred, average='weighted'), 4),
            "timestamp": datetime.now().isoformat()
        }
        return metrics
    except Exception as e:
        return {"error": str(e)}


def guardar_en_bd(metrics):
    try:
        metrics_file = "model_metrics.json"
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                all_metrics = json.load(f)
        else:
            all_metrics = []

        all_metrics.append(metrics)
        with open(metrics_file, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        return True
    except:
        return False


def reentrenar_modelo_background():
    global is_training
    try:
        is_training = True
        import time
        time.sleep(10)  # Simular entrenamiento
        return True
    except:
        return False
    finally:
        is_training = False


# Endpoints
@app.post("/predict")
async def predict(data: Cliente):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        df = preprocesar_datos(data.dict())
        df_scaled = scaler.transform(df)
        prediction = model.predict(df_scaled)
        prediction_proba = model.predict_proba(df_scaled)

        return {
            "prediccion": int(prediction[0]),
            "probabilidad_no": round(float(prediction_proba[0][0]), 4),
            "probabilidad_si": round(float(prediction_proba[0][1]), 4),
            "confianza": round(float(max(prediction_proba[0])), 4),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/metrics")
async def metrics():
    try:
        metrics_data = calcular_metricas_completas()
        save_result = guardar_en_bd(metrics_data)
        return {
            "metricas": metrics_data,
            "guardado_en_bd": save_result,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/retrain")
async def retrain(background_tasks: BackgroundTasks):
    global is_training
    if is_training:
        raise HTTPException(status_code=429, detail="Training in progress")

    background_tasks.add_task(reentrenar_modelo_background)
    return {"message": "Retraining started", "status": "started"}


@app.get("/")
async def root():
    return {"message": "Bank Marketing API", "status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import os
    #port = int(os.environ.get("PORT", 5000))app.run(host='0.0.0.', port=port, debug=False)