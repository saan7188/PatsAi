import requests
from twilio.rest import Client
from app.models import Donor

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE = "+1234567890"
MOCK_API_URL = "https://api.example.com/donors"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def fetch_donor_data(blood_type):
    try:
        response = requests.get(MOCK_API_URL, params={"blood_type": blood_type})
        return response.json()
    except:
        return [d.__dict__ for d in Donor.query.filter_by(blood_type=blood_type).all()]

def notify_donor(donor_id, patient_id):
    message = client.messages.create(
        body=f"Urgent: Thalassemia patient {patient_id} needs your blood donation. Respond ASAP!",
        from_=TWILIO_PHONE,
        to="+919876543210"
    )
    return message.sid
