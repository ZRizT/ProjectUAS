🎓 Sistem Manajemen Data Mahasiswa (SMDM)

Proyek Tugas Akhir (UAS) - Algoritma dan Pemrograman Dikembangkan untuk mendemonstrasikan penerapan struktur data, algoritma pengurutan/pencarian, pemrograman berorientasi objek (OOP), dan integrasi API sederhana.

👨‍💻 Identitas Pengembang

Nama: Rizki Ramadani

Mata Kuliah: Algoritma dan Pemrograman

🚀 Fitur Utama

Aplikasi ini dibangun berbasis GUI (Graphical User Interface) Web menggunakan framework Streamlit dengan fitur lengkap sebagai berikut:

1. Manajemen Data (CRUD) & File I/O

Create: Input data mahasiswa baru dengan validasi ketat.

Read: Menampilkan data dalam bentuk tabel interaktif.

Update: Edit data mahasiswa (IPK/Jurusan).

Delete: Menghapus data mahasiswa dari database.

Persistensi Data: Data disimpan secara permanen menggunakan format JSON, sehingga tidak hilang saat aplikasi ditutup.

2. Implementasi Algoritma

Pencarian (Searching):

🔍 Linear Search: Mencari mahasiswa berdasarkan Nama (Partial match).

⚡ Binary Search: Mencari mahasiswa berdasarkan NIM (Data otomatis diurutkan terlebih dahulu, kompleksitas $O(\log n)$).

Pengurutan (Sorting):

🔃 Bubble Sort: Metode pengurutan sederhana untuk demonstrasi langkah per langkah.

🚀 Merge Sort: Metode pengurutan Divide & Conquer untuk efisiensi tinggi ($O(n \log n)$).

3. Validasi & Keamanan (Regex & OOP)

Validasi Input (Regex):

Email: Memastikan format email valid (user@domain.com).

NIM: Memastikan input hanya berupa angka.

OOP (Object-Oriented Programming):

Menerapkan konsep Class, Inheritance (Pewarisan), Encapsulation (Data hiding untuk properti sensitif), dan Polymorphism.

4. Fitur Lanjutan (Email Automation)

📩 Notifikasi Nilai: Mengirim email personal ke mahasiswa berisi rincian IPK.

📂 Rekap Data: Mengirim backup seluruh database mahasiswa ke email admin dalam format JSON.

🛠️ Struktur Proyek

Proyek ini menerapkan konsep Modular Programming untuk mempermudah pemeliharaan kode:

📁 project-algo/
├── 📄 main.py              # Frontend: Mengatur GUI Streamlit & Navigasi
├── 📄 models.py            # Backend: Logika OOP, Class Mahasiswa, & File Manager
├── 📄 utils.py             # Tools: Algoritma (Sort/Search) & Fungsi Email SMTP
├── 📄 requirements.txt     # Daftar pustaka (library) yang digunakan
├── 📄 data_mahasiswa.json  # Database lokal (JSON)
└── 📁 assets/              # Menyimpan gambar logo & background


💻 Cara Menjalankan (Instalasi)

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda:

1. Clone Repository

git clone [https://github.com/username-kamu/project-algo.git](https://github.com/username-kamu/project-algo.git)
cd project-algo


2. Install Library
Pastikan Python sudah terinstal, lalu jalankan:

pip install -r requirements.txt


3. Konfigurasi Email (Opsional)
Agar fitur kirim email berfungsi, buat file .streamlit/secrets.toml dan isi dengan kredensial SMTP Gmail (Gunakan App Password, bukan password login biasa):

[general]
email_user = "email-anda@gmail.com"
email_password = "password-aplikasi-16-digit"


4. Jalankan Aplikasi

streamlit run main.py


📊 Analisis Kompleksitas

Fitur

Algoritma

Time Complexity (Average)

Keterangan

Cari Nama

Linear Search

$O(n)$

Iterasi satu per satu

Cari NIM

Binary Search

$O(\log n)$

Sangat cepat untuk data besar

Sort Data

Bubble Sort

$O(n^2)$

Lambat, untuk edukasi

Sort Data

Merge Sort

$O(n \log n)$

Stabil dan cepat

🖼️ Tampilan Aplikasi

(Anda bisa menambahkan screenshot aplikasi di sini nanti)

Copyright © 2025 Rizki Ramadani. Dibuat dengan ❤️ menggunakan Python & Streamlit.