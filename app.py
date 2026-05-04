import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# 1. Konfigurasi Halaman (Judul di Tab Browser)
st.set_page_config(page_title="Seputar PPKn AI - Asisten Digital", layout="centered")

# 2. CSS Custom: Gaya Minimalis Ala 'Rumah Pendidikan'
st.markdown("""
    <style>
    /* 1. Background Utama Jadi Putih Bersih */
    .stApp { background-color: #ffffff; }

    /* 2. Gaya Container Header Rata Kiri */
    .header-minimalis { 
        display: flex; 
        align-items: center; 
        padding: 20px 0px 30px 0px; 
        border-bottom: 1px solid #eaeaea; /* Garis tipis di bawah header */
        margin-bottom: 30px; 
    }

    /* 3. Gaya Logo Bulat di Kiri */
    .logo-img { 
        border-radius: 50%; 
        border: 2px solid #007bff; /* Aksen biru tipis di logo */
        background-color: white; 
        margin-right: 20px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
    }

    /* 4. Gaya Teks Judul dan Tagline */
    .title-text { 
        color: #333333; 
        font-size: 1.8rem; 
        font-weight: 800; 
        margin: 0; 
        line-height: 1.2; 
    }
    .subtitle-text { 
        color: #666666; 
        font-size: 1rem; 
        font-weight: 400; 
        margin: 0; 
    }

    /* 5. Merapikan Label Form */
    label { color: #555555 !important; font-weight: 600; }

    /* 6. Gaya Tombol Biru yang Modern */
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
        color: white; 
        border: none; 
        padding: 14px; 
        border-radius: 10px; 
        font-weight: bold; 
        box-shadow: 0 4px 6px rgba(0, 123, 255, 0.15); 
    }
    .stButton>button:hover { background: linear-gradient(135deg, #0056b3 0%, #004085 100%); }
    </style>
    """, unsafe_allow_html=True)

# 3. Struktur Header Baru (HTML Rata Kiri)
st.markdown(f"""
    <div class="header-minimalis">
        <img src="https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj" class="logo-img" width="70">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Sisa kode form (st.selectbox, st.text_area, dll) tetap sama ---
# ... (Masukkan kode input form dan logika AI kamu di sini)
