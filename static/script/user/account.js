// Load current user info
document.addEventListener('DOMContentLoaded', function () {
  const currentUser = JSON.parse(localStorage.getItem('guardiantix_current_user'));
  const users = JSON.parse(localStorage.getItem('guardiantix_users')) || [];

  if (!currentUser) {
    window.location.href = "login.html";
    return;
  }

  // Fill profile info
  document.getElementById("userName").textContent = currentUser.username;
  document.getElementById("userEmail").textContent = currentUser.email;
  document.getElementById("joinDate").textContent = currentUser.joinDate || "Unknown";

  // Stats
  document.getElementById("totalTickets").textContent = currentUser.tickets ? currentUser.tickets.length : 0;
  document.getElementById("upcomingEvents").textContent = "0"; // bisa dihitung dari data tiket
  document.getElementById("memberSince").textContent = new Date(currentUser.joinDate).getFullYear();

  // Load tickets
  const ticketsList = document.getElementById("ticketsList");
  if (currentUser.tickets && currentUser.tickets.length > 0) {
    ticketsList.innerHTML = "";
    currentUser.tickets.forEach(ticket => {
      const div = document.createElement("div");
      div.classList.add("ticket-item");
      div.textContent = `🎟️ ${ticket.event} - ${ticket.date}`;
      ticketsList.appendChild(div);
    });
  }
});

// Edit Modal
function openEditModal() {
  document.getElementById("editModal").style.display = "flex";
  const currentUser = JSON.parse(localStorage.getItem('guardiantix_current_user'));
  document.getElementById("editName").value = currentUser.username;
  document.getElementById("editEmail").value = currentUser.email;
  document.getElementById("editPhone").value = currentUser.phone || "";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

function saveProfile() {
  const users = JSON.parse(localStorage.getItem('guardiantix_users')) || [];
  let currentUser = JSON.parse(localStorage.getItem('guardiantix_current_user'));

  const name = document.getElementById("editName").value.trim();
  const email = document.getElementById("editEmail").value.trim();
  const phone = document.getElementById("editPhone").value.trim();

  if (!name || !email) {
    alert("Please fill in required fields!");
    return;
  }

  // Update current user
  currentUser.username = name;
  currentUser.email = email;
  currentUser.phone = phone;

  // Update in users array
  const index = users.findIndex(u => u.id === currentUser.id);
  if (index !== -1) {
    users[index] = currentUser;
    localStorage.setItem('guardiantix_users', JSON.stringify(users));
    localStorage.setItem('guardiantix_current_user', JSON.stringify(currentUser));
    alert("Profile updated successfully!");
    closeEditModal();
    location.reload();
  }
}

// Dummy actions
function downloadAllTickets() {
  alert("Downloading all tickets... (dummy)");
}

function viewPaymentHistory() {
  alert("Viewing payment history... (dummy)");
}

function changePassword() {
  alert("Change password feature coming soon!");
}

function contactSupport() {
  alert("Contacting support owl post... 🦉");
}
