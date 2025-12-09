import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# --- ALGORITMA SORTING & SEARCHING ---

class Algorithms:
    @staticmethod
    def linear_search(data, key):
        return [s for s in data if key.lower() in s.nama.lower()]

    @staticmethod
    def bubble_sort(data, key_attr, ascending=True):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                val_a = getattr(arr[j], key_attr) if hasattr(arr[j], key_attr) else (arr[j].get_nim() if key_attr == 'nim' else arr[j].get_ipk())
                val_b = getattr(arr[j+1], key_attr) if hasattr(arr[j+1], key_attr) else (arr[j+1].get_nim() if key_attr == 'nim' else arr[j+1].get_ipk())
                
                if ascending:
                    if val_a > val_b: arr[j], arr[j+1] = arr[j+1], arr[j]
                else:
                    if val_a < val_b: arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

# --- EMAIL SENDER (SMTP) ---

def send_email_notification(to_email, subject, body):
    # Cek apakah credential ada di secrets (untuk keamanan)
    if 'email_user' not in st.secrets or 'email_password' not in st.secrets:
        st.warning("⚠️ Fitur email dalam Mode Simulasi (Credentials belum diset). Email tidak benar-benar terkirim.")
        print(f"SIMULASI KIRIM KE: {to_email}\nISI: {body}")
        return True

    sender_email = st.secrets["email_user"]
    sender_password = st.secrets["email_password"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Gunakan Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Gagal mengirim email: {e}")
        return False

# --- CUSTOM CSS (BACKGROUND & LOGO) ---

def set_background(image_url, is_login=False):
    """
    Mengatur background dengan overlay putih transparan.
    Bisa menerima URL internet atau path lokal (harus di encode base64 jika lokal, 
    tapi untuk simplifikasi kita pakai URL/Path string di CSS).
    """
    
    # Overlay logic: Login lebih tebal putihnya (0.85), Dashboard lebih tipis (0.5)
    opacity = "0.85" if is_login else "0.95"
    
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def render_logo(logo_path="https://imgur.com/gallery/logo-uBl34rq#WJulW4w"):
    """Menampilkan logo di tengah (biasanya untuk login) atau sidebar"""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{logo_path}" width="120">
        </div>
        """,
        unsafe_allow_html=True
    )