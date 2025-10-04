// Admin Panel JavaScript
function showSection(id) {
  // Hide all sections
  document.querySelectorAll('.section').forEach(sec => sec.style.display = "none");
  
  // Show selected section
  document.getElementById(id).style.display = "block";
  
  // Update active sidebar link
  document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove("active"));
  event.target.classList.add("active");
}

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function() {
  // Add loading animation
  setTimeout(() => {
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.5s ease';
  }, 100);
  
  // Add sample interactive functionality
  initializeAdminFeatures();
});

function initializeAdminFeatures() {
  // Add event listeners to buttons for demo purposes
  document.querySelectorAll('.btn-primary').forEach(button => {
    if (button.textContent.includes('Add New Event')) {
      button.addEventListener('click', function() {
        alert('Feature: Add New Event - This would open a modal or form in a real application');
      });
    }
    
    if (button.textContent.includes('Download')) {
      button.addEventListener('click', function() {
        alert('Feature: Download Report - This would generate and download a report in a real application');
      });
    }
    
    if (button.textContent.includes('Resolve')) {
      button.addEventListener('click', function() {
        const row = this.closest('tr');
        const statusCell = row.querySelector('td:nth-child(4)');
        statusCell.textContent = 'Resolved';
        statusCell.className = 'status-resolved';
        this.textContent = 'Resolved';
        this.className = 'btn-secondary';
        alert('Support ticket marked as resolved!');
      });
    }
  });
  
  // Add functionality to edit buttons
  document.querySelectorAll('.btn-secondary').forEach(button => {
    if (button.textContent === 'Edit') {
      button.addEventListener('click', function() {
        alert('Feature: Edit Event - This would open an edit form in a real application');
      });
    }
    
    if (button.textContent === 'Activate') {
      button.addEventListener('click', function() {
        const row = this.closest('tr');
        const statusCell = row.querySelector('td:nth-child(4)');
        statusCell.textContent = 'Active';
        statusCell.className = 'status-paid';
        this.textContent = 'Suspend';
        this.className = 'btn-danger';
        alert('User activated successfully!');
      });
    }
  });
  
  // Add functionality to delete/suspend buttons
  document.querySelectorAll('.btn-danger').forEach(button => {
    if (button.textContent === 'Delete') {
      button.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this event?')) {
          const row = this.closest('tr');
          row.style.opacity = '0.5';
          row.style.backgroundColor = '#C73E3E';
          setTimeout(() => {
            row.remove();
            alert('Event deleted successfully!');
          }, 500);
        }
      });
    }
    
    if (button.textContent === 'Suspend') {
      button.addEventListener('click', function() {
        if (confirm('Are you sure you want to suspend this user?')) {
          const row = this.closest('tr');
          const statusCell = row.querySelector('td:nth-child(4)');
          statusCell.textContent = 'Suspended';
          statusCell.className = 'status-pending';
          this.textContent = 'Activate';
          this.className = 'btn-secondary';
          alert('User suspended successfully!');
        }
      });
    }
  });
}