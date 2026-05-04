import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import fitz # PyMuPDF

# --- CONFIG ---
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# --- CSS MINIMALIS (ALA RUMAH PENDIDIKAN) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .header-minimalis { display: flex; align-items: center; padding: 20px 0px; border-bottom: 1px solid #eaeaea; margin-bottom: 30px; }
    .logo-img { border-radius: 50%; margin-right: 15px; border: 1px solid #eee; }
    .title-text { color: #333; font-size: 1.5rem; font-weight: 800; margin: 0; }
    .subtitle-text { color: #666; font-size: 0.9rem; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
    <div class="header-minimalis">
        <img src="https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj" class="logo-img" width="50">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FORM INPUT ---
# Gunakan try-except agar kalau error tidak langsung putih halamannya
try:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            kelas = st.selectbox("Pilih Kelas", ["Pilih...", "Kelas VII", "Kelas VIII", "Kelas IX", "Kelas X", "Kelas XI", "Kelas XII"])
        with col2:
            jenis = st.selectbox("Jenis Soal", ["Pilih...", "Pilihan Ganda", "Esai HOTS", "Menjodohkan"])
        
        st.markdown("---")
        uploaded_file = st.file_uploader("📁 Upload Buku Referensi (PDF)", type="pdf")
        
        topik = st.text_area("Topik/Bab Pembelajaran:", placeholder="Contoh: Norma dan Keadilan...")
        
        if st.button("🚀 GENERATE SOAL"):
            st.write("Sedang memproses... (Fitur AI akan muncul di sini)")
except Exception as e:
    st.error(f"Ada kendala teknis: {e}")
