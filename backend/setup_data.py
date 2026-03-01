import pandas as pd
import os
import random
from datetime import datetime, timedelta

# Ensure directories exist
if not os.path.exists('datasets'):
    os.makedirs('datasets')

print("🏥 Booting up Smart Hospital Simulator...")
print("Generating new datasets...\n")

# --- 1. DOCTORS DATASET ---
doctors_data = [
    [1, "Dr. Alice Smith", "Physician", "09:00 AM - 01:00 PM"],
    [2, "Dr. Robert Brown", "Physician", "02:00 PM - 06:00 PM"],
    [3, "Dr. Elena Rose", "Dermatologist", "10:00 AM - 02:00 PM"],
    [4, "Dr. Chris Evans", "Dermatologist", "03:00 PM - 07:00 PM"],
    [5, "Dr. Maya Angel", "Gynecologist", "08:00 AM - 12:00 PM"],
    [6, "Dr. Sarah Jenkins", "Gynecologist", "01:00 PM - 05:00 PM"],
    [7, "Dr. Xavier Brain", "Neurologist", "09:00 AM - 01:00 PM"],
    [8, "Dr. Lisa Cuddy", "Neurologist", "02:00 PM - 06:00 PM"],
    [9, "Dr. Robert Heart", "Cardiologist", "10:00 AM - 02:00 PM"],
    [10, "Dr. Yang Grey", "Cardiologist", "03:00 PM - 07:00 PM"],
    [11, "Dr. Baby Care", "Pediatrician", "08:00 AM - 12:00 PM"],
    [12, "Dr. John Watson", "Pediatrician", "01:00 PM - 05:00 PM"],
    [13, "Dr. Look Bright", "Ophthalmologist", "09:00 AM - 01:00 PM"],
    [14, "Dr. Iris View", "Ophthalmologist", "02:00 PM - 06:00 PM"]
]
# Updated column to "Consultation_Time" instead of "Room_Number"
doc_df = pd.DataFrame(doctors_data, columns=["Doctor_ID", "Doctor_Name", "Department", "Consultation_Time"])
doc_df.to_csv('datasets/DOCTORS.csv', index=False)
print("✅ DOCTORS.csv created (14 Doctors across 7 Departments).")

# --- 2. PATIENTS DATASET (For Login) ---
# Removed passwords. Login will now use Patient_ID and Name
patients_data = [
    ["P001", "John Doe", "9876543210", 45],
    ["P002", "Jane Smith", "8765432109", 28],
    ["P003", "Alice Brown", "7654321098", 65],
    ["P004", "Bob White", "6543210987", 12]
]
pat_df = pd.DataFrame(patients_data, columns=["Patient_ID", "Name", "Phone_Number", "Age"])
pat_df.to_csv('datasets/PATIENTS.csv', index=False)
print("✅ PATIENTS.csv created (Mock users for login).")

# --- 3. APPOINTMENTS DATASET (Master Booking List) ---
# Completely empty to start
app_df = pd.DataFrame(columns=["Booking_ID", "Patient_ID", "Doctor_ID", "Appointment_Date", "Status"])
app_df.to_csv('datasets/APPOINTMENTS.csv', index=False)
print("✅ APPOINTMENTS.csv created (Empty Master schedule).")

# --- 4. TODAY'S QUEUE DATASET (The Active Tracker) ---
# Completely empty to start
queue_df = pd.DataFrame(columns=["Booking_ID", "Patient_Name", "Age", "Doctor_ID", "Status", "Estimated_Wait"])
queue_df.to_csv('datasets/TODAYS_QUEUE.csv', index=False)
print("✅ TODAYS_QUEUE.csv created (Empty Live tracker for today).")

# --- 5. HISTORICAL DATA (For AI Training) ---
historical_data = []
for _ in range(500):
    age = random.randint(5, 85)
    doc_id = random.randint(1, 14) # UPDATED: Now randomly picks from 1 to 14!
    time_of_day = random.randint(8, 17)
    queue_size = random.randint(0, 15)
    
    # Secret Logic remains exactly the same!
    base_time = 10
    if age > 60: base_time += 5
    if time_of_day > 14: base_time += 3
    if doc_id in [3, 4]: base_time -= 2 # Dermatologists (Elena & Chris) are faster
    
    actual_time = base_time + random.randint(-3, 5) 
    historical_data.append([age, doc_id, time_of_day, queue_size, actual_time])

hist_df = pd.DataFrame(historical_data, columns=["Age", "Doctor_ID", "Time_of_Day", "Queue_Size", "Actual_Consultation_Time"])
hist_df.to_csv('datasets/HISTORICAL_DATA.csv', index=False)
print("✅ HISTORICAL_DATA.csv created (500 records for the AI).")

print("\n🚀 All datasets generated successfully! You are ready to run train_model.py.")