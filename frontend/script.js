const API_URL = "http://127.0.0.1:5000/api";

async function loginUser() {
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    
    let response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({phone, password})
    });
    
    let data = await response.json();
    if (data.status === "success") {
        // Save user details to browser memory
        localStorage.setItem("patient_id", data.patient_id);
        localStorage.setItem("patient_name", data.name);
        localStorage.setItem("patient_age", data.age);
        window.location.href = "selection.html"; // Move to next page
    } else {
        document.getElementById('error-msg').innerText = "Incorrect Phone or Password.";
    }
}

async function loadDoctors() {
    let response = await fetch(`${API_URL}/doctors`);
    let doctors = await response.json();
    
    let grid = document.getElementById('doctor-grid');
    doctors.forEach(doc => {
        grid.innerHTML += `
            <div class="doctor-card">
                <h3>${doc.Doctor_Name}</h3>
                <p>${doc.Department}</p>
                <button class="book-btn" onclick="bookAppointment(${doc.Doctor_ID})">Book Now</button>
            </div>
        `;
    });
}

async function bookAppointment(doctorId) {
    let response = await fetch(`${API_URL}/book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            patient_id: localStorage.getItem("patient_id"),
            patient_name: localStorage.getItem("patient_name"),
            age: localStorage.getItem("patient_age"),
            doctor_id: doctorId
        })
    });
    
    let data = await response.json();
    if (data.status === "success") {
        alert("Success! Your Booking ID is: " + data.booking_id);
        localStorage.setItem("booking_id", data.booking_id);
        window.location.href = "dashboard.html"; // Move to dashboard
    }
}

async function checkIn() {
    const bookingId = document.getElementById('booking-id-input').value;
    
    let response = await fetch(`${API_URL}/checkin`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({booking_id: bookingId})
    });
    
    let data = await response.json();
    if (data.status === "success") {
        document.getElementById('checkin-section').style.display = 'none';
        document.getElementById('wait-time-display').style.display = 'block';
        document.getElementById('wait-time-display').innerText = `Estimated Wait: ${data.wait_time} mins`;
        loadQueue();
    }
}

async function loadQueue() {
    let response = await fetch(`${API_URL}/queue`);
    let queue = await response.json();
    
    let list = document.getElementById('queue-list');
    list.innerHTML = "";
    queue.forEach(p => {
        list.innerHTML += `<p><b>${p.Booking_ID}</b> - ${p.Patient_Name} (Waiting)</p>`;
    });
}