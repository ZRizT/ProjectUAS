import streamlit as st
import json
import re
import time
import os
from abc import ABC, abstractmethod

# 1. KONSEP OOP (Encapsulation, Inheritance, Polymorphism)
class Person(ABC):
    def __init__(self, nama, email):
        self.nama = nama
        self.email = email

    @abstractmethod
    def display_info(self):
        pass

# Child Class: Student (Inheritance)
class Student(Person):
    def __init__(self, nim, nama, email, jurusan, ipk):
        super().__init__(nama, email)
        self.__nim = nim       # Encapsulation (Private attribute)
        self.jurusan = jurusan
        self.__ipk = ipk       # Encapsulation

    # Getter & Setter (Encapsulation)
    def get_nim(self):
        return self.__nim

    def get_ipk(self):
        return self.__ipk

    def set_ipk(self, new_ipk):
        if 0.0 <= new_ipk <= 4.0:
            self.__ipk = new_ipk
        else:
            raise ValueError("IPK harus antara 0.0 dan 4.0")

    # Polymorphism: Implementasi method display_info
    def display_info(self):
        return {
            "NIM": self.__nim,
            "Nama": self.nama,
            "Email": self.email,
            "Jurusan": self.jurusan,
            "IPK": self.__ipk
        }
    
    # Method untuk convert ke Dict (JSON)
    def to_dict(self):
        return {
            "nim": self.__nim,
            "nama": self.nama,
            "email": self.email,
            "jurusan": self.jurusan,
            "ipk": self.__ipk
        }

# 2. MANAJEMEN DATA & FILE I/O
class StudentManager:
    def __init__(self, filename="data_mahasiswa.json"):
        self.filename = filename
        self.students = []
        self.load_data()

    # File I/O: Membaca data
    def load_data(self):
        if not os.path.exists(self.filename):
            self.save_data() # Buat file jika belum ada
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student(**item) for item in data]
        except (json.JSONDecodeError, IOError):
            self.students = []

    # File I/O: Menyimpan data
    def save_data(self):
        try:
            data = [s.to_dict() for s in self.students]
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            st.error(f"Gagal menyimpan data: {e}")

    # CRUD: Create
    def add_student(self, student):
        # Cek duplikasi NIM
        for s in self.students:
            if s.get_nim() == student.get_nim():
                raise ValueError("NIM sudah terdaftar!")
        self.students.append(student)
        self.save_data()

    # CRUD: Delete
    def delete_student(self, nim):
        original_count = len(self.students)
        self.students = [s for s in self.students if s.get_nim() != nim]
        if len(self.students) == original_count:
            raise ValueError("Mahasiswa tidak ditemukan.")
        self.save_data()

    # CRUD: Update (Edit IPK contohnya)
    def update_ipk(self, nim, new_ipk):
        for s in self.students:
            if s.get_nim() == nim:
                s.set_ipk(new_ipk)
                self.save_data()
                return True
        raise ValueError("Mahasiswa tidak ditemukan.")

    # Helper untuk mendapatkan list dict (untuk tampilan tabel)
    def get_all_data(self):
        return [s.to_dict() for s in self.students]

# 3. ALGORITMA SEARCHING & SORTING

