import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders      
import streamlit as st
import os
import base64


# --- ALGORITMA SORTING & SEARCHING ---
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
        arr = data.copy() 
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
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

def send_email_notification(to_email, subject, body_html, body_plain=None, attachments=None):
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

    if body_plain:
        msg.attach(MIMEText(body_plain, 'plain'))

    msg.attach(MIMEText(body_html, 'html'))
    
    if attachments:
        for file_path, file_name in attachments:
            with open(file_path, "rb") as f:
                mime_file = MIMEBase("application", "octet-stream")
                mime_file.set_payload(f.read())
            
            encoders.encode_base64(mime_file)
            mime_file.add_header("Content-Disposition", f"attachment; filename={file_name}")
            msg.attach(mime_file)

    try:
#        server = smtplib.SMTP('smtp.gmail.com', 587)
#        server.starttls()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Gagal mengirim email: {e}")
        return False

# --- CUSTOM CSS (BACKGROUND & LOGO) ---
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_asset_local_or_online(local_path, online_url):
    if os.path.exists(local_path):
        try:
            ext = local_path.split('.')[-1]
            base64_str = get_img_as_base64(local_path)
            return f"data:image/{ext};base64,{base64_str}"
        except Exception as e:
            st.error(f"Gagal memuat gambar lokal: {e}")
            return online_url
    return online_url

logo_path = load_asset_local_or_online("assets/logo.png", "https://i.imgur.com/WJulW4w.png")
bg_login = load_asset_local_or_online("assets/bg_login.jpg", "https://i.imgur.com/hUT5YRQ.jpeg")
bg_dash = load_asset_local_or_online("assets/bg_dash.jpg", "https://biaya.info/wp-content/uploads/2023/03/2022-03-12.jpg")

def set_background(image_url, is_login=False):
    opacity = "0.55" if is_login else "0.65"
    
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

def render_logo(logo_path_input):
    """Menampilkan logo di tengah (login) dan sidebar"""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{logo_path_input}" width="120">
        </div>
        """,
        unsafe_allow_html=True
    )
    