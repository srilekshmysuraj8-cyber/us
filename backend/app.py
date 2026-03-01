from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import datetime
import os

app = Flask(__name__)
CORS(app) # Allows your friend's frontend to connect securely!

# Load the AI Model
try:
    model = joblib.load('model/wait_time_model.pkl')
    print("✅ AI Model loaded successfully!")
except Exception as e:
    print("❌ Error loading AI Model. Make sure to run train_model.py first!")

# --- API 1: PATIENT LOGIN ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    df = pd.read_csv('datasets/PATIENTS.csv')
    
    # 🚨 UPDATED LOGIC: Checking Patient_ID and Name instead of Phone/Password
    user = df[(df['Patient_ID'] == data.get('patient_id')) & (df['Name'] == data.get('name'))]
    
    if not user.empty:
        return jsonify({
            "status": "success", 
            "patient_id": user.iloc[0]['Patient_ID'], 
            "name": user.iloc[0]['Name'], 
            "age": int(user.iloc[0]['Age'])
        }), 200
        
    return jsonify({"status": "error", "message": "Invalid Patient ID or Name."}), 401

# --- API 2: GET ALL DOCTORS ---
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    # Because we use to_dict, this automatically sends all 14 doctors and their new Consultation Times!
    df = pd.read_csv('datasets/DOCTORS.csv')
    return jsonify(df.to_dict(orient='records')), 200

# --- API 3: BOOK AN APPOINTMENT ---
@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    app_df = pd.read_csv('datasets/APPOINTMENTS.csv')
    queue_df = pd.read_csv('datasets/TODAYS_QUEUE.csv')
    
    # Generate a unique Booking ID (e.g., B001, B002)
    booking_id = f"B{len(app_df) + 1:03d}"
    
    # Add to Appointments (Master Calendar)
    new_app = {
        "Booking_ID": booking_id, 
        "Patient_ID": data['patient_id'], 
        "Doctor_ID": data['doctor_id'], 
        "Appointment_Date": datetime.datetime.now().strftime("%Y-%m-%d"), 
        "Status": "Booked"
    }
    app_df.loc[len(app_df)] = new_app
    app_df.to_csv('datasets/APPOINTMENTS.csv', index=False)
    
    # Add to Today's Queue (Wait time starts at 0 until they physically check in)
    new_queue = {
        "Booking_ID": booking_id, 
        "Patient_Name": data['patient_name'], 
        "Age": data['age'], 
        "Doctor_ID": data['doctor_id'], 
        "Status": "Booked", 
        "Estimated_Wait": 0
    }
    queue_df.loc[len(queue_df)] = new_queue
    queue_df.to_csv('datasets/TODAYS_QUEUE.csv', index=False)
    
    return jsonify({"status": "success", "booking_id": booking_id}), 200

# --- API 4: PHYSICAL CHECK-IN (The AI Engine) ---
@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    df = pd.read_csv('datasets/TODAYS_QUEUE.csv')
    patient = df[df['Booking_ID'] == data.get('booking_id')]
    
    if not patient.empty:
        # Change status from Booked to Waiting
        df.loc[df['Booking_ID'] == data['booking_id'], 'Status'] = 'Waiting'
        
        # Prepare the clues for the AI
        age = int(patient.iloc[0]['Age'])
        doc_id = int(patient.iloc[0]['Doctor_ID'])
        current_hour = datetime.datetime.now().hour
        # Count how many people are waiting specifically for THIS doctor
        queue_size = len(df[(df['Status'] == 'Waiting') & (df['Doctor_ID'] == doc_id)])
        
        # Ask the AI for the prediction
        wait_time = int(round(model.predict([[age, doc_id, current_hour, queue_size]])[0]))
        
        # Save the wait time
        df.loc[df['Booking_ID'] == data['booking_id'], 'Estimated_Wait'] = wait_time
        df.to_csv('datasets/TODAYS_QUEUE.csv', index=False)
        
        return jsonify({"status": "success", "wait_time": wait_time}), 200
        
    return jsonify({"status": "error", "message": "Booking ID not found."}), 404

# --- API 5: GET LIVE QUEUE DASHBOARD ---
@app.route('/api/queue', methods=['GET'])
def get_queue():
    df = pd.read_csv('datasets/TODAYS_QUEUE.csv')
    # Send only the patients who are physically waiting in the hospital
    waiting = df[df['Status'] == 'Waiting'].to_dict(orient='records')
    return jsonify(waiting), 200
# --- API 6: DOCTOR COMPLETES CONSULTATION (Move the queue forward!) ---
@app.route('/api/doctor/done', methods=['POST'])
def doctor_done():
    data = request.json
    booking_id = data.get('booking_id')
    
    df = pd.read_csv('datasets/TODAYS_QUEUE.csv')
    
    if booking_id in df['Booking_ID'].values:
        # Mark the patient as Completed so they drop off the live dashboard
        df.loc[df['Booking_ID'] == booking_id, 'Status'] = 'Completed'
        df.to_csv('datasets/TODAYS_QUEUE.csv', index=False)
        
        return jsonify({"status": "success", "message": "Consultation done!"}), 200
        
    return jsonify({"status": "error", "message": "Booking ID not found."}), 404

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(debug=True, port=5000)