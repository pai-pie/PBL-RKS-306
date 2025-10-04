// Authentication System
class AuthSystem {
  constructor() {
    this.users = JSON.parse(localStorage.getItem('guardiantix_users')) || [];
    this.currentUser = JSON.parse(localStorage.getItem('guardiantix_current_user')) || null;
  }

  login(email, password) {
    const user = this.users.find(u => u.email === email && u.password === password);
    if (user) {
      this.currentUser = user;
      localStorage.setItem('guardiantix_current_user', JSON.stringify(user));
      return { success: true, user };
    }
    return { success: false, message: 'Invalid magical credentials! Please check your owl post address and secret spell.' };
  }

  register(userData) {
    // Check if user already exists
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
    
    // Auto login after registration
    this.currentUser = newUser;
    localStorage.setItem('guardiantix_current_user', JSON.stringify(newUser));

    return { success: true, user: newUser };
  }

  logout() {
    this.currentUser = null;
    localStorage.removeItem('guardiantix_current_user');
  }

  isLoggedIn() {
    return this.currentUser !== null;
  }

  getCurrentUser() {
    return this.currentUser;
  }
}

const auth = new AuthSystem();

// Check if already logged in
if (auth.isLoggedIn()) {
  window.location.href = 'homepage.html';
}

// Event submit
const loginForm = document.getElementById("loginForm");
const errorMessage = document.getElementById("errorMessage");
const successMessage = document.getElementById("successMessage");

// Check for success message from registration
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('registered') === 'true') {
  successMessage.textContent = '✨ Magical account created successfully! Please sign in.';
  successMessage.style.display = 'block';
  
  // Remove parameter from URL
  window.history.replaceState({}, document.title, window.location.pathname);
}

loginForm.addEventListener("submit", function(e){
  e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  // Basic validation
  if (!email || !password) {
    errorMessage.textContent = 'Please fill in all magical fields!';
    errorMessage.style.display = 'block';
    return;
  }

  const result = auth.login(email, password);
  
  if (result.success) {
    // Add magical loading effect
    const button = document.querySelector('button[type="submit"]');
    const originalText = button.textContent;
    button.textContent = 'Casting Sign In Spell...';
    button.disabled = true;

    // Show success message
    errorMessage.style.display = 'none';
    successMessage.textContent = '✨ Welcome back! Redirecting to your magical journey...';
    successMessage.style.display = 'block';

    setTimeout(() => {
      window.location.href = "homepage.html";
    }, 1500);
  } else {
    errorMessage.textContent = result.message;
    errorMessage.style.display = 'block';
    successMessage.style.display = 'none';
  }
});

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('input');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.style.transform = 'scale(1.02)';
    });
    input.addEventListener('blur', function() {
      this.style.transform = 'scale(1)';
    });
  });
});
