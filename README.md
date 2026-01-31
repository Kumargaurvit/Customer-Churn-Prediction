# 🎯 Customer Churn Prediction

## 📌 Project Overview

The **Customer Churn Prediction** is a Machine Learning web application that predicts customer churn using behavioral, demographic, and transactional data to support proactive customer retention strategies.

The system automates the **end-to-end ML pipeline**, including:
- Data ingestion from MongoDB
- Data validation and drift detection
- Data transformation
- Model training and evaluation
- Prediction through a Streamlit + FastAPI integration based web interface

It is built with **production-grade architecture**, following modular design, logging, exception handling, and CI/CD readiness.

---

## 🎯 Problem Statement

Customer churn poses a significant challenge for businesses, as losing existing customers directly impacts revenue and growth.
This project aims to classify customers as likely to churn or remain retained by analyzing historical customer data and behavioral patterns, helping organizations take proactive retention measures.

---

## 🧠 Solution Approach

1. **Dataset**
   - Customer Churn Data stored in MongoDB

2. **Machine Learning Pipeline**
   - Data Ingestion
   - Data Validation (Schema & Drift Detection)
   - Data Transformation (Preprocessing & Imputation)
   - Model Training (Classification models)
   - Model Evaluation
   - Pydantic model based input for input verification
   - Prediction & Output generation

3. **Web API**
   - FastAPI-based REST service
   - Streamlit Web App for easy User Interaction and Manual feature input

---

## ⚙️ Tech Stack Used

### 🔹 Programming & Frameworks
- Python 3.13
- FastAPI
- Uvicorn
- Streamlit
- Pydantic

### 🔹 Machine Learning
- Scikit-learn
- NumPy
- Pandas
- Pickle

### 🔹 Database
- MongoDB Atlas
- PyMongo

### 🔹 DevOps & MLOps
- GitHub Actions
- Docker-ready architecture
- MLFlow and DAGsHub
- Data Drift Detection
- Logging & Exception Handling

### 🔹 Cloud Deployment
- Amazon S3 Bucket (Artifact and Model Storage)
- Amazon ECR (Docker Image Repository)
- Amazon EC2 Instance (Web App Deployment)

---

## 🗄 MongoDB Atlas Setup

1. Create a MongoDB Atlas account:  
   https://www.mongodb.com/cloud/atlas

2. Create a new cluster (Free Tier M0 works)

3. Create a database and collection:
   - Database name: `your_db_name`
   - Collection name: `your_collection_name`

4. Add your IP address to **Network Access**

5. Create a database user and note:
   - Username
   - Password

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<db_name>?retryWrites=true&w=majority
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run the FastAPI Application
```bash
python app.py
```

## ▶️ Run the Training Pipeline Locally
```bash
python main.py
```