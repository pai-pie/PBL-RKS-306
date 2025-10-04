// static/script/user/homepage.js

class BookingModal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = this.modal.querySelector(".close"); // tombol X di modal
        this.selectedType = null;
        this.selectedPrice = null;

        // Tutup modal kalau klik tombol close
        this.closeBtn.onclick = () => {
            this.close();
        };

        // Tutup modal kalau klik di luar modal
        window.onclick = (event) => {
            if (event.target === this.modal) {
                this.close();
            }
        };
    }

    open(city) {
        // Set nama kota di modal (kalau ada elemen #modalCity)
        const citySpan = this.modal.querySelector("#modalCity");
        if (citySpan) {
            citySpan.textContent = city;
        }

        this.modal.style.display = "block";
    }

    close() {
        this.modal.style.display = "none";
    }

    // Pilih jenis tiket
    select(element, type) {
        const allCards = this.modal.querySelectorAll(".ticket-card");
        allCards.forEach(card => card.classList.remove("selected"));
        element.classList.add("selected");

        this.selectedType = type;
        this.selectedPrice = element.querySelector("p").innerText; // ambil harga dari <p>
    }

    // Konfirmasi pilihan tiket
    confirm() {
        if (!this.selectedType || !this.selectedPrice) {
            alert("Please select a ticket first!");
            return;
        }

        // Redirect ke halaman payment dengan data di URL
        const url = `/payment?type=${encodeURIComponent(this.selectedType)}&price=${encodeURIComponent(this.selectedPrice)}`;
        window.location.href = url;
    }
}

// buat object global biar bisa dipakai di onclick html
window.bookingModal = new BookingModal("ticketModal");
