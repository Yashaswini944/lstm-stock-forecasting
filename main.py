from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError   # <-- ADD THIS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load TensorFlow model  <-- REPLACE THIS BLOCK
model = load_model(
    "model/lstm_stock_model.h5",
    custom_objects={"mse": MeanSquaredError()},
    compile=False
)
# -----------------------

# Load scaler
scaler = joblib.load("scaler/scaler.pkl")

WINDOW_SIZE = 60

class ForecastRequest(BaseModel):
    days: int

@app.get("/")
def home():
    return {"message": "TensorFlow LSTM Stock Forecasting API is running"}

@app.post("/predict")
def predict(request: ForecastRequest):
    days = request.days

    # Load last sequence
    try:
        last_sequence = np.load("last_sequence.npy")
    except:
        return {"error": "last_sequence.npy not found"}

    # Reshape for LSTM input
    current_seq = last_sequence.reshape(1, WINDOW_SIZE, 1)

    future_predictions = []

    for _ in range(days):
        next_pred = model.predict(current_seq)[0][0]
        future_predictions.append(next_pred)

        # Slide window forward
        current_seq = np.append(current_seq[:, 1:, :], [[[next_pred]]], axis=1)

    # Inverse scale predictions
    future_predictions = scaler.inverse_transform(
        np.array(future_predictions).reshape(-1, 1)
    )

    return {
        "days_requested": days,
        "forecast": future_predictions.flatten().tolist()
    }
