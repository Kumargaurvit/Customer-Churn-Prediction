import os
import sys
import streamlit as st
import requests
from dotenv import load_dotenv
load_dotenv()

CHURN_PREDICTION_API = os.getenv("CHURN_PREDICTION_API")

from src.exception.exception import CustomerChurnException

# Page configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="wide",
    page_icon="📊"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Output box styling */
    .output-box {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 2px solid #e0e0e0;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: 2rem;
    }
    
    .output-title {
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .prediction-result {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .churn-yes {
        color: #dc3545;
    }
    
    .churn-no {
        color: #28a745;
    }
    
    .probability-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1.5rem;
    }
    
    /* Progress bar container */
    .progress-container {
        width: 100%;
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 30px;
        margin-top: 1rem;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        border-radius: 10px;
        transition: width 0.6s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        margin-top: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Placeholder box styling */
    .placeholder-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 2rem;
    }
    
    .placeholder-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .placeholder-text {
        font-size: 1.2rem;
        color: #666;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🎯 Customer Churn Prediction</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">A Machine Learning based Web App to predict if customer is likely to churn or not</p>', unsafe_allow_html=True)

st.markdown("---")

# Create two columns - Input on left, Output on right
col_input, col_output = st.columns([1, 1], gap="large")

# Initialize session state for prediction result
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
    st.session_state.prediction_result = None
    st.session_state.churn_probability = 0

try:
    with col_input:
        st.markdown('<div class="section-header">📝 Customer Information</div>', unsafe_allow_html=True)
        
        CreditScore = st.number_input("Enter your Credit Score", min_value=0, max_value=900, value=500, step=1)
        Geography = st.selectbox("Select your Country", options=["France","Spain","Germany"], index=None, placeholder="Choose a country")
        Gender = st.selectbox("Select your Gender", options=["Male","Female"], index=None, placeholder="Choose gender")
        Age = st.slider("Select your Age", min_value=0, max_value=100, value=18)
        Tenure = st.slider("How many years you have been with the bank?", min_value=0, max_value=10, value=0)
        Balance = st.number_input("How much money do you currently have in the bank account?", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        NumOfProducts = st.number_input("How many bank products you currently use?", min_value=0, max_value=10, value=0, step=1)
        HasCrCard = st.selectbox("Do you currently have a credit card (0->No, 1->Yes)?", options=[0,1], index=None, placeholder="Select option")
        IsActiveMember = st.selectbox("Are you an active member of the bank (0->No, 1->Yes)?", options=[0,1], index=None, placeholder="Select option")
        EstimatedSalary = st.number_input("What is your estimated salary? (Monthly)", min_value=0.0, value=0.0, step=0.01, format="%.2f")

        if st.button("🔮 Predict Customer Churn"):
            # Validation
            if Geography is None or Gender is None or HasCrCard is None or IsActiveMember is None:
                st.error("⚠️ Please fill in all required fields!")
            else:
                with st.spinner("Prediction in progress..."):
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
                            churn_prob = result['predicted']
                            
                            # Store results in session state
                            st.session_state.prediction_made = True
                            st.session_state.churn_probability = churn_prob
                            
                            if churn_prob >= 0.5:
                                st.session_state.prediction_result = "likely"
                            else:
                                st.session_state.prediction_result = "not_likely"
                                
                    except Exception as e:
                        raise CustomerChurnException(e,sys)
    
    with col_output:
        st.markdown('<div class="section-header">📊 Prediction Result</div>', unsafe_allow_html=True)
        
        if st.session_state.prediction_made:
            # Display output box with result
            churn_prob = st.session_state.churn_probability
            percentage = churn_prob * 100
            
            if st.session_state.prediction_result == "likely":
                result_class = "churn-yes"
                result_text = "Likely to Churn"
                result_icon = "⚠️"
            else:
                result_class = "churn-no"
                result_text = "Not Likely to Churn"
                result_icon = "✅"
            
            # Create the output box
            st.markdown(f"""
                <div class="output-box">
                    <div class="output-title">Prediction Outcome</div>
                    <div class="prediction-result {result_class}">
                        {result_icon} {result_text}
                    </div>
                    <div class="probability-text">
                        Churn Probability: {percentage:.2f}%
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {percentage}%;">
                            {percentage:.1f}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Placeholder when no prediction has been made
            st.markdown("""
                <div class="placeholder-box">
                    <div class="placeholder-icon">📊</div>
                    <div class="placeholder-text">
                        Fill in customer details and click<br>"Predict Customer Churn"<br>to see results here
                    </div>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    raise CustomerChurnException(e,sys)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p style="font-size: 0.9rem;">Built with ❤️ using Streamlit & Machine Learning</p>
    </div>
""", unsafe_allow_html=True)