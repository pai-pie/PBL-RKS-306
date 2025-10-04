// static/script/user/homepage.js

class BookingModal {
    constructor(modalId, closeBtnId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = document.getElementById(closeBtnId);

        // Tutup modal kalau klik tombol close
        this.closeBtn.onclick = () => {
            this.close();
        };

<<<<<<< HEAD
        // Tutup modal kalau klik di luar modal
=======
        // Tutup modal kalau klik di luar modal-content
        window.onclick = (event) => {// static/script/user/homepage.js

class BookingModal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = this.modal.querySelector(".close"); // cari tombol close di dalam modal

        // Tutup modal kalau klik tombol close
        this.closeBtn.onclick = () => {
            this.close();
        };

        // Tutup modal kalau klik di luar modal-content
>>>>>>> ec8f950d47651a3238c41233eab0d535003be91b
        window.onclick = (event) => {
            if (event.target === this.modal) {
                this.close();
            }
        };
    }

    open(city) {
<<<<<<< HEAD
        // Set nama kota di modal (kalau ada elemen #modalCity)
=======
        // Boleh tampilkan nama kota biar lebih dinamis
>>>>>>> ec8f950d47651a3238c41233eab0d535003be91b
        const citySpan = this.modal.querySelector("#modalCity");
        if (citySpan) {
            citySpan.textContent = city;
        }

        this.modal.style.display = "block";
    }

    close() {
        this.modal.style.display = "none";
    }
<<<<<<< HEAD

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
=======
}

// buat object global biar bisa dipanggil di onclick html
window.bookingModal = new BookingModal("ticketModal");

            if (event.target === this.modal) {
                this.close();
            }
        };
    }

    open(city) {
        // Boleh tampilkan nama kota biar lebih dinamis
        const citySpan = this.modal.querySelector("#modalCity");
        if (citySpan) {
            citySpan.textContent = city;
        }

        this.modal.style.display = "block";
    }

    close() {
        this.modal.style.display = "none";
    }
}

// buat object global biar bisa dipanggil di onclick html
window.bookingModal = new BookingModal("ticketModal", "selectBtn");
>>>>>>> ec8f950d47651a3238c41233eab0d535003be91b
