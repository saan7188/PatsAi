import pandas as pd
from datetime import datetime, timedelta

def calculate_empathy_score(donor, patient):
    last_donation = datetime.strptime(donor["last_donation"], "%Y-%m-%d")
    days_since_donation = (datetime.now() - last_donation).days
    if days_since_donation < 56:
        return 0
    if donor["blood_type"] != patient["blood_type"] and donor["blood_type"] != "O-":
        return 0
    frequency_score = min(donor["frequency"] / 10, 1.0)
    recency_score = max(1.0 - (days_since_donation / 365), 0.1)
    response_score = max(1.0 - (donor["response_time_hours"] / 24), 0.1)
    urgency_boost = patient["urgency"]
    score = (0.4 * frequency_score + 0.3 * recency_score + 0.2 * response_score) * (1 + urgency_boost)
    return round(score * 100, 2)

def match_donors(patient, donors):
    ranked_donors = []
    for donor in donors:
        score = calculate_empathy_score(donor, patient)
        if score > 0:
            ranked_donors.append({"id": donor["id"], "score": score, "blood_type": donor["blood_type"]})
    ranked_donors.sort(key=lambda x: x["score"], reverse=True)
    return ranked_donors[:3]
