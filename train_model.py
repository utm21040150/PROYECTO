import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle
import os

# ========================
# Cargar y preparar datos
# ========================
print("Iniciado carga y preparación de datos...")

df = pd.read_csv("bank-full.csv", sep=';')

# Codificar variables categóricas
label_encoders = {}
for col in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop('y', axis=1)
y = df['y']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ========================
# Entrenar modelo SVM
# ========================
print("Entrenando modelo SVM...")

model = SVC(kernel='rbf', probability=True, random_state=42)
model.fit(X_train, y_train)

# ========================
# Guardar modelo y scaler
# ========================
os.makedirs("models", exist_ok=True)
with open("models/svm_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("models/label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print("Modelo, scaler y codificadores guardados en carpeta 'models'.")
