from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from model import predict
from contextlib import asynccontextmanager
import pandas as pd
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import playergamelog, boxscoretraditionalv3, boxscoreusagev3, shotchartdetail, commonteamroster, playergamelogs
from typing import List, Dict, Optional, Union, Tuple
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import time


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

@app.get("/todays_games")
def get_todays_games():
    games = scoreboard.ScoreBoard().games.get_dict()
    game_list = []

    for game in games:
        game_list.append({
            "game_id": game["gameId"],
            "home_team": game["homeTeam"]["teamName"],
            "away_team": game["awayTeam"]["teamName"],
            "home_id": game["homeTeam"]["teamId"],
            "away_id": game["awayTeam"]["teamId"],
            "home_tri": game["homeTeam"]["teamTricode"],
            "away_tri": game["awayTeam"]["teamTricode"]

        })

    return pd.DataFrame(game_list)
