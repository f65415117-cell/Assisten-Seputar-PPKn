import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# 2. CSS Custom: Gaya Sinematik dengan Logo
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
    }
    
    /* Styling Logo agar melingkar dan estetik */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: -20px;
        position: relative;
        z-index: 1;
    }
    
    .logo-img {
        border-radius: 50%;
        border: 4px solid #b31217;
        box-shadow: 0 0 20px rgba(179, 18, 23, 0.5);
        background-color: white;
    }
    
    .header-container {
        background: linear-gradient(135deg, #b31217 0%, #e52d27 100%);
        padding: 50px 20px 30px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    
    label { color: #c9d1d9 !important; font-weight: bold; }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        color: white;
        border: none;
        padding: 18px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.4s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 75, 43, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONEKSI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum ada di Secrets!")

# --- TAMPILAN HEADER DENGAN LOGO ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj" class="logo-img" width="120">
    </div>
    <div class="header-container">
        <h1 style="margin-top: 20px;">🚀 Seputar PPKn AI</h1>
        <p>Asisten Digital Cerdas by 1MWF</p>
    </div>
    """, unsafe_allow_html=True)

# --- FORM INPUT ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox("Pilih Kelas", ["Kelas VII", "Kelas VIII", "Kelas IX"])
    with col2:
        jenis = st.selectbox("Jenis Soal", ["Pilihan Ganda", "Esai HOTS"])
        
    level = st.selectbox("Level Kognitif", ["C1-C2 (Pemahaman)", "C3-C4 (Aplikasi/Analisis)", "C5-C6 (Evaluasi/Kreasi)"])
    materi = st.text_area("Masukkan Materi PPKn:", placeholder="Tempel materi di sini...", height=150)
    
    if st.button("✨ GENERATE SOAL SEKARANG"):
        if materi:
            try:
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                prompt = f"Buatkan 5 soal {jenis} {kelas} level {level} materi: {materi}. Sertakan kunci dan pembahasan."
                with st.spinner("Meracik soal..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 Hasil Soal:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("<br><p style='text-align: center; color: #8b949e;'>© 2026 1MWF Project</p>", unsafe_allow_html=True)
