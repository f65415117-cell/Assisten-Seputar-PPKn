import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & Tema Custom (Biar mirip Canva)
st.set_page_config(page_title="Generator Soal PPKn", layout="centered")

# CSS untuk membuat tampilan modern (Gaya Dark Mode & Card)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #ff4b2b, #ff416c);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px;
    }
    .header-box {
        background: linear-gradient(to right, #e52d27, #b31217);
        padding: 25px;
        border-radius: 15px 15px 0px 0px;
        color: white;
        text-align: center;
        margin-bottom: 0px;
    }
    .content-box {
        background-color: #1a1c24;
        padding: 30px;
        border-radius: 0px 0px 15px 15px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Ambil API Key dari Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Waduh, API Key belum masuk di Secrets!")

# Tampilan Judul
st.markdown('<div class="header-box"><h1>📖 Generator Soal PPKn</h1></div>', unsafe_allow_html=True)

# Container Utama
with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    st.write("⚙️ **Pengaturan Soal Profesional**")
    
    # Baris 1: Kelas & Jenis
    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox("Pilih Kelas", ["Kelas VII", "Kelas VIII", "Kelas IX"])
    with col2:
        jenis = st.selectbox("Jenis Soal", ["Pilihan Ganda", "Esai HOTS"])
        
    # Baris 2: Level & Jumlah
    col3, col4 = st.columns(2)
    with col3:
        level = st.selectbox("Level Kognitif", [
            "C1 - Mengingat", 
            "C2 - Memahami", 
            "C3 - Menerapkan", 
            "C4 - Menganalisis", 
            "C5 - Mengevaluasi", 
            "C6 - Mencipta"
        ])
    with col4:
        jumlah = st.number_input("Jumlah Soal", min_value=1, max_value=50, value=5)
        
    materi = st.text_area("Masukkan Materi PPKn:", height=150, placeholder="Tempel materi atau poin penting di sini...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tombol Aksi
    if st.button("✨ GENERATE SOAL SEKARANG"):
        if materi:
            try:
                # Menggunakan model Gemini Pro yang stabil
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                
                with st.spinner("Tunggu bentar, AI lagi mikir soal yang pas..."):
                    prompt = (f"Anda adalah Pakar PPKn Digital. Buatlah {jumlah} soal {jenis} "
                             f"untuk tingkat {kelas} dengan standar Level Kognitif {level}. "
                             f"Gunakan materi dasar berikut: {materi}. "
                             "Sajikan dalam format yang rapi, sertakan kunci jawaban dan pembahasan singkat.")
                    
                    response = model.generate_content(prompt)
                    st.success("Selesai! Ini hasilnya:")
                    st.markdown("---")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Ada kendala teknis: {e}")
        else:
            st.warning("Isi dulu materinya dong, Bro!")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Identitas
st.markdown("<br><p style='text-align: center; color: gray;'>Aplikasi by 1MWF Project</p>", unsafe_allow_html=True)
