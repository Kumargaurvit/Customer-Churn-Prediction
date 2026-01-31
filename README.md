# Customer Churn Prediction

A production-ready, end-to-end machine learning solution for predicting customer churn with automated MLOps pipeline, scalable architecture, and seamless cloud deployment.

## 🚀 Project Overview

This project implements a comprehensive customer churn prediction system designed for real-world production environments. It features a complete ML lifecycle automation, from data ingestion to model deployment, with a focus on scalability, maintainability, and ease of deployment.

## ✨ Key Features

### 🔄 End-to-End ML Pipeline
- **Automated ML Lifecycle**: Complete automation of data ingestion, preprocessing, feature engineering, model training, and evaluation
- **Modular Architecture**: Well-structured pipeline components for easy maintenance and updates
- **Reproducible Results**: Consistent model training and evaluation across different environments

### 🌐 Interactive User Interface
- **FastAPI Backend**: High-performance API for model predictions and training triggers
- **Streamlit Frontend**: Intuitive web interface for user interaction and visualization
- **Real-time Predictions**: Instant churn predictions with comprehensive insights
- **Asynchronous Processing**: Non-blocking operations for improved user experience

### 🐳 Containerization
- **Docker Integration**: Fully containerized application for consistent deployment
- **Multi-stage Builds**: Optimized Docker images for production efficiency
- **Easy Local Testing**: Spin up the entire application with a single command
- **Environment Isolation**: No dependency conflicts across different systems

### ☁️ AWS Cloud Integration
- **S3 Bucket Sync**: Automated data and model artifact syncing to AWS S3
- **ECR Integration**: Docker images pushed to Amazon Elastic Container Registry
- **EC2 Deployment**: Application hosted on AWS EC2 instances
- **Scalable Infrastructure**: Cloud-native architecture ready for horizontal scaling

### 🔁 CI/CD Pipeline
- **GitHub Actions Workflow**: Automated testing, building, and deployment
- **Self-Hosted Runner**: Dedicated EC2-based runner for secure deployments
- **Continuous Integration**: Automated testing on every code push
- **Continuous Deployment**: Seamless deployment to production environment

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   FastAPI       │◄────►│  ML Pipeline     │
│   Backend       │      │  Components      │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│   Docker        │      │  AWS S3          │
│   Container     │      │  (Data/Models)   │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│   AWS ECR/EC2   │
└─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- AWS Account (for cloud deployment)
- GitHub Account (for CI/CD)

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/customer-churn-prediction.git
   cd customer-churn-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t customer-churn-prediction .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 -p 8501:8501 customer-churn-prediction
   ```

3. **Access the application**
   - Streamlit UI: http://localhost:8501
   - FastAPI Docs: http://localhost:8000/docs

## 🚀 Usage

### Training the Model

```python
# Via API
curl -X POST "http://localhost:8000/train" \
     -H "Content-Type: application/json"

# Via Streamlit UI
# Navigate to the Training page and click "Start Training"
```

### Making Predictions

```python
# Via API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"feature1": value1, "feature2": value2, ...}'

# Via Streamlit UI
# Navigate to the Prediction page and input customer data
```

## ☁️ AWS Deployment

### Prerequisites
- AWS CLI configured
- IAM user with appropriate permissions
- S3 bucket created
- ECR repository created

## 📞 Contact

For questions, suggestions, or issues, please open an issue on GitHub or contact:
- Email: kumargaurvit@example.com
- LinkedIn: (https://linkedin.com/in/gaurvitkumar)

---

**Note**: This is a production-ready system designed for scalability and reliability. For production deployment, ensure proper security measures, monitoring, and testing are in place.