from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Student
from algorithms import bubble_sort_ipk, selection_sort_nim, linear_search_nama, binary_search_nim
import json, os

# 🚀 Tambahan import library bawaan Python untuk fitur email
import random
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app) 

FILE_PATH = 'data.json'

def load_data():
    try:
        if not os.path.exists(FILE_PATH):
            return []
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error membaca file: {e}")
        return []

def save_data(data):
    try:
        with open(FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4) 
    except Exception as e:
        print(f"Error menyimpan file: {e}")

# API Endpoint untuk Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username_input = data.get('username')
    password_input = data.get('password')
    
    # DAFTAR AKUN SAKTI (Sejajar dengan variabel di atas)
    if (username_input == 'admin' and password_input == 'admin123') or \
       (username_input == 'najwanpratomo07@gmail.com' and password_input == 'najwanp078'):
        return jsonify({"status": "success", "message": "Login berhasil"})
        
    return jsonify({"status": "error", "message": "Username atau password salah!"}), 401

# 🚀 API Endpoint: Lupa Password (Kirim OTP via Email)
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email_tujuan = data.get('email')

    if not email_tujuan:
        return jsonify({"status": "error", "message": "Email tidak boleh kosong"}), 400

    # 1. Generate 6 Digit OTP Acak
    otp_code = str(random.randint(100000, 999999))

    # 2. Siapkan Pesan Email
    msg = EmailMessage()
    msg['Subject'] = "Kode OTP Reset Password - TechNova University"
    
    # ✅ PERBAIKAN: Gunakan email asli kamu sebagai pengirim
    msg['From'] = "najwanpratomo07@gmail.com" 
    msg['To'] = email_tujuan
    
    pesan = f"""
    Halo Mahasiswa/Admin TechNova,
    
    Sistem kami menerima permintaan untuk mereset password akun Anda.
    Berikut adalah kode OTP Anda:
    
    {otp_code}
    
    Kode ini bersifat rahasia. Jangan berikan kode ini kepada siapapun, termasuk pihak kampus.
    Jika Anda tidak merasa meminta reset password, abaikan email ini.
    
    Salam,
    Sistem Keamanan TechNova University
    """
    msg.set_content(pesan)

    # 3. Kirim Email pakai smtplib
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # ✅ PERBAIKAN: Spasi di App Password sudah dihilangkan agar tidak error
            smtp.login("najwanpratomo07@gmail.com", "vbpahgycgzhlnwzw")
            smtp.send_message(msg)
            
        return jsonify({
            "status": "success", 
            "message": "OTP berhasil dikirim ke email",
            "dev_otp": otp_code 
        }), 200
        
    except Exception as e:
        print("Error ngirim email:", e)
        return jsonify({"status": "error", "message": "Gagal mengirim email, cek koneksi atau App Password"}), 500

# 🚀 API Endpoint BARU: Contact Us (Kirim Pesan + Lampiran File)
@app.route('/api/contact', methods=['POST'])
def contact_us():
    try:
        # Menangkap input form (menggunakan request.form karena dari FormData React)
        name = request.form.get('from_name')
        email_user = request.form.get('reply_to')
        message = request.form.get('message')
        
        # Menangkap lampiran file
        file = request.files.get('my_file')

        msg = EmailMessage()
        msg['Subject'] = f"Tiket Laporan TechNova dari: {name}"
        msg['From'] = "najwanpratomo07@gmail.com" 
        # Pesan Contact Us dikirim ke email Admin (email kamu sendiri)
        msg['To'] = "najwanpratomo07@gmail.com"   

        pesan_lengkap = f"""
        Ada laporan kendala baru dari sistem TechNova:
        
        Nama Pengirim: {name}
        Email Pengirim: {email_user}
        
        Pesan:
        {message}
        """
        msg.set_content(pesan_lengkap)

        # Cek dan tambahkan lampiran file jika ada
        if file and file.filename:
            file_data = file.read()
            file_name = file.filename
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Kirim email menggunakan smtplib
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("najwanpratomo07@gmail.com", "vbpahgycgzhlnwzw")
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": "Pesan terkirim"}), 200

    except Exception as e:
        print("Error Contact Us:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# API Endpoint untuk Mengambil dan Mencari/Mengurutkan Data
@app.route('/api/mahasiswa', methods=['GET'])
def get_mahasiswa():
    data = load_data()
    langkah = 0 
    
    query = request.args.get('q')
    jenis_search = request.args.get('search_type')
    sort_by = request.args.get('sort')

    # Fitur Search
    if query:
        if jenis_search == 'nim':
            data, langkah = binary_search_nim(data, query)
        elif jenis_search == 'jurusan':
            from algorithms import sequential_search_jurusan 
            data, langkah = sequential_search_jurusan(data, query)
        else:
            data, langkah = linear_search_nama(data, query)
            
    # Fitur Sort
    if sort_by == 'ipk':
        data, langkah = bubble_sort_ipk(data)
    elif sort_by == 'nim':
        data, langkah = selection_sort_nim(data)
    elif sort_by == 'semester': 
        from algorithms import merge_sort_semester
        hasil = merge_sort_semester(data)
        if isinstance(hasil, tuple):
            data, langkah = hasil
        else:
            data = hasil

    return jsonify({
        "data": data,
        "langkah": langkah
    })

# API Endpoint untuk Tambah Data
@app.route('/api/mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    try:
        data_baru = request.json
        nim = data_baru.get('nim')
        nama = data_baru.get('nama')
        
        # Validasi Regex berjalan di sini
        Student.validasi_input(nim, nama)
        
        mhs = Student(
            nim, nama, data_baru.get('jurusan'), 
            data_baru.get('semester'), data_baru.get('status'), data_baru.get('ipk')
        )
        
        data = load_data()
        data.append(mhs.to_dict())
        save_data(data)
        
        return jsonify({"status": "success", "message": "Data berhasil ditambahkan!"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# API Endpoint untuk Hapus Data
@app.route('/api/mahasiswa/<nim>', methods=['DELETE'])
def hapus_mahasiswa(nim):
    data = load_data()
    data = [m for m in data if m['nim'] != nim]
    save_data(data)
    return jsonify({"status": "success", "message": "Data berhasil dihapus!"})

if __name__ == '__main__':
    if not os.path.exists(FILE_PATH):
        save_data([])
    # Jalankan API di port 5000
    app.run(debug=True, port=5000)