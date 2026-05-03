import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# 2. CSS Custom: Tema Biru Putih Bersih
st.markdown("""
    <style>
    /* Background utama putih abu-abu sangat muda agar mata tidak lelah */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Logo Container */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: -25px;
        position: relative;
        z-index: 1;
    }
    
    .logo-img {
        border-radius: 50%;
        border: 4px solid #007bff; /* Biru Primer */
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
        background-color: white;
    }
    
    /* Header Box Biru Modern */
    .header-container {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        padding: 50px 20px 30px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    /* Warna Label Input */
    label { 
        color: #333333 !important; 
        font-weight: bold; 
    }
    
    /* Tombol Generate Biru */
    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #007bff, #0056b3);
        color: white;
        border: none;
        padding: 16px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
        background: linear-gradient(to right, #0056b3, #004494);
    }

    /* Kotak Input */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #dee2e6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONEKSI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum terpasang di Secrets!")

# --- TAMPILAN HEADER ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj" class="logo-img" width="120">
    </div>
    <div class="header-container">
        <h1 style="margin-top: 20px; font-size: 2.5rem;">Seputar PPKn AI</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">Assisten Pembelajaran Digital PPKn</p>
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
    materi = st.text_area("Masukkan Materi PPKn:", placeholder="Tempelkan teks materi atau ringkasan bab di sini...", height=150)
    
    if st.button("✨ GENERATE SOAL SEKARANG"):
        if materi:
            try:
                # Memakai model 2.5 Flash-Lite yang sudah terbukti jalan di akunmu
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                prompt = f"Anda adalah pakar PPKn. Buatkan 5 soal {jenis} untuk {kelas} dengan level {level}. Sumber materi: {materi}. Berikan kunci jawaban dan pembahasan singkat."
                
                with st.spinner("Sedang menyusun soal..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 Hasil Soal:")
                    st.info(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Silakan masukkan materi terlebih dahulu, Bro.")

st.markdown("<br><p style='text-align: center; color: #6c757d; font-size: 0.8rem;'>© 2026 1MWF Project • Seputar PPKn AI</p>", unsafe_allow_html=True)
