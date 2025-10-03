import os
import psycopg2
import psycopg2.extras # Berguna untuk mengambil data seperti dictionary
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# --- SETUP APLIKASI DAN DATABASE ---
app = Flask(__name__)
load_dotenv() # Memuat variabel dari file .env

# Ganti dengan kunci rahasia yang lebih kompleks dan unik
app.secret_key = os.getenv('SECRET_KEY', 'default_super_secret_key')

def get_db_connection():
    """Fungsi helper untuk membuat koneksi ke database."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

# --- DECORATOR UNTUK MEMASTIKAN USER SUDAH LOGIN ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Silakan login untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# --- HOMEPAGE ---
@app.route("/")
@app.route("/homepage")
@login_required # Menggunakan decorator, jadi tidak perlu cek session manual
def homepage():
    return render_template("user/homepage.html")

# --- REGISTER ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = None # Inisialisasi koneksi
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Cek apakah email sudah terdaftar di DATABASE
            cur.execute('SELECT id FROM users WHERE email = %s;', (email,))
            user_exists = cur.fetchone()

            if user_exists:
                flash('Email sudah terdaftar! Silakan gunakan email lain atau login.')
                return redirect(url_for('register'))

            # HASH password sebelum disimpan! Ini SANGAT PENTING.
            hashed_password = generate_password_hash(password)

            # Simpan user baru ke DATABASE
            cur.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',
                        (username, email, hashed_password))
            
            # Konfirmasi perubahan agar data tersimpan permanen.
            conn.commit()
            
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for("login"))

        except (Exception, psycopg2.DatabaseError) as error:
            flash('Terjadi kesalahan pada database.', 'danger')
            print(error) # Tampilkan error di terminal untuk debugging
            return redirect(url_for('register'))
        finally:
            if conn is not None:
                conn.close()

    return render_template("user/register.html")


# --- LOGIN ---
@app.route("/login", methods=["GET", "POST"])
def login():
    # Jika user sudah login, arahkan ke homepage
    if 'loggedin' in session:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        # Menggunakan DictCursor agar bisa memanggil kolom dengan nama, contoh: user['password_hash']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Cari user berdasarkan email di DATABASE
        cur.execute('SELECT * FROM users WHERE email = %s;', (email,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()

        # Jika user tidak ada ATAU password salah (membandingkan hash)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Email atau password salah. Silakan coba lagi.', 'danger')
            return redirect(url_for('login'))
        
        # Jika berhasil, simpan info di session
        session['loggedin'] = True
        session['id'] = user['id']
        session['username'] = user['username']

        return redirect(url_for('homepage'))

    return render_template('user/login.html')

# --- LOGOUT ---
@app.route("/logout")
def logout():
    # Hapus semua data session
    session.clear()
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('login'))


# --- RUTE-RUTE LAIN YANG DIPROTEKSI ---

@app.route("/account")
@login_required # Menggunakan decorator
def account():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Ambil data user dari database berdasarkan ID yang tersimpan di session
    cur.execute('SELECT * FROM users WHERE id = %s;', (session['id'],))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template("user/account.html", user=user_data)


@app.route("/concert")
@login_required # Menggunakan decorator
def concert():
    return render_template("user/concert.html")


@app.route("/payment")
@login_required # Menggunakan decorator
def payment():
    return render_template("user/payment.html")


@app.route("/success")
@login_required # Menggunakan decorator
def success():
    return render_template("user/success.html")

# --- MENJALANKAN APLIKASI ---
if __name__ == "__main__":
    app.run(debug=True)