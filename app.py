import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# 2. FUNGSI DOWNLOAD WORD
def to_word(text):
    doc = Document()
    doc.add_heading('Administrasi Soal - Seputar PPKn AI', 0)
    doc.add_paragraph(text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# 3. CSS MODERN (VERSI JARAK IDEAL)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Header dikasih ruang biar logo gak kepotong */
    .header-minimalis { 
        display: flex; 
        align-items: center; 
        padding: 25px 0px; 
        border-bottom: 1px solid #f0f0f0; 
        margin-bottom: 35px; 
    }
    .logo-img { 
        border-radius: 50%; 
        margin-right: 20px; 
        border: 2px solid #007bff; 
        padding: 3px;
        object-fit: cover;
    }
    .title-text { color: #333; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .subtitle-text { color: #666; font-size: 1rem; margin: 0; }
    
    /* Jarak antar baris form yang pas (Normal) */
    .stSelectbox, .stNumberInput, .stTextArea {
        margin-bottom: 15px;
    }
    
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
        color: white; 
        border-radius: 12px; 
        font-weight: bold; 
        height: 3.8em; 
        border: none;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONEKSI API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum terpasang!")

# 4. HEADER (Logo SPN PPKn Kamu)
logo_url = "https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj"

st.markdown(f"""
    <div class="header-minimalis">
        <img src="{logo_url}" class="logo-img" width="75">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. FORM INPUT (SIMETRIS & BERNAFAS)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox("1. Pilih Kelas", ["Pilih...", "Kelas VII", "Kelas VIII", "Kelas IX"])
    with col2:
        jenis = st.selectbox("2. Jenis Soal", ["Pilih...", "Pilihan Ganda", "Esai HOTS", "Menjodohkan"])
    
    col3, col4 = st.columns(2)
    with col3:
        level = st.selectbox("3. Level Kognitif", ["Pilih...", "C1-C2", "C3-C4", "C5-C6"])
    with col4:
        jumlah = st.number_input("4. Jumlah Soal", 1, 50, 5)
    
    topik = st.text_area("5. Topik atau Bab Pembelajaran:", 
                         placeholder="Contoh: Norma Masyarakat, Kedaulatan NKRI, atau Pancasila...",
                         height=120)

    if st.button("🚀 GENERATE SOAL SEKARANG"):
        if kelas == "Pilih..." or jenis == "Pilih..." or not topik:
            st.warning("Data belum lengkap, Bro!")
        else:
            try:
                # MODEL GEMINI 2.5 FLASH-LITE
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                Anda Pakar PPKn Indonesia. Buat tabel kisi-kisi dan {jumlah} soal {jenis} kelas {kelas} topik {topik} level {level}.
                Format A, B, C, D wajib berderet ke bawah. Sertakan kunci dan pembahasan.
                """
                
                with st.spinner("Lagi nyusun administrasi..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 Hasil:")
                    st.write(response.text)
                    st.download_button("📥 Download (Word)", to_word(response.text), f"Soal_PPKn_{kelas}.docx")
            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
                
