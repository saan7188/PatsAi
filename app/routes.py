from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Patient, Donor, db
from app.empathy_scoring import match_donors
from app.api_integration import fetch_donor_data, notify_donor
import plotly.express as px
import pandas as pd

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

@main_bp.route('/match/<patient_id>')
@login_required
def match_patient(patient_id):
    patient = Patient.query.get(patient_id)
    donors = fetch_donor_data(patient.blood_type)
    top_donors = match_donors(patient.__dict__, donors)
    if top_donors:
        notify_donor(top_donors[0]["id"], patient_id)
    return render_template('match_results.html', top_donors=top_donors)

@main_bp.route('/analytics')
@login_required
def analytics():
    df = pd.DataFrame([d.__dict__ for d in Donor.query.all()])
    fig = px.bar(df.groupby('blood_type').size().reset_index(name='count'),
                 x='blood_type', y='count', title='Donor Distribution by Blood Type')
    graph_json = fig.to_json()
    return render_template('analytics.html', graph_json=graph_json)

@main_bp.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all()
    patient = Patient(id="P001", blood_type="A+", last_transfusion=datetime(2025, 7, 15), urgency=0.9)
    donor1 = Donor(id="D001", blood_type="A+", last_donation=datetime(2025, 6, 20), frequency=4, response_time_hours=2)
    donor2 = Donor(id="D002", blood_type="A+", last_donation=datetime(2025, 7, 10), frequency=2, response_time_hours=5)
    db.session.add_all([patient, donor1, donor2])
    db.session.commit()
    return "Database initialized!"
