from fastapi import FastAPI
import numpy as np
import onnxruntime as ort
import joblib

app = FastAPI()

# Load ONNX model
session = ort.InferenceSession("model/model.onnx")

# Load scaler
scaler = joblib.load("model/scaler.pkl")

# Load last sequence
last_sequence = np.load("model/last_sequence.npy")

@app.get("/")
def home():
    return {"message": "LSTM Stock Forecasting API is running!"}

@app.get("/predict")
def predict(days: int = 5):
    seq = last_sequence.reshape(1, 60, 1).astype(np.float32)
    predictions = []

    for _ in range(days):
        inputs = {session.get_inputs()[0].name: seq}
        pred = session.run(None, inputs)[0][0]
        predictions.append(pred)
        seq = np.append(seq[:, 1:, :], [[pred]], axis=1)

    predictions = scaler.inverse_transform(predictions)

    return {
        "days": days,
        "forecast": predictions.flatten().tolist()
    }
