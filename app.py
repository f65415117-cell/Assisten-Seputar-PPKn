import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# 2. FUNGSI DOWNLOAD WORD
def to_word(text):
    doc = Document()
    doc.add_heading('Hasil Soal - Seputar PPKn AI', 0)
    doc.add_paragraph(text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# 3. CSS MINIMALIS (ALA RUMAH PENDIDIKAN)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .header-minimalis { 
        display: flex; 
        align-items: center; 
        padding: 20px 0px; 
        border-bottom: 1px solid #eaeaea; 
        margin-bottom: 30px; 
    }
    .logo-img { border-radius: 50%; margin-right: 15px; border: 1px solid #007bff; }
    .title-text { color: #333; font-size: 1.5rem; font-weight: 800; margin: 0; }
    .subtitle-text { color: #666; font-size: 0.9rem; margin: 0; }
    .stButton>button { 
        width: 100%; 
        background: #007bff; 
        color: white; 
        border-radius: 10px; 
        font-weight: bold; 
        height: 3em; 
        border: none; 
    }
    .stButton>button:hover { background: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

# --- KONEKSI API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum terpasang di Secrets!")

# 4. HEADER MINIMALIS
st.markdown(f"""
    <div class="header-minimalis">
        <img src="https://raw.githubusercontent.com/streamlit/norm-vignette/main/img/sample_profile.png" class="logo-img" width="55">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. FORM INPUT
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox("1. Pilih Kelas", ["Pilih...", "Kelas VII", "Kelas VIII", "Kelas IX", "Kelas X", "Kelas XI", "Kelas XII"])
    with col2:
        jenis = st.selectbox("2. Jenis Soal", ["Pilih...", "Pilihan Ganda", "Esai HOTS", "Menjodohkan"])
    
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        level = st.selectbox("3. Level Kognitif", ["Pilih...", "C1-C2 (Pemahaman)", "C3-C4 (Aplikasi/Analisis)", "C5-C6 (Evaluasi/Kreasi)"])
    with col4:
        jumlah = st.number_input("4. Jumlah Soal", 1, 50, 5)
    
    topik = st.text_area("5. Topik/Bab Pembelajaran Spesifik:", placeholder="Contoh: Kedaulatan, Norma, atau Pancasila...")

    if st.button("🚀 GENERATE SOAL SEKARANG"):
        if kelas == "Pilih..." or jenis == "Pilih..." or not topik:
            st.warning("Lengkapi data dulu, Bro!")
        else:
            try:
                # PAKAI MODEL 2.5 FLASH LITE SEPERTI REQUES KAMU
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                Bertindaklah sebagai Pakar PPKn Indonesia.
                Buatlah {jumlah} soal {jenis} untuk {kelas} topik {topik} dengan level {level}.
                
                ATURAN FORMAT WAJIB:
                - Jika Pilihan Ganda, opsi (A, B, C, D) HARUS ditulis berderet ke bawah.
                - Gunakan standar Kurikulum Merdeka terbaru.
                - Sertakan kunci jawaban dan pembahasan di bagian akhir.
                """
                
                with st.spinner("Gemini 2.5 Flash Lite sedang bekerja..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 Hasil Soal:")
                    st.write(response.text)
                    st.download_button("📥 Download (Word)", to_word(response.text), f"Soal_{topik}.docx")
            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
