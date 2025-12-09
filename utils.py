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

def template_ipk(mhs):
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                background: #ffffff;
                margin: 30px auto;
                padding: 25px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #eeeeee;
                padding-bottom: 15px;
                margin-bottom: 25px;
            }}
            .header h2 {{
                color: #2b3d63;
                margin: 0;
                font-size: 22px;
                font-weight: 600;
            }}
            .box {{
                background: #f0f4ff;
                padding: 15px;
                border-left: 4px solid #355ad4;
                border-radius: 6px;
                margin: 15px 0;
            }}
            .footer {{
                margin-top: 35px;
                font-size: 12px;
                color: #818181;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Pemberitahuan Hasil Studi Semester</h2>
            </div>

            <p>Halo <b>{mhs.nama}</b>,</p>
            <p>Berikut adalah hasil evaluasi akademik Anda:</p>

            <div class="box">
                <p><b>NIM :</b> {mhs.get_nim()}</p>
                <p><b>IPK :</b> {mhs.get_ipk()}</p>
            </div>

            <p>
                Semoga Anda dapat mempertahankan dan meningkatkan prestasi akademik ke depannya.
                Jika terdapat pertanyaan, silakan menghubungi bagian Akademik.
            </p>

            <p>Salam hormat,<br><b>Admin Kampus</b></p>

            <div class="footer">
                Email dikirim otomatis oleh sistem akademik. Mohon tidak membalas pesan ini.
            </div>
        </div>
    </body>
    </html>
    """


# --- EMAIL SENDER (SMTP) ---

def send_email_notification(to_email, subject, body_html, body_plain=None):
    if 'email_user' not in st.secrets or 'email_password' not in st.secrets:
        st.warning("⚠️ Fitur email dalam Mode Simulasi (Credentials belum diset). Email tidak benar-benar terkirim.")
        print(f"SIMULASI KIRIM KE: {to_email}\nISI HTML:\n{body_html}")
        return True

    sender_email = st.secrets["email_user"]
    sender_password = st.secrets["email_password"]

    msg = MIMEMultipart("alternative")  
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # fallback jika client tidak bisa HTML
    if body_plain is None:
        body_plain = "Anda menerima notifikasi akademik. Silakan buka email menggunakan aplikasi yang mendukung HTML."

    msg.attach(MIMEText(body_plain, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Gagal mengirim email: {e}")
        return False

# --- CUSTOM CSS (BACKGROUND & LOGO) ---

image_url = "https://i.imgur.com/hUT5YRQ.jpeg"
def set_background(image_url, is_login=False):
    opacity = "0.75" if is_login else "0.65"
    
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

def render_logo(logo_path="https://i.imgur.com/WJulW4w.png"):
    """Menampilkan logo di tengah (login) dan sidebar"""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{logo_path}" width="120">
        </div>
        """,
        unsafe_allow_html=True
    )
    