class Algorithms:
    
    # --- SEARCHING ---
    
    @staticmethod
    def linear_search(data, key):
        """Sequential Search: O(n)"""
        results = []
        for student in data:
            if key.lower() in student.nama.lower():
                results.append(student)
        return results

    @staticmethod
    def binary_search_by_nim(data, target_nim):
        """Binary Search: O(log n) - Data harus terurut berdasarkan NIM"""
        # Sorting data sementara agar binary search bekerja
        sorted_data = sorted(data, key=lambda x: x.get_nim())
        
        low = 0
        high = len(sorted_data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            mid_val = sorted_data[mid].get_nim()
            
            if mid_val == target_nim:
                return [sorted_data[mid]]
            elif mid_val < target_nim:
                low = mid + 1
            else:
                high = mid - 1
        return []

    # --- SORTING ---

    @staticmethod
    def bubble_sort(data, key_attr, ascending=True):
        """Bubble Sort: O(n^2)"""
        arr = data.copy() # Copy agar tidak merusak data asli langsung
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                # Dinamis mengambil atribut (NIM, Nama, atau IPK)
                val_a = getattr(arr[j], key_attr) if hasattr(arr[j], key_attr) else (arr[j].get_nim() if key_attr == 'nim' else arr[j].get_ipk())
                val_b = getattr(arr[j+1], key_attr) if hasattr(arr[j+1], key_attr) else (arr[j+1].get_nim() if key_attr == 'nim' else arr[j+1].get_ipk())

                if ascending:
                    if val_a > val_b:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                else:
                    if val_a < val_b:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def merge_sort(data, key_attr, ascending=True):
        """Merge Sort: O(n log n)"""
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = Algorithms.merge_sort(data[:mid], key_attr, ascending)
        right = Algorithms.merge_sort(data[mid:], key_attr, ascending)

        return Algorithms._merge(left, right, key_attr, ascending)

    @staticmethod
    def _merge(left, right, key_attr, ascending):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            val_a = getattr(left[i], key_attr) if hasattr(left[i], key_attr) else (left[i].get_nim() if key_attr == 'nim' else left[i].get_ipk())
            val_b = getattr(right[j], key_attr) if hasattr(right[j], key_attr) else (right[j].get_nim() if key_attr == 'nim' else right[j].get_ipk())

            condition = (val_a < val_b) if ascending else (val_a > val_b)
            
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# 4. GUI & VALIDASI (STREAMLIT)

def main():
    st.set_page_config(page_title="Sistem Data Mahasiswa", page_icon="🎓")
    
    st.title("🎓 Manajemen Data Mahasiswa")
    st.markdown("Created by Rizki Ramadani | 241011400098 | Algoritma & Pemrograman Project")

    # Inisialisasi Manager
    if 'manager' not in st.session_state:
        st.session_state.manager = StudentManager()
    
    manager = st.session_state.manager

    # Sidebar Menu
    menu = st.sidebar.selectbox("Menu", ["Dashboard", "Tambah Mahasiswa", "Cari & Sortir", "Analisis Kompleksitas"])

    # --- DASHBOARD (READ & DELETE) ---
    if menu == "Dashboard":
        st.subheader("Daftar Seluruh Mahasiswa")
        
        data = manager.get_all_data()
        if data:
            st.dataframe(data, use_container_width=True)
            
            # Delete Section
            st.write("---")
            st.warning("Hapus Data")
            del_nim = st.text_input("Masukkan NIM untuk dihapus")
            if st.button("Hapus Mahasiswa"):
                try:
                    manager.delete_student(del_nim)
                    st.success(f"Mahasiswa dengan NIM {del_nim} berhasil dihapus!")
                    time.sleep(1)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
        else:
            st.info("Belum ada data mahasiswa. Silakan tambah data baru.")

    # --- CREATE (TAMBAH DATA) ---
    elif menu == "Tambah Mahasiswa":
        st.subheader("Input Data Baru")
        
        with st.form("add_form"):
            nim = st.text_input("NIM (Nomor Induk)")
            nama = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            jurusan = st.selectbox("Jurusan", ["Informatika", "Sistem Informasi", "Teknik Mesin", "Teknik Elektro"])
            ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, step=0.01)
            
            submitted = st.form_submit_button("Simpan Data")
            
            if submitted:
                # Validasi Input (Regex & Try-Catch)
                try:
                    if not nim or not nama or not email:
                        raise ValueError("Semua field wajib diisi!")
                    
                    # Regex Email Validation
                    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    if not re.match(email_pattern, email):
                        raise ValueError("Format email tidak valid!")
                    
                    # Regex NIM (Contoh: hanya angka)
                    if not re.match(r'^\d+$', nim):
                        raise ValueError("NIM harus berupa angka!")

                    new_student = Student(nim, nama, email, jurusan, ipk)
                    manager.add_student(new_student)
                    st.success("Data berhasil ditambahkan!")
                    
                except ValueError as e:
                    st.error(f"Error Validasi: {e}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")

    # --- SEARCHING & SORTING ---
    elif menu == "Cari & Sortir":
        st.subheader("Pencarian & Pengurutan")
        
        tab1, tab2 = st.tabs(["🔍 Pencarian", "🔃 Pengurutan"])
        
        with tab1:
            search_method = st.radio("Metode Cari", ["Linear Search (By Nama)", "Binary Search (By NIM)"])
            query = st.text_input("Masukkan Kata Kunci")
            
            if st.button("Cari"):
                start_time = time.time()
                
                if search_method == "Linear Search (By Nama)":
                    result = Algorithms.linear_search(manager.students, query)
                else:
                    result = Algorithms.binary_search_by_nim(manager.students, query)
                
                end_time = time.time()
                
                if result:
                    st.write(f"Ditemukan {len(result)} data dalam {(end_time - start_time):.6f} detik.")
                    st.dataframe([s.to_dict() for s in result])
                else:
                    st.warning("Data tidak ditemukan.")

        with tab2:
            sort_algo = st.selectbox("Algoritma", ["Bubble Sort", "Merge Sort"])
            sort_key = st.selectbox("Berdasarkan", ["IPK", "Nama"])
            order = st.radio("Urutan", ["Ascending (A-Z / 0-4)", "Descending (Z-A / 4-0)"])
            is_asc = True if order.startswith("Ascending") else False
            
            attr_map = {"IPK": "ipk", "Nama": "nama"} # Mapping ke atribut internal/getter
            
            if st.button("Urutkan Data"):
                start_time = time.time()
                
                # Menentukan atribut yang dipakai untuk sort
                target_attr = "ipk" if sort_key == "IPK" else "nama" 
                # Khusus IPK diakses lewat getter logic di algo, nama via atribut langsung
                
                if sort_algo == "Bubble Sort":
                    sorted_list = Algorithms.bubble_sort(manager.students, target_attr, is_asc)
                else:
                    sorted_list = Algorithms.merge_sort(manager.students, target_attr, is_asc)
                
                end_time = time.time()
                
                st.write(f"Selesai diurutkan dalam {(end_time - start_time):.6f} detik.")
                st.dataframe([s.to_dict() for s in sorted_list])

    # --- ANALISIS KOMPLEKSITAS ---
    elif menu == "Analisis Kompleksitas":
        st.subheader("Estimasi Time Complexity")
        
        st.markdown("""
        Berikut adalah analisis kompleksitas algoritma yang digunakan dalam aplikasi ini:
        
        ### 1. Searching
        | Algoritma | Best Case | Average Case | Worst Case | Keterangan |
        | :--- | :--- | :--- | :--- | :--- |
        | **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | Cek satu per satu, lambat untuk data besar. |
        | **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | Sangat cepat, tapi data **wajib urut** dulu. |
        
        ### 2. Sorting
        | Algoritma | Best Case | Average Case | Worst Case | Keterangan |
        | :--- | :--- | :--- | :--- | :--- |
        | **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | Mudah implementasi, performa buruk di data besar. |
        | **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | Stabil dan cepat (Divide & Conquer). |
        
        ### 3. Space Complexity
        - Aplikasi ini menggunakan Array (List) untuk menyimpan objek `Student`.
        - **Merge Sort** memakan memori tambahan $O(n)$ karena rekursi dan pembuatan list baru.
        """)

if __name__ == "__main__":
    main()