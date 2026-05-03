import streamlit as st
import google.generativeai as genai

# Konfigurasi API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key belum disetting di Secrets!")

# Gunakan model yang paling stabil
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.title("Pembuat Soal PPKn Otomatis")
st.write("Masukkan materi, lalu AI akan membuatkan soal untukmu.")

materi = st.text_area("Tempel Materi Di Sini:", height=200)
jumlah = st.slider("Jumlah Soal:", 1, 10, 5)

if st.button("BUAT SOAL SEKARANG"):
    if materi:
        with st.spinner("Sedang meramu soal..."):
            prompt = f"Anda adalah Pakar PPKn. Buatlah {jumlah} soal pilihan ganda berdasarkan materi ini: {materi}. Berikan kunci jawabannya juga."
            response = model.generate_content(prompt)
            st.success("Selesai!")
            st.write(response.text)
    else:
        st.warning("Isi dulu materinya, Bro!")
