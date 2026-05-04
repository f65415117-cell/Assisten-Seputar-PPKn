import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import fitz  # PyMuPDF untuk baca PDF kilat

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Seputar PPKn AI", layout="centered")

# 2. FUNGSI EKSTRAK PDF
def extract_pdf_fast(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 3. FUNGSI DOWNLOAD WORD
def to_word(text):
    doc = Document()
    doc.add_heading('Hasil Soal - Seputar PPKn AI', 0)
    doc.add_paragraph(text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# 4. CSS MINIMALIS (ALA RUMAH PENDIDIKAN)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .header-minimalis { display: flex; align-items: center; padding: 20px 0px; border-bottom: 1px solid #eaeaea; margin-bottom: 30px; }
    .logo-img { border-radius: 50%; margin-right: 15px; border: 1px solid #eee; }
    .title-text { color: #333; font-size: 1.5rem; font-weight: 800; margin: 0; }
    .subtitle-text { color: #666; font-size: 0.9rem; margin: 0; }
    .stButton>button { width: 100%; background: #007bff; color: white; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 5. KONEKSI KE GEMINI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum terpasang di Secrets Streamlit!")

# 6. HEADER
st.markdown(f"""
    <div class="header-minimalis">
        <img src="https://raw.githubusercontent.com/streamlit/norm-vignette/main/img/sample_profile.png" class="logo-img" width="50">
        <div>
            <h1 class="title-text">Seputar PPKn AI</h1>
            <p class="subtitle-text">Asisten Pembelajaran Digital PPKn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. FORM INPUT
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        kelas = st.selectbox("1. Pilih Kelas", ["Pilih...", "Kelas VII", "Kelas VIII", "Kelas IX", "Kelas X", "Kelas XI", "Kelas XII"])
    with col2:
        jenis = st.selectbox("2. Jenis Soal", ["Pilih...", "Pilihan Ganda", "Esai HOTS", "Menjodohkan"])
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📁 3. Upload Buku/Modul PDF (Opsional)", type="pdf")
    
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        level = st.selectbox("4. Level Kognitif", ["Pilih...", "C1-C2", "C3-C4", "C5-C6"])
    with col4:
        jumlah = st.number_input("5. Jumlah Soal", 1, 50, 5)
    
    topik = st.text_area("6. Topik/Bab Pembelajaran:", placeholder="Contoh: Norma dan Keadilan...")

    # 8. LOGIKA GENERATE
    if st.button("🚀 GENERATE SOAL SEKARANG"):
        if kelas == "Pilih..." or jenis == "Pilih..." or not topik:
            st.warning("Data belum lengkap, Bro!")
        else:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Baca PDF jika ada
                konteks = ""
                if uploaded_file:
                    with st.spinner("Membaca PDF tebal..."):
                        konteks = extract_pdf_fast(uploaded_file)[:30000] # Ambil 30rb karakter pertama
                
                prompt = f"""
                Buatkan {jumlah} soal {jenis} kelas {kelas} tentang {topik}.
                Level kognitif: {level}.
                Referensi: {konteks if konteks else 'Kurikulum Merdeka PPKn terbaru'}.
                
                ATURAN FORMAT:
                - Opsi jawaban (A, B, C, D) HARUS berderet ke bawah.
                - Berikan kunci jawaban dan pembahasan di akhir.
                """
                
                with st.spinner("Gemini lagi mikir..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 Hasil Soal:")
                    st.write(response.text)
                    st.download_button("📥 Download Word", to_word(response.text), f"Soal_{topik}.docx")
            except Exception as e:
                st.error(f"Error: {e}")
