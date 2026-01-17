import os
import sys
import streamlit as st
import requests
from dotenv import load_dotenv
load_dotenv()

CHURN_PREDICTION_API = os.getenv("CHURN_PREDICTION_API")

from src.exception.exception import CustomerChurnException

st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

st.title("Customer Churn Prediction")
st.subheader("A Machine Learning based Web App to predict if customer is likely to churn or not")

try:
    CreditScore = st.number_input("Enter your Credit Score", min_value=0, max_value=900, value=500, step=1)
    Geography = st.selectbox("Select your Country", options=["France","Spain","Germany"], index=None)
    Gender = st.selectbox("Select your Gender", options=["Male","Female"], index=None)
    Age = st.slider("Select your Age", min_value=0, max_value=100, value=18)
    Tenure = st.slider("How many years you have been with the bank?", min_value=0, max_value=10, value=0)
    Balance = st.number_input("How much money do you currently have in the bank account?", min_value=0, value=0.0, step=0.01, format="%.2f")
    NumOfProducts = st.number_input("How many bank products you currently use?", min_value=0, max_value=10, value=0, step=1)
    HasCrCard = st.selectbox("Do you currently have a credit card (0->No, 1->Yes)?", options=[0,1], index=None)
    IsActiveMember = st.selectbox("Are you an active member of the bank (0->No, 1->Yes)?", options=[0,1], index=None)
    EstimatedSalary = st.number_input("What is your estimated salary? (Monthly)", min_value=0, value=0.0, step=0.01, format="%.2f")

    if st.button("Predict Customer Churn"):
        data = {
        "CreditScore" : CreditScore,
        "Geography" : Geography,
        "Gender" : Gender,
        "Age" : Age,
        "Tenure" : Tenure,
        "Balance" : Balance,
        "NumOfProducts" : NumOfProducts,
        "HasCrCard" : HasCrCard,
        "IsActiveMember" : IsActiveMember,
        "EstimatedSalary" : EstimatedSalary
        }

        try:
            api_response = requests.post(CHURN_PREDICTION_API, json=data)
            if api_response.status_code == 200:
                result = api_response.json()
                if result['predicted'] >= 0.5:
                    st.error("The Customer is likely to churn")
                else:
                    st.success("The Customer is not likely to churn")
        except Exception as e:
            raise CustomerChurnException(e,sys)

except Exception as e:
    raise CustomerChurnException(e,sys)