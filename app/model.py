import joblib
import numpy as np
from pathlib import Path

# Load the model
MODEL_PATH = Path(__file__).parent / "model" / "NBA_XGB_MultiOutput.pkl"
xgb_model = joblib.load(MODEL_PATH)

def predict(input_data: np.ndarray):
    """Runs a prediction using the loaded model."""
    return xgb_model.predict(input_data)