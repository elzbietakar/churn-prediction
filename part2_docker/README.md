# Dockerized Run

Build and start both services (API and Streamlit UI):

```bash
docker compose build
docker compose up -d
```

API available at: http://localhost:5000

Endpoints:
http://localhost:5000/health [GET],
http://localhost:5000/metrics [GET], 
http://localhost:5000/api/predict [POST]

Example test data available at: models/test_api_data.json

Streamlit UI available at: http://localhost:8501