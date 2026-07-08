**Manajemen Inventaris & Optimasi Rantai Pasok KDMP**

Sistem cerdas untuk mengoptimalkan rute distribusi sembako dari Gudang Pusat KDMP ke gerai-gerai tingkat kecamatan di Kabupaten Bandung Barat, meminimalkan biaya transportasi melalui pendekatan Informed Search (Algoritma A*).
Architecture Diagram
Sistem ini mengintegrasikan pemodelan stok berbasis waktu dengan optimasi pencarian rute berbasis koordinat geografis.

**Alur Kerja:**
Forecasting Layer: Menganalisis tingkat stok dan memprediksi kebutuhan restock.
Graph Processing: Memetakan koordinat lat-long ke dalam struktur graf.
A Search Engine:* Menghitung jalur optimal menggunakan fungsi heuristik.
API Layer: Menyajikan rute terbaik untuk tim logistik lapangan.
Setup Guide

**Prasyarat**
Python 3.10 atau lebih tinggi
pip untuk manajemen paket.

**Langkah Instalasi**
Clone repositori:
Bash
git clone https://github.com/Azazelivae/Manajemen-Inventaris-Rantai-Pasok-Terintegrasi.git
cd Manajemen-Inventaris-Rantai-Pasok-Terintegrasi

**Install dependensi:**
Bash
pip install -r requirements.txt


Jalankan Aplikasi:
Bash
python app.py


**API Documentation**
POST /api/v1/optimize-route
Menghitung rute optimal dari gudang ke titik gerai yang memiliki stok kritis.
Request



JSON
{
  "warehouse_id": "GUDANG_NGAMPRAH",
  "target_outlets": ["GERAI_CISARUA", "GERAI_PARONGPONG"],
  "heuristic_type": "euclidean"
}


Response (200 OK)



JSON
{
  "status": "success",
  "data": {
    "route": ["GUDANG_NGAMPRAH", "GERAI_CISARUA", "GERAI_PARONGPONG"],
    "total_distance_km": 12.5,
    "execution_time_ms": 45
  }
}


Response (400 Bad Request)



JSON
{
  "status": "error",
  "message": "Koordinat gerai tidak ditemukan dalam database graf."
}


**Pemahaman Konsep (Ringkasan Teknis)**
Heuristik: Kami membandingkan Euclidean vs Haversine. Hasil riset menunjukkan bahwa untuk skala lokal, Euclidean memberikan sweet spot antara performa komputasi dan akurasi rute.
Admissible & Consistent: Algoritma kami menjamin jalur terpendek karena fungsi heuristik yang digunakan tidak pernah melebih-lebihkan jarak nyata (admissible) dan memenuhi aturan triangle inequality (consistent).
