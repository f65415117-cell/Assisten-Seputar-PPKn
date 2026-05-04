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

# 3. CSS MODERN (LOGIKA JARAK SIMETRIS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .header-minimalis { 
        display: flex; align-items: center; padding: 20px 0px; 
        border-bottom: 1px solid #eaeaea; margin-bottom: 25px; 
    }
    .logo-img { border-radius: 50%; margin-right: 15px; border: 2px solid #007bff; padding: 2px; }
    .title-text { color: #333; font-size: 1.6rem; font-weight: 800; margin: 0; }
    .subtitle-text { color: #666; font-size: 0.95rem; margin: 0; }
    
    /* Merapikan Jarak Baris Form */
    [data-testid="stVerticalBlock"] > div { padding-bottom: 0px; margin-bottom: -10px; }
    
    .stButton>button { 
        width: 100%; background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); 
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONEKSI API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum terpasang!")

# 4. HEADER (Logo SPN PPKn)
logo_url = "https://yt3.googleusercontent.com/ytc/AIdro_k9jAOBysirU8tWHJ6xT4OQs6OvIBkC7JIjXf5uiUPKuA=s900-c-k-c0x00ffffff-no-rj"

st.markdown(f"""
    <div class="header-minimalis">
        <img src="{logo_url}" class="logo-img" width="65">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. FORM INPUT (SIMETRIS)
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        kelas = st.selectbox("1. Pilih Kelas", ["Pilih...", "Kelas VII", "Kelas VIII", "Kelas IX", "Kelas X", "Kelas XI", "Kelas XII"])
    with c2:
        jenis = st.selectbox("2. Jenis Soal", ["Pilih...", "Pilihan Ganda", "Esai HOTS", "Menjodohkan"])
    
    c3, c4 = st.columns(2)
    with c3:
        level = st.selectbox("3. Level Kognitif", ["Pilih...", "C1-C2", "C3-C4", "C5-C6"])
    with c4:
        jumlah = st.number_input("4. Jumlah Soal", 1, 50, 5)
    
    topik = st.text_area("5. Topik, Bab, atau Kisi-kisi Soal:", 
                         placeholder="Masukkan judul bab atau paste kisi-kisi soal di sini...",
                         height=120)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    if st.button("🚀 GENERATE SOAL & ADMINISTRASI"):
        if kelas == "Pilih..." or jenis == "Pilih..." or not topik:
            st.warning("Lengkapi data dulu, Bro!")
        else:
            try:
                # MODEL ELITE PILIHANMU
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                Bertindaklah sebagai Pakar Kurikulum PPKn.
                Input user: {topik}
                
                TUGAS:
                1. Jika user input KISI-KISI, tampilkan kembali kisi-kisi tersebut dalam TABEL ADMINISTRASI yang rapi dan formal.
                2. Jika user input JUDUL BAB, buatkan KISI-KISI SOAL yang relevan dalam TABEL ADMINISTRASI.
                3. Buatkan {jumlah} soal {jenis} untuk {kelas} (level {level}) yang SINKRON dengan kisi-kisi tersebut.
                
                FORMAT HASIL:
                - TABEL KISI-KISI (No, Lingkup Materi, Indikator Soal, Level, No Soal).
                - DAFTAR SOAL (Opsi A, B, C, D wajib ke bawah).
                - KUNCI & PEMBAHASAN.
                """
                
                with st.spinner("Sedang merapikan administrasi..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 Hasil Administrasi & Soal:")
                    st.write(response.text)
                    st.download_button("📥 Download (Word)", to_word(response.text), f"Soal_PPKn_{kelas}.docx")
            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
