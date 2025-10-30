from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import pickle
import os
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, RocCurveDisplay, PrecisionRecallDisplay,
    ConfusionMatrixDisplay
)
import pandas as pd

app = FastAPI(title="API SVM - Bank Marketing Dataset", version="1.0")

# ========================
# Rutas de archivos
# ========================
MODEL_PATH = "models/svm_model.pkl"
SCALER_PATH = "models/scaler.pkl"
LABEL_ENCODERS_PATH = "models/label_encoders.pkl"

PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

CONFUSION_PATH = os.path.join(PLOTS_DIR, "confusion_matrix.png")
ROC_PATH = os.path.join(PLOTS_DIR, "roc_curve.png")
PR_PATH = os.path.join(PLOTS_DIR, "precision_recall_curve.png")

# ========================
# Cargar modelo y scaler
# ========================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

with open(LABEL_ENCODERS_PATH, "rb") as f:
    label_encoders = pickle.load(f)

# ========================
# Cargar datos de prueba
# ========================
df = pd.read_csv("bank-full.csv", sep=';')
for col, le in label_encoders.items():
    df[col] = le.transform(df[col])

X = df.drop('y', axis=1)
y = df['y']

X_scaled = scaler.transform(X)

# Predicciones y métricas
y_pred = model.predict(X_scaled)
y_prob = model.predict_proba(X_scaled)[:, 1]

accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)
roc_auc = roc_auc_score(y, y_prob)
cm = confusion_matrix(y, y_pred)

# ========================
# Generar gráficas
# ========================
# Matriz de confusión
fig, ax = plt.subplots(figsize=(5,4))
ConfusionMatrixDisplay(cm, display_labels=["No","Yes"]).plot(ax=ax)
plt.title("Matriz de Confusión - SVM")
plt.savefig(CONFUSION_PATH)
plt.close(fig)

# Curva ROC
fig, ax = plt.subplots()
RocCurveDisplay.from_estimator(model, X_scaled, y, ax=ax)
plt.title("Curva ROC/AUC - SVM")
plt.savefig(ROC_PATH)
plt.close(fig)

# Curva Precisión-Recall
fig, ax = plt.subplots()
PrecisionRecallDisplay.from_estimator(model, X_scaled, y, ax=ax)
plt.title("Curva Precisión vs Recall - SVM")
plt.savefig(PR_PATH)
plt.close(fig)

# ========================
# Endpoints API
# ========================
@app.get("/")
def root():
    return {"message": "API de Clasificación SVM con métricas y gráficas"}

@app.get("/metrics")
def get_metrics():
    return JSONResponse({
        "Modelo": "Support Vector Machine (SVM)",
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1_Score": round(f1, 4),
        "ROC_AUC": round(roc_auc, 4),
        "Confusion_Matrix": cm.tolist()
    })

@app.get("/plot/confusion")
def get_confusion_plot():
    return FileResponse(CONFUSION_PATH)

@app.get("/plot/roc")
def get_roc_plot():
    return FileResponse(ROC_PATH)

@app.get("/plot/precision_recall")
def get_precision_recall_plot():
    return FileResponse(PR_PATH)
