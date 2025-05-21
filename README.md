Berikut adalah versi bahasa Indonesia dari dokumentasi proyek **Pseudofile - Layanan Cloud Pemrosesan PDF**:

---

# Pseudofile - Layanan Cloud Pemrosesan PDF

**Pseudofile** adalah layanan cloud untuk memproses file PDF yang memungkinkan pengguna untuk mengonversi, mengompres, menggabungkan, dan menyimpan file PDF. Aplikasi ini dibangun menggunakan **Streamlit** untuk antarmuka frontend dan **Supabase** untuk otentikasi, basis data, dan penyimpanan.

## Fitur

* **Konversi PDF**: Mengonversi berbagai format dokumen (Word, gambar, teks) ke PDF
* **Kompresi PDF**: Mengurangi ukuran file PDF tanpa kehilangan kualitas secara signifikan
* **Gabung PDF**: Menggabungkan beberapa file PDF menjadi satu dokumen
* **PDF Pocket**: Menyimpan dan mengelola file PDF yang telah diproses di cloud
* **Otentikasi Pengguna**: Sistem login dan registrasi yang aman
* **Pelacakan Penggunaan**: Memantau dan membatasi penggunaan harian
* **Simulasi Penagihan**: Menghitung biaya berdasarkan penggunaan

## Struktur Proyek

```
pseudofile/
├── frontend/             # Komponen UI Streamlit
│   ├── app.py            # Aplikasi utama Streamlit
│   ├── pages/            # UI untuk halaman-halaman berbeda
│   ├── components/       # Komponen UI yang dapat digunakan kembali
│   └── styles/           # Gaya CSS
├── backend/              # Logika backend
│   ├── auth.py           # Fungsi otentikasi
│   ├── database.py       # Interaksi dengan database
│   ├── storage.py        # Operasi penyimpanan file
│   └── pdf/              # Fungsi pemrosesan PDF
├── database/             # Skema dan inisialisasi database
├── .env                  # Variabel lingkungan (tidak disimpan di repo)
├── .env.example          # Contoh variabel lingkungan
├── requirements.txt      # Dependensi proyek
└── main.py               # Titik masuk aplikasi
```

## Instruksi Instalasi

1. **Clone repositori**

```bash
git clone https://github.com/yourusername/pseudofile.git
cd pseudofile
```

2. **Atur variabel lingkungan**

Salin file contoh variabel lingkungan dan sesuaikan dengan kredensial Supabase Anda:

```bash
cp .env.example .env
# Edit file .env dengan kredensial Anda
```

3. **Install dependensi**

```bash
pip install -r requirements.txt
```

4. **Inisialisasi database**

Jalankan skrip inisialisasi database untuk membuat skema:

```bash
python database/init_db.py
```

5. **Jalankan aplikasi**

```bash
streamlit run main.py
```

## Pengaturan Supabase

1. Buat proyek baru di Supabase
2. Aktifkan otentikasi dengan email/kata sandi
3. Buat tabel database sesuai dengan SQL di `database/schema.sql`
4. Buat bucket penyimpanan bernama "files" dengan akses publik
5. Salin URL Supabase dan API key ke file `.env`

## Batasan Penggunaan

* Konversi PDF: Maksimal 3 kali per hari
* Kompresi PDF: Maksimal 3 kali per hari
* Gabung PDF: Maksimal 3 kali per hari

## Simulasi Biaya

* Konversi: Rp100 per operasi
* Kompresi: Rp100 per operasi
* Gabung: Rp200 per operasi

## Lisensi
Mitha Yang Buat 

