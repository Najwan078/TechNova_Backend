from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Student
from algorithms import bubble_sort_ipk, selection_sort_nim, linear_search_nama, binary_search_nim
import random
import smtplib
from email.message import EmailMessage
import requests 

app = Flask(__name__)
CORS(app) 

# ==========================================
# KONFIGURASI JSONBIN.IO (DATABASE CLOUD)
# ==========================================
JSONBIN_BIN_ID = "6a19ba9dddf5aa59f7751c3e"
JSONBIN_API_KEY = "$2a$10$gH6D9CpO4v4sPXZBA1mWOeRdiE6xBooFdeFBbvObvM7u8ZLAsfIx6"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"

def load_data():
    try:
        headers = {
            'X-Master-Key': JSONBIN_API_KEY
        }
        # Mengambil data langsung dari internet (JSONBin)
        response = requests.get(JSONBIN_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get('record', [])
        return []
    except Exception as e:
        print(f"Error membaca dari JSONBin: {e}")
        return []

def save_data(data):
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': JSONBIN_API_KEY
        }
        # Menyimpan data langsung ke internet (JSONBin)
        requests.put(JSONBIN_URL, json=data, headers=headers)
    except Exception as e:
        print(f"Error menyimpan ke JSONBin: {e}")

# ==========================================
# API ENDPOINTS
# ==========================================

# API Endpoint untuk Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username_input = data.get('username')
    password_input = data.get('password')

    if (username_input == 'admin' and password_input == 'admin123') or \
       (username_input == 'najwanpratomo07@gmail.com' and password_input == 'najwanp078'):
        return jsonify({"status": "success", "message": "Login berhasil"})
        
    return jsonify({"status": "error", "message": "Username atau password salah!"}), 401

# API Endpoint: Lupa Password (Kirim OTP via Email)
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email_tujuan = data.get('email')

    if not email_tujuan:
        return jsonify({"status": "error", "message": "Email tidak boleh kosong"}), 400

    otp_code = str(random.randint(100000, 999999))

    msg = EmailMessage()
    msg['Subject'] = "Kode OTP Reset Password - TechNova University"
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

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
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

# API Endpoint BARU: Contact Us (Kirim Pesan + Lampiran File)
@app.route('/api/contact', methods=['POST'])
def contact_us():
    try:
        name = request.form.get('from_name')
        email_user = request.form.get('reply_to')
        message = request.form.get('message')
        file = request.files.get('my_file')

        msg = EmailMessage()
        msg['Subject'] = f"Tiket Laporan TechNova dari: {name}"
        msg['From'] = "najwanpratomo07@gmail.com" 
        msg['To'] = "najwanpratomo07@gmail.com"   

        pesan_lengkap = f"""
        Ada laporan kendala baru dari sistem TechNova:
        
        Nama Pengirim: {name}
        Email Pengirim: {email_user}
        
        Pesan:
        {message}
        """
        msg.set_content(pesan_lengkap)

        if file and file.filename:
            file_data = file.read()
            file_name = file.filename
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

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

    if query:
        if jenis_search == 'nim':
            data, langkah = binary_search_nim(data, query)
        elif jenis_search == 'jurusan':
            from algorithms import sequential_search_jurusan 
            data, langkah = sequential_search_jurusan(data, query)
        else:
            data, langkah = linear_search_nama(data, query)
            
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
        
        Student.validasi_input(nim, nama)
        
        mhs = Student(
            nim, nama, data_baru.get('jurusan'), 
            data_baru.get('semester'), data_baru.get('status'), data_baru.get('ipk')
        )
        
        data = load_data()
        data.append(mhs.to_dict())
        save_data(data) # Sekarang otomatis tersimpan ke JSONBin!
        
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

# API Endpoint untuk Edit Data
@app.route('/api/mahasiswa/<nim>', methods=['PUT'])
def edit_mahasiswa(nim):
    try:
        data_baru = request.json
        data = load_data()
        for i, m in enumerate(data):
            if m['nim'] == nim:
                data[i].update({
                    'nama': data_baru.get('nama', m['nama']),
                    'jurusan': data_baru.get('jurusan', m['jurusan']),
                    'semester': data_baru.get('semester', m['semester']),
                    'status': data_baru.get('status', m['status']),
                    'ipk': data_baru.get('ipk', m['ipk'])
                })
                save_data(data)
                return jsonify({"status": "success", "message": "Data berhasil diupdate!"})
        return jsonify({"status": "error", "message": "Mahasiswa tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# API Endpoint untuk Export JSON
@app.route('/api/mahasiswa/export', methods=['GET'])
def export_mahasiswa():
    data = load_data()
    return jsonify(data)

# API Endpoint untuk Import JSON
@app.route('/api/mahasiswa/import', methods=['POST'])
def import_mahasiswa():
    try:
        data_import = request.json
        if not isinstance(data_import, list):
            return jsonify({"status": "error", "message": "Format harus berupa array JSON"}), 400
        save_data(data_import)
        return jsonify({"status": "success", "message": f"{len(data_import)} data berhasil diimport!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)