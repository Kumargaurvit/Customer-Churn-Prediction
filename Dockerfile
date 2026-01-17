# Use python 3.13 Base Image
FROM python:3.13-slim

# Copy project files to /app dir
COPY . /app

# Set workdir to /app
WORKDIR /app

# Install all requirements
RUN RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 and 8501 for fastapi and streamlit
EXPOSE 8000
EXPOSE 8501

# Run command to start project service
CMD ["bash","-c","uvicorn src.api.predict_api:app --host 0.0.0.0 --port 8000 --reload & streamlit run churn_app.py"]