from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from model import predict
from contextlib import asynccontextmanager


app = FastAPI()
multi_output_model = None

# Define request schema
class PredictionInput(BaseModel):
    features: list[float]  # Make sure this matches the shape of your model input

@asynccontextmanager
async def lifespan(app: FastAPI):
    global multi_output_model
    # Load the entire MultiOutputRegressor model
    multi_output_model = joblib.load('./app/model/NBA_XGB_MultiOutput_Regressor.pkl')
    print("MultiOutputRegressor model loaded successfully!")
    
    yield
    
    # Code to clean up during shutdown (optional)
    multi_output_model = None
    print("Model unloaded during shutdown")

# Attach the lifespan context manager to the FastAPI app
app.state.lifespan = lifespan

@app.post("/predict")
async def get_prediction(data: PredictionInput):
    # Convert input list to NumPy array and reshape for model
    input_array = np.array(data.features).reshape(1, -1)
    
    # Get prediction
    prediction = predict(input_array)

    return {"prediction": prediction.tolist()}
