import streamlit as st
from src.graph_search import astar, NODES
import requests
import time

st.set_page_config(page_title="KDMP AI Supply Chain", layout="centered")

st.title("🚛 Optimasi Distribusi Rantai Pasok Terintegrasi")
st.markdown(r"Mengorkestrasikan *Forecasting (Exponential Smoothing)* dan *A\* Search* untuk menentukan rute prioritas.")

# Form Input
with st.form("routing_form"):
    # Filter dinamis untuk Gudang (semua yang diawali "Gudang_")
    daftar_gudang = [n for n in NODES if n.startswith("Gudang_")]
    gudang = st.selectbox("Pilih Gudang Awal:", daftar_gudang)
    
    mode = st.radio("Mode Penentuan Target:", ["Otomatis (AI Forecasting)", "Manual (Pilih Gerai)"])
    
    gerai = "AUTO"
    if mode == "Manual (Pilih Gerai)":
        # Filter dinamis untuk Gerai (semua kecuali gudang + dummy test)
        daftar_gerai = [n for n in NODES if n != "Gudang_Ngamprah"] + ["Gerai_Fiktif (Test Error)"]
        gerai = st.selectbox("Pilih Gerai Tujuan:", daftar_gerai)
        
    submitted = st.form_submit_button("Hitung Rute Optimal")

if submitted:
    # Siapkan Payload
    payload = {
        "gudang_awal": gudang,
        "gerai_tujuan": gerai if mode == "Manual (Pilih Gerai)" else "AUTO",
        "data_gerai": [
            {"gerai_name": "Gerai_Lembang", "current_stock": 35, "sales_history": [12, 10, 15, 11]},
            {"gerai_name": "Gerai_Batujajar", "current_stock": 90, "sales_history": [5, 6, 5, 8]},
        ]
    }
    
    # LOADING SPINNER (Sesuai Protokol)
    with st.spinner("AI sedang mengorkestrasikan prediksi stok dan menghitung Heuristik A*..."):
        time.sleep(1) # Simulasi network delay
        try:
            # Tembak ke FastAPI (Pastikan URL & port sesuai dengan Uvicorn Anda)
            url = "https://manajemen-inventaris-rantai-pasok-terintegrasi-production.up.railway.app/api/v1/distribute"
            res = requests.post(url, json=payload)
            data = res.json()
            
            if res.status_code == 200:
                st.success(data["message"])
                st.write(f"**Target Gerai (Kritis):** {data['data']['target_gerai']}")
                st.write(f"**Total Jarak Tempuh:** {data['data']['total_cost_km']} km")
                st.write(f"**Heuristik Optimal:** {data['data']['heuristic_used']}")
                
                # Visualisasi Rute Sederhana
                rute = " ➔ ".join(data['data']['route_path'])
                st.info(f"**Jalur:** {rute}")
                
            else:
                # HUMAN READABLE ERROR (Sesuai Protokol)
                st.error(f"⚠️ Gagal memproses rute. Alasan: {data['message']}")
                st.warning("Tips: Pastikan lokasi gudang atau gerai terdaftar di sistem.")
                
        except requests.exceptions.ConnectionError:
            st.error("Server API Backend mati atau belum dijalankan! Jalankan `uvicorn app:app --reload` di terminal.")
