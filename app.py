from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import os

app = Flask(__name__)

# Load CSV Data
def load_data():
    patients = pd.read_csv("data/patients.csv")
    donors = pd.read_csv("data/donors.csv")
    return patients, donors

# Donor empathy prediction (stub logic)
def predict_empathy():
    return round(random.uniform(0.5, 1.0), 2)

# Match top 3 donors
def match_donors(patient_id, patients, donors):
    patient = patients[patients["id"] == int(patient_id)].iloc[0]
    donor_scores = []
    for _, donor in donors.iterrows():
        donor_scores.append({
            "name": donor["name"],
            "last_donation_days": donor["last_donation_days"],
            "empathy_score": predict_empathy()
        })
    top_donors = sorted(donor_scores, key=lambda x: x["empathy_score"], reverse=True)[:3]
    return patient.to_dict(), top_donors

@app.route('/', methods=['GET', 'POST'])
def index():
    patients, donors = load_data()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        try:
            patient, matches = match_donors(patient_id, patients, donors)
            return render_template('result.html', patient=patient, matches=matches)
        except:
            return render_template('index.html', patients=patients, error="Invalid Patient ID")
    return render_template('index.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
