import streamlit as st
import google.generativeai as genai

# Tampilan halaman
st.set_page_config(page_title="Pakar PPKn Digital", layout="wide")

# Ambil API Key dari settingan rahasia nanti
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum disetting di Secrets!")

# Bagian Samping (Sidebar)
with st.sidebar:
    st.title("🇮🇩 Menu Panel")
    fase = st.selectbox("Pilih Fase", ["Fase D (SMP)", "Fase E (SMA)", "Fase F (SMA)"])
    level = st.select_slider("Level Kognitif", options=["C1", "C2", "C3", "C4", "C5", "C6"])
    tipe = st.radio("Buat Apa?", ["Soal Pilihan Ganda", "Soal Esai HOTS", "Ringkasan Materi"])
    jumlah = st.number_input("Jumlah", min_value=1, max_value=20, value=5)
    st.markdown("---")
    st.caption("Aplikasi by 1MWF Project")

# Bagian Utama
st.title("Asisten Guru PPKn Digital")
st.write("Gunakan AI untuk mempermudah administrasi dan analisis materi.")

materi = st.text_area("Masukkan Materi/Teks Buku di Sini:", height=200)

if st.button("🚀 PROSES SEKARANG"):
    if materi:
        with st.spinner("Sedang menganalisis..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Anda adalah Pakar PPKn. Buatkan {jumlah} {tipe} level {level} untuk {fase} berdasarkan materi ini: {materi}"
            response = model.generate_content(prompt)
            st.success("Selesai!")
            st.markdown(response.text)
    else:
        st.warning("Isi materinya dulu ya!")
