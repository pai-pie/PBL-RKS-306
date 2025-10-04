// Authentication System
class AuthSystem {
  constructor() {
    this.users = JSON.parse(localStorage.getItem('guardiantix_users')) || [];
    this.currentUser = JSON.parse(localStorage.getItem('guardiantix_current_user')) || null;
  }

  register(userData) {
    if (this.users.find(u => u.email === userData.email)) {
      return { success: false, message: 'A wizard already exists with this owl post address!' };
    }

    if (userData.password.length < 8) {
      return { success: false, message: 'Secret spell must be at least 8 magical characters long!' };
    }

    if (userData.password !== userData.confirmPassword) {
      return { success: false, message: 'Secret spells do not match!' };
    }

    const newUser = {
      id: Date.now().toString(),
      username: userData.username,
      email: userData.email,
      password: userData.password,
      joinDate: new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }),
      phone: userData.phone || ''
    };

    this.users.push(newUser);
    localStorage.setItem('guardiantix_users', JSON.stringify(this.users));

    return { success: true, user: newUser };
  }

  isLoggedIn() {
    return this.currentUser !== null;
  }
}

const auth = new AuthSystem();
const errorMessage = document.getElementById("errorMessage");
const successMessage = document.getElementById("successMessage");

// Check if already logged in
if (auth.isLoggedIn()) {
  window.location.href = 'homepage.html';
}

// Real-time password matching
document.addEventListener('DOMContentLoaded', function() {
  const password = document.getElementById('password');
  const confirm = document.getElementById('confirm');
  
  function validatePasswords() {
    if(password.value && confirm.value && password.value !== confirm.value) {
      confirm.style.borderColor = '#C73E3E';
      confirm.style.boxShadow = '0 0 10px rgba(199, 62, 62, 0.3)';
    } else if(password.value && confirm.value && password.value === confirm.value) {
      confirm.style.borderColor = '#FFD700';
      confirm.style.boxShadow = '0 0 10px rgba(255, 215, 0, 0.3)';
    }
  }
  
  password.addEventListener('input', validatePasswords);
  confirm.addEventListener('input', validatePasswords);
});

const form = document.getElementById("registerForm");
form.addEventListener("submit", function(e){
  e.preventDefault();
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm").value;

  if (!username || !email || !password || !confirmPassword) {
    errorMessage.textContent = 'Please fill in all magical fields!';
    errorMessage.style.display = 'block';
    return;
  }

  const result = auth.register({
    username,
    email,
    password,
    confirmPassword
  });

  if (result.success) {
    const button = document.querySelector('button[type="submit"]');
    button.textContent = 'Casting Registration Spell...';
    button.disabled = true;

    errorMessage.style.display = 'none';
    successMessage.textContent = '✨ Magical account created successfully! Redirecting to login...';
    successMessage.style.display = 'block';

    setTimeout(() => {
      window.location.href = "login.html?registered=true";
    }, 2000);
  } else {
    errorMessage.textContent = result.message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
  }
});
