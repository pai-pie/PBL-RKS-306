import os
import psycopg2
import psycopg2.extras # Berguna untuk mengambil data seperti dictionary
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# --- SETUP APLIKASI ---
app = Flask(__name__)
load_dotenv() # Memuat variabel dari file .env

# Mengambil SECRET_KEY dari .env, jika tidak ada, gunakan default (kurang aman)
app.secret_key = os.getenv('SECRET_KEY', 'ganti_dengan_kunci_rahasia_yang_unik')

# --- KONEKSI DATABASE ---
def get_db_connection():
    """Fungsi helper untuk membuat koneksi ke database."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'), # Gunakan user aplikasi, bukan admin DBeaver
        password=os.getenv('DB_PASSWORD')
    )
    return conn

# --- DECORATORS (PENJAGA RUTE) ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Silakan login untuk mengakses halaman ini.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Hanya admin yang dapat mengakses halaman ini.', 'danger')
            return redirect(url_for('homepage'))
        return f(*args, **kwargs)
    return decorated_function

# --- RUTE UTAMA & AUTENTIKASI ---

@app.route("/")
def index():
    # Arahkan ke homepage jika sudah login, jika belum ke login
    if 'loggedin' in session:
        return redirect(url_for('homepage'))
    return redirect(url_for('login'))

@app.route("/homepage")
@login_required
def homepage():
    # Jika admin, langsung arahkan ke panel admin
    if session.get('role') == 'admin':
        return redirect(url_for('admin_panel'))
    # Jika user biasa, tampilkan homepage user
    return render_template("user/homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Cek apakah email atau username sudah terdaftar
            cur.execute('SELECT id FROM users WHERE email = %s OR username = %s;', (email, username))
            user_exists = cur.fetchone()

            if user_exists:
                flash('Email atau username sudah terdaftar!', 'danger')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)

            # Simpan user baru, role default adalah 'user'
            cur.execute('INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)',
                        (username, email, hashed_password, 'user'))
            
            conn.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for("login"))

        except (Exception, psycopg2.DatabaseError) as error:
            flash('Terjadi kesalahan saat registrasi.', 'danger')
            print(f"REGISTER ERROR: {error}")
            return redirect(url_for('register'))
        finally:
            if conn:
                conn.close()

    return render_template("user/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["email"].strip() # Bisa email atau username
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Cari user berdasarkan email ATAU username
        cur.execute('SELECT * FROM users WHERE email = %s OR username = %s;', (identifier.lower(), identifier))
        user = cur.fetchone()
        
        cur.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            # Login berhasil, simpan data ke session
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            flash(f"Selamat datang, {user['username']}!", 'success')
            return redirect(url_for('homepage'))
        else:
            # Login gagal
            flash("Email/Username atau password salah!", "danger")
            return redirect(url_for('login'))

    return render_template("user/login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Anda berhasil logout.", "info")
    return redirect(url_for("login"))

# --- RUTE ADMIN ---

@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    return render_template("adminpanel.html")


# --- RUTE USER ---

@app.route("/concert")
@login_required
def concert():
    return render_template("user/concert.html")

@app.route("/account")
@login_required
def account():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s;', (session['id'],))
    user_data = cur.fetchone()
    cur.close()
    conn.close()    
    return render_template("user/account.html", user=user_data)

@app.route("/payment")
@login_required
def payment():
    return render_template("user/payment.html")

@app.route("/success")
@login_required
def success():
    return render_template("user/success.html")

# --- MENJALANKAN APLIKASI ---
if __name__ == "__main__":
    app.run(debug=True)

