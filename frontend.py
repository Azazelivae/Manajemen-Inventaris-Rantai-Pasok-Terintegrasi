import streamlit as st
from src.graph_search import astar
from src.forecasting import simple_exponential_smoothing

st.title("🚛 Optimasi Distribusi Rantai Pasok")

# Form Input
with st.form("routing_form"):
    gudang = st.selectbox("Pilih Gudang:", ["Gudang_Ngamprah"])
    gerai = st.selectbox("Pilih Gerai:", ["Gerai_Lembang", "Gerai_Batujajar", "Gerai_Gununghalu"])
    submitted = st.form_submit_button("Hitung Rute")

if submitted:
    with st.spinner("AI sedang memproses..."):
        try:
            # Memanggil fungsi langsung (Tanpa HTTP Request)
            result = astar(gudang, gerai)
            
            if result:
                st.success("Berhasil!")
                st.write(f"**Jalur:** {' ➔ '.join(result['path'])}")
                st.write(f"**Biaya/Jarak:** {result['cost']} km")
            else:
                st.error("Rute tidak ditemukan!")
        except Exception as e:
            st.error(f"Error: {e}")
