class Ticket {
  constructor(ticketType, method){
    this.ticketType = ticketType;
    this.method = method;
    this.bookingCode = this.generateCode();
    this.showDetails();
    this.createConfetti();
  }

  generateCode(){
    const now = new Date();
    const datePart = now.getFullYear().toString().slice(-2) +
                     (now.getMonth()+1).toString().padStart(2,"0") +
                     now.getDate().toString().padStart(2,"0");
    const randomPart = Math.random().toString(36).substring(2,6).toUpperCase();
    return `MAGIC-${datePart}-${randomPart}`;
  }

  showDetails(){
    document.getElementById("ticketDetails").innerHTML = 
      `Ticket Type: <b>${this.ticketType}</b>`;
    document.getElementById("bookingCode").innerText = `Enchantment Code: ${this.bookingCode}`;
  }

  createConfetti() {
    const confettiContainer = document.getElementById('confetti');
    const colors = ['#FFD700', '#C73E3E', '#C8A2C8', '#FDF6E3'];
    
    for (let i = 0; i < 50; i++) {
      const sparkle = document.createElement('div');
      sparkle.className = 'sparkle';
      sparkle.style.left = Math.random() * 100 + 'vw';
      sparkle.style.top = Math.random() * 100 + 'vh';
      sparkle.style.background = colors[Math.floor(Math.random() * colors.length)];
      sparkle.style.animationDelay = Math.random() * 2 + 's';
      sparkle.style.animationDuration = (1 + Math.random() * 2) + 's';
      confettiContainer.appendChild(sparkle);
    }
  }

  download(){
    const content = `✨ GuardianTix Magical E-Ticket ✨
════════════════════════════════
Enchantment Code: ${this.bookingCode}
Ticket Type    : ${this.ticketType}
Payment Method : ${this.method}
Purchase Date  : ${new Date().toLocaleDateString()}

🎭 The Mystic Symphony World Tour
   by Ethereal Orchestra

📜 IMPORTANT MAGICAL NOTES:
• Present this scroll at the enchanted entrance
• Keep your wand ready for verification
• Arrive 30 minutes before the magical performance
• No dark arts allowed in the venue

May your musical journey be truly magical! ✨

"Where notes dance and spells enchant"`;
    
    const blob = new Blob([content], {type: "text/plain"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; 
    a.download = `Magical-Ticket-${this.bookingCode}.txt`; 
    
    // Add magical download effect
    const button = document.querySelector('button');
    const originalText = button.textContent;
    button.textContent = '📜 Casting Download Spell...';
    button.disabled = true;
    
    setTimeout(() => {
      a.click();
      URL.revokeObjectURL(url);
      button.textContent = originalText;
      button.disabled = false;
      
      // Show success message
      const celebration = document.querySelector('.celebration');
      celebration.textContent = '✨ E-Ticket scroll successfully downloaded!';
      celebration.style.color = '#FFD700';
    }, 1000);
  }

  goHome(){ 
    // Add magical transition effect
    document.body.style.opacity = '0.7';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
      window.location.href = "homepage";
    }, 500);
  }
}

// Initialize ticket from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const ticketType = urlParams.get("ticket") || "Standard";
const method = urlParams.get("method") || "Unknown";
const ticket = new Ticket(ticketType, method);