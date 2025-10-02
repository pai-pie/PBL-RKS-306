// static/script/user/homepage.js

class ConcertManager {
    constructor() {
        this.cities = [
            {
                name: "Bali",
                venue: "Garuda Wisnu Kencana",
                date: "Saturday, 10 November 2025",
                time: "19.30 wib",
                ticketsSold: 750
            },
            {
                name: "Jakarta", 
                venue: "Jakarta International Stadium",
                date: "Saturday, 25 November 2025", 
                time: "18.30 wita",
                ticketsSold: 550
            },
            {
                name: "Makassar",
                venue: "Trans Studio Mall", 
                date: "Saturday, 8 December 2025",
                time: "18.30 wita",
                ticketsSold: 450
            },
            {
                name: "Pekanbaru",
                venue: "Lanud Roesmin Nurjadin",
                date: "Saturday, 20 December 2025",
                time: "19.30 wib", 
                ticketsSold: 300
            }
        ];
        
        this.ticketTypes = [
            { type: "Standard", price: "Rp 450.000" },
            { type: "Premium", price: "Rp 850.000" },
            { type: "VIP", price: "Rp 1.250.000" }
        ];
    }
    
    getCities() {
        return this.cities;
    }
    
    getTicketTypes() {
        return this.ticketTypes;
    }
    
    getCityByName(cityName) {
        return this.cities.find(city => city.name === cityName);
    }
}

class UIManager {
    constructor() {
        this.currentSelectedCity = null;
        this.currentSelectedTicket = null;
    }
    
    updateModalContent(cityName) {
        const city = window.concertApp.concertManager.getCityByName(cityName);
        if (city) {
            document.getElementById('modalTitle').textContent = `Book Tickets - ${cityName}`;
            document.getElementById('modalInfo').textContent = 
                `${city.venue} | ${city.date} | ${city.time}`;
        }
    }
    
    handleTicketSelection(element, ticketType) {
        // Remove active class dari semua ticket cards
        document.querySelectorAll('.ticket-card').forEach(card => {
            card.classList.remove('active');
        });
        
        // Add active class ke yang dipilih
        element.classList.add('active');
        this.currentSelectedTicket = ticketType;
        
        // Enable select button
        const selectBtn = document.getElementById('selectBtn');
        selectBtn.classList.add('active');
        selectBtn.disabled = false;
    }
    
    handleConfirmation() {
        if (this.currentSelectedTicket && this.currentSelectedCity) {
            alert(`Booking confirmed!\nCity: ${this.currentSelectedCity}\nTicket: ${this.currentSelectedTicket}`);
            window.concertApp.bookingModal.close();
            this.resetSelection();
        }
    }
    
    resetSelection() {
        this.currentSelectedCity = null;
        this.currentSelectedTicket = null;
        document.querySelectorAll('.ticket-card').forEach(card => {
            card.classList.remove('active');
        });
        const selectBtn = document.getElementById('selectBtn');
        selectBtn.classList.remove('active');
        selectBtn.disabled = true;
    }
    
    setCurrentCity(cityName) {
        this.currentSelectedCity = cityName;
    }
}

class BookingModal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.uiManager = new UIManager();
        this.bindEvents();
    }
    
    bindEvents() {
        // Close modal ketika klik close button
        this.modal.querySelector('.close').onclick = () => {
            this.close();
        };
        
        // Close modal ketika klik di luar
        window.onclick = (event) => {
            if (event.target === this.modal) {
                this.close();
            }
        };
    }
    
    open(cityName) {
        this.uiManager.setCurrentCity(cityName);
        this.uiManager.updateModalContent(cityName);
        this.uiManager.resetSelection();
        this.modal.style.display = "block";
    }
    
    close() {
        this.modal.style.display = "none";
        this.uiManager.resetSelection();
    }
    
    select(element, ticketType) {
        this.uiManager.handleTicketSelection(element, ticketType);
    }
    
    confirm() {
        this.uiManager.handleConfirmation();
    }
}

// Initialize application
class ConcertApp {
    constructor() {
        this.concertManager = new ConcertManager();
        this.bookingModal = new BookingModal("ticketModal");
        this.init();
    }
    
    init() {
        // Expose ke global scope
        window.concertApp = this;
        window.bookingModal = this.bookingModal;
        
        console.log('ConcertApp initialized successfully!');
    }
}

// Start the application
document.addEventListener('DOMContentLoaded', function() {
    new ConcertApp();
});