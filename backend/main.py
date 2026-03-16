import os
from datetime import datetime
from joblib import load
from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.request_models import ClienteIn
from models.response_models import ClientOut, ResponseOut
from services.preprocess import preprocesar_cliente

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

app = FastAPI()

with open("modelo_credit_scoring.pkl", "rb") as f:
    modelo = load(f)

with open("scaler_credit_scoring.pkl", "rb") as f:
    scaler = load(f)


@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.post("/predict/", response_model=ResponseOut)
async def predecir(cliente: ClienteIn) -> ResponseOut:
    X = preprocesar_cliente(cliente).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = modelo.predict(X_scaled)[0]
    probability = float(modelo.predict_proba(X_scaled)[0].max())

    return ResponseOut(
        prediction=str(prediction),
        probability=probability,
        cliente=ClientOut(name=cliente.name, email=cliente.email, phoneNum=cliente.phoneNum),
        timestamp=datetime.now(),
    )


@app.get("/health_status")
async def monitoreo():
    pass


@app.get("/informacion_modelo")
async def info_modelo():
    pass
