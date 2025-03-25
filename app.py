from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel
from database import insert_feedback, get_all_feedback
from model import train_model, predict, categorize_alert, calculate_accuracy

app = FastAPI(
    title="PagerDuty Feedback System",
    description="An API to fetch PagerDuty incidents, collect feedback, and predict resolutions with accuracy tracking.",
    version="1.0.0"
)

# ✅ Load API Key and Service ID from Environment Variables
PAGERDUTY_API_KEY = os.getenv("PAGERDUTY_API_KEY")
PAGERDUTY_SERVICE_ID = os.getenv("PAGERDUTY_SERVICE_ID")

if not PAGERDUTY_API_KEY or not PAGERDUTY_SERVICE_ID:
    raise ValueError("❌ ERROR: PagerDuty API Key or Service ID is missing. Set them as environment variables.")

class FeedbackRequest(BaseModel):
    incident_id: str
    resolution: str  # Correct, Incorrect, or Partially Correct

@app.get("/incidents", tags=["PagerDuty"])
def get_service_incidents():
    """Fetch all incidents from PagerDuty for a specific service."""
    url = "https://api.pagerduty.com/incidents"
    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_KEY}",
        "Accept": "application/json"
    }
    params = {"service_ids[]": PAGERDUTY_SERVICE_ID}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"❌ Failed to fetch incidents: {response.text}")

    incidents = response.json()["incidents"]
    
    categorized_incidents = [
        {
            "incident_id": incident["id"],
            "title": incident["title"],
            "status": incident["status"],
            "category": categorize_alert(incident["title"])
        }
        for incident in incidents
    ]

    return {"incidents": categorized_incidents}

@app.post("/feedback", tags=["Feedback"])
def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for an incident (Correct, Incorrect, Partially Correct)."""
    try:
        insert_feedback(feedback.incident_id, feedback.resolution)
        return {"message": "✅ Feedback submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback", tags=["Feedback"])
def get_feedback():
    """Retrieve all feedback."""
    try:
        feedback_data = get_all_feedback()
        return feedback_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to retrieve feedback: {str(e)}")

@app.get("/rca_calculator", tags=["AI Model"])
def get_prediction(incident_id: str):
    """Predict the root cause of an incident and calculate accuracy."""
    try:
        predicted_rca, accuracy = predict(incident_id)
        return {
            "root_cause": predicted_rca,
            "accuracy": f"{accuracy:.2f}%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accuracy", tags=["AI Model"])
def get_accuracy():
    """Calculate and return the accuracy of predictions."""
    try:
        accuracy = calculate_accuracy()
        return {"accuracy": f"{accuracy:.2f}%"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train", tags=["AI Model"])
def train():
    """Train the AI model using stored feedback data."""
    try:
        train_model()
        return {"message": "✅ Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

