import streamlit as st
import time
import pandas as pd
from models import Student, StudentManager
import utils
import json

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
    # URL Gambar Background Login (Ganti dengan file lokal atau URL kamu)
    # Contoh pakai placeholder image
    bg_login = "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070&auto=format&fit=crop"
    utils.set_background(bg_login, is_login=True)

    utils.render_logo() # Logo default
    
    st.markdown("<h1 style='text-align: center;'>Portal Akademik</h1>", unsafe_allow_html=True)
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
    # URL Gambar Background Dashboard (Ganti dengan assetmu)
    bg_dash = "https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=50070&auto=format&fit=crop"
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

    # 2. INPUT DATA
    elif menu == "Input Data":
        with st.form("input_form"):
            col1, col2 = st.columns(2)
            nim = col1.text_input("NIM")
            nama = col2.text_input("Nama")
            email = col1.text_input("Email")
            jurusan = col2.selectbox("Jurusan", ["Informatika", "SI", "DKV"])
            ipk = st.number_input("IPK", 0.0, 4.0, step=0.01)
            
            if st.form_submit_button("Simpan"):
                try:
                    new_s = Student(nim, nama, email, jurusan, ipk)
                    manager.add_student(new_s)
                    st.success("Data tersimpan!")
                except Exception as e: st.error(str(e))

    # 3. KIRIM EMAIL (FITUR BARU)
    elif menu == "Kirim Email":
        st.info("📨 Fitur Notifikasi Email")
        
        tab1, tab2 = st.tabs(["Kirim ke Satu Mahasiswa", "Kirim Rekap Database"])
        
        # Kirim IPK Personal
        with tab1:
            target_nim = st.selectbox("Pilih Mahasiswa", [s['nim'] for s in manager.get_all_data()])
            if st.button("Kirim Notifikasi IPK"):
                # Cari data
                mhs = next((s for s in manager.students if s.get_nim() == target_nim), None)
                if mhs:
                    subjek = f"Pemberitahuan IPK Semester - {mhs.nama}"
                    isi = f"Halo {mhs.nama},\n\nBerikut adalah hasil studi Anda:\nNIM: {mhs.get_nim()}\nIPK: {mhs.get_ipk()}\n\nTetap semangat!\nAdmin Kampus."
                    
                    with st.spinner("Mengirim email..."):
                        if utils.send_email_notification(mhs.email, subjek, isi):
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
        data = manager.students
        algo = st.selectbox("Metode Sort", ["Bubble Sort"])
        key = "ipk"
        
        if st.button("Urutkan Ranking IPK"):
            sorted_data = utils.Algorithms.bubble_sort(data, key, ascending=False)
            st.write("### Peringkat Mahasiswa (Tertinggi ke Terendah)")
            st.table([s.to_dict() for s in sorted_data])

# --- LOGIC SWITCHER ---
if st.session_state.is_logged_in:
    dashboard_page()
else:
    login_page()