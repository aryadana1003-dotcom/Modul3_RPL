# Aryadana Agung Karama F5212510013
# Sistem Manajemen Perpustakaan

## 📖 Deskripsi Singkat Aplikasi
Aplikasi Perpustakaan adalah perangkat lunak berbasis desktop yang dikembangkan menggunakan bahasa pemrograman Python. Aplikasi ini mengimplementasikan pola arsitektur Model-View-Controller (MVC) untuk memisahkan antarmuka pengguna, logika bisnis, dan pengelolaan data. Aplikasi ini dilengkapi dengan antarmuka grafis (GUI) modern menggunakan `customtkinter`, sistem keamanan *hash* SHA-256 untuk kata sandi, serta Otorisasi Berbasis Peran (Admin & Anggota).

## 📂 Struktur Direktori MVC
Proyek ini diorganisasikan dengan struktur modular sebagai berikut:
```text
📦 Perpustakaan
 ┣ 📂 config/          # Pengaturan koneksi ke basis data MySQL
 ┣ 📂 controllers/     # Logika aplikasi dan jembatan antara View & Model
 ┣ 📂 models/          # Eksekusi kueri SQL dan pengolahan data
 ┣ 📂 views/           # Tampilan antarmuka pengguna (GUI)
 ┣ 📂 tests/           # Kumpulan skrip pengujian otomatis (pytest)
 ┣ 📜 main.py          # Titik masuk utama (Entry point) aplikasi
 ┣ 📜 requirements.txt # Daftar dependensi pustaka Python
 ┗ 📜 README.md        # Dokumentasi teknis aplikasi