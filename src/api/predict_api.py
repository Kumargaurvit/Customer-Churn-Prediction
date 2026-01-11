from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import sys

from src.pydantic_model.pydantinc_model import UserInput
from src.exception.exception import CustomerChurnException
from src.utils.ml_utils import preprocess

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def home():
    return "Customer Churn Predicition API"

@app.post('/predict')
def churn_prediction(data: UserInput):
    try:
        input_data = pd.DataFrame([data.model_dump()])

        test_data, model = preprocess(input_data)

        prediction = model.predict_proba(test_data)[0][1]

        return JSONResponse(status_code=200, content={'predicted' : prediction})
    except Exception as e:
        raise CustomerChurnException(e,sys)