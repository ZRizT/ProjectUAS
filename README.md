# 🎓 Sistem Manajemen Data Mahasiswa (SMDM)
Kunjungi [SMDM](https://projectuas-ap2-0098.streamlit.app) untuk mengakses aplikasi ini.

---

Proyek Tugas Akhir (UAS) - **Algoritma dan Pemrograman**  
Dikembangkan untuk mendemonstrasikan penerapan **struktur data**, **algoritma pengurutan/pencarian**, **OOP (Object-Oriented Programming)**, dan **integrasi API sederhana**.

---

## 👨‍💻 Identitas Developer
**Nama:** Rizki Ramadani  
**NIM:** 241011400098
**Mata Kuliah:** Algoritma dan Pemrograman 2


---

## 🚀 Fitur Utama

Aplikasi ini dibangun berbasis **GUI Web** menggunakan **Streamlit**, dengan fitur lengkap sebagai berikut:

---

### **1. Manajemen Data (CRUD) & File I/O**
- **Create** → Input data mahasiswa baru dengan validasi ketat  
- **Read** → Menampilkan data dalam tabel interaktif  
- **Update** → Edit data mahasiswa (IPK / Jurusan)  
- **Delete** → Menghapus data mahasiswa dari database  
- **Persistensi Data** → Data disimpan permanen dalam format **JSON**

---

### **2. Implementasi Algoritma**

#### 🔍 **Pencarian (Searching)**  
- **Linear Search** → Mencari mahasiswa berdasarkan Nama *(partial match)*  
- **Binary Search** → Mencari mahasiswa berdasarkan NIM *(data diurutkan otomatis)*  
  - Kompleksitas: **O(log n)**

#### 🔃 **Pengurutan (Sorting)**
- **Bubble Sort** → Metode sederhana, cocok untuk edukasi  
  - Kompleksitas: **O(n²)**
- **Merge Sort** → Metode efisien Divide & Conquer  
  - Kompleksitas: **O(n log n)**

---

### **3. Validasi & Keamanan (Regex & OOP)**

#### ✔ **Validasi Input (Regex)**
- Email → Format email valid (`user@domain.com`)  
- NIM → Hanya angka  
- Nama → Valid dan aman  

#### 🧩 **OOP Concepts**
- **Class**
- **Inheritance**
- **Encapsulation**
- **Polymorphism**

---

### **4. Fitur Lanjutan (Email Automation)**

📩 **Notifikasi Nilai** → Mengirim email personal berisi IPK  
📂 **Rekap Data** → Mengirim backup database JSON ke admin  

---

## 🛠️ Struktur Proyek
```text
ProjectUAS/
├── main.py             # Frontend: GUI Streamlit & Navigasi
├── models.py           # Backend: OOP, Class Mahasiswa, File Manager
├── utils.py            # Tools: Algoritma (Sort/Search), CSS, Email SMTP
├── requirements.txt    # Library yang digunakan
├── data_mahasiswa.json # Database lokal (JSON)
└── assets/             # Gambar logo & background
```

---

## 💻 Cara Menjalankan (Instalasi)

### **1. Clone Repository**
```bash
git clone https://github.com/ZRizT/ProjectUAS
cd ProjectUAS
```

### **2. Install Library**
Pastikan Python sudah terinstal, lalu jalankan:
```bash
pip install -r requirements.txt
```

### **3. Konfigurasi Email (Opsional)**
Agar fitur kirim email berfungsi, buat file `.streamlit/secrets.toml` dan isi dengan kredensial SMTP Gmail (Gunakan App Password, bukan password login biasa):
```toml
email_user = "email-anda@gmail.com"
email_password = "password-aplikasi-16-digit"    
```         

### **4. Jalankan Aplikasi**
```bash
streamlit run main.py
```

---

## 📊 Analisis Kompleksitas

| Fitur     | Algoritma      | Waktu Rata-rata | Keterangan                               |
|-----------|----------------|-----------------|-------------------------------------------|
| Cari Nama | Linear Search  | *O(n)*            | Iterasi satu per satu                    |
| Cari NIM  | Binary Search  | *O(log n)*        | Sangat cepat (data harus urut)           |
| Sort Data | Bubble Sort    | *O(n²)*           | Lambat, untuk edukasi                    |
| Sort Data | Merge Sort     | *O(n log n)*      | Stabil & cepat (Divide & Conquer)        |

---

Copyright © 2025 **Rizki Ramadani**  
Dibuat dengan ❤️ menggunakan *Python & Streamlit*


