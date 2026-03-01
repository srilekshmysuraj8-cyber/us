const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

// Sliding Animation logic
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// REDIRECT LOGIC: This moves the user to the selection page
// We look for the "Sign In" button inside the white form
const signInSubmit = document.querySelector('.sign-in button');

signInSubmit.addEventListener('click', (e) => {
    e.preventDefault(); // Prevents the page from just refreshing
    window.location.href = "selection.html"; 
});