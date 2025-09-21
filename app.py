from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import pickle


app = FastAPI()

# Static dosyalar için mount
app.mount("/static", StaticFiles(directory="."), name="static")

#Templates
templates = Jinja2Templates(directory="templates")

with open('Gym_.pkl', 'rb') as f:
    saved_data = pickle.load(f)
    model = saved_data['model']


class GYM_Features(BaseModel):
    day_of_week: int
    is_weekend: int
    is_holiday: int
    temperature: float
    is_start_of_semester: int
    is_during_semester: int
    month: int
    hour: int

class PredictionResponse(BaseModel):
    prediction: int

@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/predict")
async def predict(features: GYM_Features):
    input_data = pd.DataFrame([features.model_dump()])

    prediction = model.predict(input_data)[0]

    return {"predicted_price": int(prediction)}





