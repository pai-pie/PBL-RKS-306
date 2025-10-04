class Payment {
  chooseMethod(method) {
    const details = document.getElementById("paymentDetails");
    details.innerHTML = "";

    if (method === "QR") {
      details.innerHTML = `
        <h3>📲 Pay with QRIS</h3>
        <p>Scan the QR code below with your e-wallet app:</p>
        <img src="/static/img/qris.png" alt="QRIS Payment" style="width:200px; margin-top:10px;">
      `;
    } else if (method === "VA") {
      details.innerHTML = `
        <h3>🏦 Pay with Virtual Account</h3>
        <p>Transfer to this VA number:</p>
        <div class="va-box">1234 5678 9012 3456</div>
        <small>Use your bank app or ATM to complete payment</small>
      `;
    }
  }

  confirm() {
    alert("✅ Payment completed successfully! Your ticket has been reserved.");
    window.location.href = "/"; // balik ke homepage setelah bayar
  }
}

const payment = new Payment();
