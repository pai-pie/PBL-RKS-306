// Concert Data - HANYA 1 ARTIS
const concerts = [
  {
    id: 1,
    title: "The Mystic Symphony World Tour",
    artist: "Ethereal Orchestra",
    genre: "classical",
    city: "jakarta",
    date: "December 15, 2024",
    venue: "Jakarta Convention Center",
    time: "7:00 PM",
    price: "Rp 450.000",
    image: "The Mystic Symphony",
    description: "Experience the magical symphony that enchants millions"
  },
  {
    id: 2,
    title: "The Mystic Symphony World Tour", 
    artist: "Ethereal Orchestra",
    genre: "classical",
    city: "bandung",
    date: "December 18, 2024",
    venue: "Bandung Convention Hall",
    time: "7:00 PM",
    price: "Rp 450.000",
    image: "The Mystic Symphony",
    description: "An unforgettable night of classical music mastery"
  },
  {
    id: 3,
    title: "The Mystic Symphony World Tour",
    artist: "Ethereal Orchestra",
    genre: "classical",
    city: "surabaya",
    date: "December 22, 2024",
    venue: "Surabaya Grand Hall", 
    time: "7:00 PM",
    price: "Rp 450.000",
    image: "The Mystic Symphony",
    description: "The musical phenomenon live in Surabaya"
  },
  {
    id: 4,
    title: "The Mystic Symphony World Tour",
    artist: "Ethereal Orchestra",
    genre: "classical", 
    city: "bali",
    date: "January 12, 2025",
    venue: "Bali Beach Arena",
    time: "7:00 PM",
    price: "Rp 450.000",
    image: "The Mystic Symphony",
    description: "Open air concert under the stars"
  }
];

// Render Concerts
function renderConcerts(filteredConcerts = concerts) {
  const container = document.getElementById('concertsContainer');
  container.innerHTML = '';

  if (filteredConcerts.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #C8A2C8;">
        <h3>No concerts found for selected filters</h3>
        <p>Try adjusting your search criteria</p>
      </div>
    `;
    return;
  }

  filteredConcerts.forEach(concert => {
    const concertCard = `
      <div class="concert-card">
        <div class="concert-image">${concert.image}</div>
        <div class="concert-info">
          <h3 class="concert-title">${concert.city.charAt(0).toUpperCase() + concert.city.slice(1)} Concert</h3>
          <p class="concert-artist">by ${concert.artist}</p>
          <div class="concert-details">
            <div><i>📅</i> ${concert.date}</div>
            <div><i>📍</i> ${concert.venue}</div>
            <div><i>⏰</i> ${concert.time}</div>
            <div><i>🎵</i> ${concert.genre.charAt(0).toUpperCase() + concert.genre.slice(1)}</div>
          </div>
          <p style="color: #C8A2C8; font-style: italic; margin: 10px 0;">${concert.description}</p>
          <div class="concert-price">From ${concert.price}</div>
          <button class="btn btn-primary" onclick="bookingModal.openConcert(${concert.id})">Book Tickets</button>
        </div>
      </div>
    `;
    container.innerHTML += concertCard;
  });
}

// Filter Concerts
function filterConcerts() {
  const city = document.getElementById('cityFilter').value;
  const month = document.getElementById('monthFilter').value;

  const filtered = concerts.filter(concert => {
    const cityMatch = city === 'all' || concert.city === city;
    const monthMatch = month === 'all' || 
                      (month === 'december' && concert.date.includes('December')) ||
                      (month === 'january' && concert.date.includes('January'));
    
    return cityMatch && monthMatch;
  });

  renderConcerts(filtered);
}

// Booking Modal System
class BookingModal {
  constructor(modalId, selectBtnId) {
    this.modal = document.getElementById(modalId);
    this.selectBtn = document.getElementById(selectBtnId);
    this.selectedTicket = null;
    this.selectedConcert = null;

    window.addEventListener("click", (event) => {
      if (event.target === this.modal) this.close();
    });
  }

  openConcert(concertId) {
    if (!auth.isLoggedIn()) {
      alert('Please login first to book tickets!');
      window.location.href = './login.html';
      return;
    }

    const concert = concerts.find(c => c.id === concertId);
    this.selectedConcert = concert;

    const title = document.getElementById("modalTitle");
    const info = document.getElementById("modalInfo");

    title.innerText = `Book Tickets - ${concert.city.charAt(0).toUpperCase() + concert.city.slice(1)}`;
    info.innerText = `${concert.date} | ${concert.venue} | ${concert.time}`;
    this.modal.style.display = "block";

    this.selectedTicket = null;
    document.querySelectorAll('.ticket-card').forEach(card => card.classList.remove('active'));
    this.selectBtn.classList.remove("active");
    this.selectBtn.disabled = true;
  }

  close() { 
    this.modal.style.display = "none"; 
    this.selectedConcert = null;
  }

  select(element, type){
    document.querySelectorAll('.ticket-card').forEach(card => card.classList.remove('active'));
    element.classList.add('active');
    this.selectedTicket = type;
    this.selectBtn.classList.add("active");
    this.selectBtn.disabled = false;
  }

  confirm(){
    if(this.selectedTicket && this.selectedConcert){
      const ticketData = {
        concert: this.selectedConcert.title,
        artist: this.selectedConcert.artist,
        city: this.selectedConcert.city,
        date: this.selectedConcert.date,
        venue: this.selectedConcert.venue,
        type: this.selectedTicket,
        price: this.getPrice(this.selectedTicket)
      };
      window.location.href = `./payment.html?data=${encodeURIComponent(JSON.stringify(ticketData))}`;
    } else {
      alert('Please select a ticket type first.');
    }
  }

  getPrice(type){
    const prices = { "Standard":"Rp 450.000", "Premium":"Rp 850.000", "VIP":"Rp 1.250.000" };
    return prices[type];
  }
}

const bookingModal = new BookingModal("ticketModal","selectBtn");

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
  if (!auth.isLoggedIn()) {
    window.location.href = './login.html';
    return;
  }
  
  updateNavbar();
  renderConcerts();
  
  // Add event listeners to filters
  document.getElementById('cityFilter').addEventListener('change', filterConcerts);
  document.getElementById('monthFilter').addEventListener('change', filterConcerts);

  setTimeout(() => {
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.5s ease';
  }, 100);
});