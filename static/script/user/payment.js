class Payment {
  constructor(ticketType) {
    this.ticketType = ticketType;
    this.prices = { 
      "Standard": "Rp 450.000", 
      "Premium": "Rp 850.000", 
      "VIP": "Rp 1.250.000" 
    };
    this.method = null;
    
    // Display ticket info with magical styling
    document.getElementById("ticketType").innerText = `${this.ticketType} Ticket`;
    document.getElementById("ticketPrice").innerText = `Price: ${this.prices[this.ticketType]}`;
  }

  chooseMethod(method) {
    this.method = method;
    const details = document.getElementById("paymentDetails");
    
    if(!method) { 
      details.style.display = "none"; 
      return; 
    }

    details.style.display = "block";
    
    if(method === "E-Wallet"){
      details.innerHTML = `
        <h3>✨ E-Wallet Payment</h3>
        <p>Scan this magical QR code:</p>
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=GuardianTix-Magical-Payment-${this.ticketType}" alt="QR Code">
        <p style="margin-top: 10px; color: #FFD700;">Complete payment via your preferred E-Wallet</p>
      `;
    } else if(method === "Bank Transfer"){
      details.innerHTML = `
        <h3>🏦 Bank Transfer</h3>
        <p>Transfer to our magical vault:</p>
        <div class="bank-info">
          <p><strong>Bank:</strong> Magical Bank of Indonesia</p>
          <p><strong>Account:</strong> 1234 5678 9012</p>
          <p><strong>Name:</strong> GuardianTix Enchantment</p>
          <p><strong>Amount:</strong> ${this.prices[this.ticketType]}</p>
        </div>
        <p style="margin-top: 10px; color: #C8A2C8;">Please include your email as reference</p>
      `;
    }
  }

  confirm() {
<<<<<<< HEAD
    alert("✅ Payment completed successfully! Your ticket has been reserved.");
    window.location.href = "/"; // balik ke homepage setelah bayar
  }
}

const payment = new Payment();
=======
    if(!this.method){ 
      alert("Please choose a magical payment method!"); 
      return; 
    }
    
    // Add magical confirmation effect
    const button = document.querySelector('button');
    const originalText = button.textContent;
    button.textContent = 'Casting Payment Spell...';
    button.disabled = true;
    
    // Simulate magical processing
    setTimeout(() => {
      window.location.href = `success.html?ticket=${this.ticketType}&method=${this.method}`;
    }, 1500);
  }
}

// Get ticket type from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const ticketType = urlParams.get("ticket") || "Standard";
const payment = new Payment(ticketType);
>>>>>>> ec8f950d47651a3238c41233eab0d535003be91b
