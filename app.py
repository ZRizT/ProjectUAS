import streamlit as st
import time
import pandas as pd
from models import Student, StudentManager
import utils
import json
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Akademik", page_icon="🎓", layout="centered")

# --- INITIALIZATION ---
if 'manager' not in st.session_state:
    st.session_state.manager = StudentManager()

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

manager = st.session_state.manager

# --- FUNGSI HALAMAN LOGIN ---
def login_page():
    # URL Gambar Background Login
    bg_login = "https://i.imgur.com/hUT5YRQ.jpeg"
    utils.set_background(bg_login, is_login=True)

    utils.render_logo() # Logo default
    
    st.markdown("<h1 style='text-align: center;'>Portal Akademik 'SMDM'</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Silakan login untuk melanjutkan</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            role = st.selectbox("Masuk Sebagai", ["Admin / Dosen", "Mahasiswa"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            login_btn = st.button("Masuk", use_container_width=True)
            
            if login_btn:
                # Validasi Login Sederhana
                if role == "Admin / Dosen":
                    if username == "admin" and password == "admin123":
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "admin"
                        st.success("Login Berhasil!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")
                
                elif role == "Mahasiswa":
                    st.warning("⚠️ Fitur Login Mahasiswa sedang dalam perbaikan. Silakan hubungi Admin.")

# --- FUNGSI HALAMAN DASHBOARD ---
def dashboard_page():
    bg_dash = "https://i.imgur.com/hUT5YRQ.jpeg"
    utils.set_background(bg_dash, is_login=False)

    # Sidebar
    with st.sidebar:
        utils.render_logo(logo_path="https://i.imgur.com/WJulW4w.png")
        st.write(f"Selamat datang, **{st.session_state.user_role.capitalize()}**")
        
        menu = st.radio("Navigasi", ["Data Mahasiswa", "Input Data", "Kirim Email", "Analisis"])
        
        st.divider()
        if st.button("Logout"):
            st.session_state.is_logged_in = False
            st.rerun()

    st.title(f"🎓 Menu {menu}")

    # 1. VIEW DATA
    if menu == "Data Mahasiswa":
        data = manager.get_all_data()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Fitur Delete
            with st.expander("Hapus Data"):
                del_nim = st.text_input("Masukkan NIM data yang ingin dihapus")
                if st.button("Hapus"):
                    try:
                        manager.delete_student(del_nim)
                        st.success("Data terhapus.")
                        time.sleep(0.5); st.rerun()
                    except ValueError as e: st.error(str(e))
        else:
            st.info("Data kosong.")

    # 2. INPUT DATA REGEX VALIDATION
    elif menu == "Input Data":
        with st.form("input_form"):
            col1, col2 = st.columns(2)
            nim = col1.text_input("NIM")
            nama = col2.text_input("Nama")
            email = col1.text_input("Email")
            jurusan = col2.selectbox("Jurusan", ["Informatika", "SI", "Teknik Elektro", "Manajemen", "Akuntansi"])
            ipk = st.number_input("IPK", 0.0, 4.0, step=0.01)
            
            if st.form_submit_button("Simpan"):
                try:
                    if not nim or not nama or not email:
                        raise ValueError("Semua field wajib diisi!")
                                        
                    # Regex NIM dan NAMA (Contoh: hanya angka/huruf)
                    if not re.match(r'^[a-zA-Z]{3,50}$', nama):
                        raise ValueError("Nama harus berupa minimal 3 huruf!")

                    if not re.match(r'^\d{10,12}$', nim):
                        raise ValueError("NIM harus terdiri dari 10-12 digit angka!")
                    
                    # Regex Email Validation
                    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    if not re.match(email_pattern, email):
                        raise ValueError("Format email tidak valid!")                    
                    
                    new_student = Student(nim, nama, email, jurusan, ipk)
                    manager.add_student(new_student)
                    st.success("Data berhasil ditambahkan!")
                    
                except ValueError as e:
                    st.error(f"Error Validasi: {e}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")                

    # 3. KIRIM EMAIL
    elif menu == "Kirim Email":
        st.info("Kirim Notifikasi Email")
        
        tab1, tab2 = st.tabs(["Kirim ke Satu Mahasiswa", "Kirim Rekap Database"])
        
        # Kirim IPK Personal
        with tab1:
            target_nim = st.selectbox("Pilih Mahasiswa", [s['nim'] for s in manager.get_all_data()])
            if st.button("Kirim Notifikasi IPK"):
                # Cari data
                mhs = next((s for s in manager.students if s.get_nim() == target_nim), None)
                if mhs:
                    subjek = f"Pemberitahuan IPK Semester - {mhs.nama}"
                    isi_html = utils.template_ipk(mhs)
                    isi_plain = f"Halo {mhs.nama}, berikut hasil evaluasi: NIM {mhs.get_nim()}, IPK {mhs.get_ipk()}."
       
                    with st.spinner("Mengirim email..."):
                        if utils.send_email_notification(mhs.email, subjek, isi_html, isi_plain):
                            st.success(f"Email terkirim ke {mhs.email}")
                else:
                    st.error("Mahasiswa tidak ditemukan.")

        # Kirim Rekap ke Email Admin/Tujuan
        with tab2:
            target_email = st.text_input("Email Tujuan Rekap")
            if st.button("Kirim Data Rekap"):
                data_str = json.dumps(manager.get_all_data(), indent=4)
                subjek = "Rekapitulasi Data Mahasiswa"
                isi = f"Berikut adalah data rekap terbaru:\n\n{data_str}"
                
                with st.spinner("Mengirim rekap..."):
                    if utils.send_email_notification(target_email, subjek, isi):
                        st.success("Rekap data berhasil dikirim.")

    # 4. ANALISIS (SORTING)
    
    elif menu == "Analisis":
        st.subheader("Pencarian & Pengurutan")
        
        tab1, tab2 = st.tabs(["🔍 Pencarian", "🔃 Pengurutan"])
        
        with tab1:
            search_method = st.radio("Metode Cari", ["Linear Search (By Nama)", "Binary Search (By NIM)"])
            query = st.text_input("Masukkan Kata Kunci")
            
            if st.button("Cari"):
                start_time = time.time()
                
                if search_method == "Linear Search (By Nama)":
                    result = utils.Algorithms.linear_search(manager.students, query)
                else:
                    result = utils.Algorithms.binary_search_by_nim(manager.students, query)
                
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
                    sorted_list = utils.Algorithms.bubble_sort(manager.students, target_attr, is_asc)
                else:
                    sorted_list = utils.Algorithms.merge_sort(manager.students, target_attr, is_asc)
                
                end_time = time.time()
                
                st.write(f"Selesai diurutkan dalam {(end_time - start_time):.6f} detik.")
                st.dataframe([s.to_dict() for s in sorted_list])    

# --- LOGIC SWITCHER ---
if st.session_state.is_logged_in:
    dashboard_page()
else:
    login_page()