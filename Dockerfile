# Use python as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install required packages
# Make sure you have a requirements.txt with fastapi, uvicorn, and streamlit
COPY . /app
RUN apt update -y && apt install awscli -y
RUN apt-get update && pip install -r requirements.txt

# Expose ports
# 8000 for FastAPI, 8501 for Streamlit
EXPOSE 8000 8501

# Create a startup script to run both services
RUN echo '#!/bin/bash\n\
uvicorn churn_api:app --host 0.0.0.0 --port 8000 &\n\
streamlit run churn_app.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run both services
CMD ["/app/start.sh"]