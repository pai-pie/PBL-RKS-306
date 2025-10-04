from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecret"

# Simpan user sementara (sementara dict, harusnya database)
users = {}

# --- HOMEPAGE ---
@app.route("/")
@app.route("/homepage")
def homepage():
    if "username" in session:
        return render_template("user/homepage.html", username=session["username"])
    return redirect(url_for("login"))

# --- REGISTER ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Cek apakah email sudah terdaftar
        if email in users:
            return render_template("user/register.html", error="Email sudah terdaftar!")

        # Simpan user baru
        users[email] = {"username": username, "password": password}

        # Setelah register → suruh login dulu
        flash("Registrasi berhasil, silakan login!", "success")
        return redirect(url_for("login"))

    return render_template("user/register.html")

# --- LOGIN ---
# --- LOGIN ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["email"]  # ini bisa email ATAU username
        password = request.form["password"]

        # Login pakai email
        if identifier in users and users[identifier]["password"] == password:
            session["username"] = users[identifier]["username"]
            session["email"] = identifier
            return redirect(url_for("homepage"))

        # Login pakai username
        for email, data in users.items():
            if data["username"] == identifier and data["password"] == password:
                session["username"] = data["username"]
                session["email"] = email
                return redirect(url_for("homepage"))

        return render_template("user/login.html", error="Email/Username atau password salah!")

    return render_template("user/login.html")

# --- LOGOUT ---
@app.route("/logout")
def logout():
    session.clear()
    flash("Anda sudah logout.", "info")
    return redirect(url_for("login"))

# --- CONTOH HALAMAN LAIN ---
@app.route("/concert")
def concert():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("user/concert.html")

@app.route("/account")
def account():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template(
        "user/account.html",
        username=session["username"],
        email=session["email"]
    )

@app.route("/payment")
def payment():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("user/payment.html")

@app.route("/success")
def success():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("user/success.html")

if __name__ == "__main__":
    app.run(debug=True)
