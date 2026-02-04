# 🌧️ Dashboard Analisis Cuaca & Curah Hujan Kota Bandung

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Repository ini berisi *source code* untuk **Tugas Besar Pemrograman Dasar Sains Data**. Aplikasi ini dikembangkan sebagai dashboard interaktif untuk menganalisis pola curah hujan, kecepatan angin, dan suhu di Kota Bandung menggunakan data historis.

---

## 🔗 Akses Aplikasi
Aplikasi sudah di-deploy dan dapat diakses secara *online* melalui tautan berikut:

[![](https://img.shields.io/badge/👉_Buka_Dashboard_di_Sini-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://dashboardhujankotabandung.streamlit.app)

---

## 📋 Fitur Utama

Dashboard ini dirancang untuk memudahkan pemantauan dan analisis cuaca dengan fitur:

1.  **Ringkasan Statistik (KPI)**: Menampilkan rata-rata curah hujan, suhu, kecepatan angin, serta nilai ekstrem (tertinggi/terendah).
2.  **Grafik Tren Interaktif**:
    * 📊 **Bar Chart**: Visualisasi intensitas dan curah hujan.
    * 📈 **Area Chart**: Visualisasi fluktuasi kecepatan angin dan suhu.
3.  **Analisis Distribusi**: Grafik batang horizontal untuk melihat frekuensi kategori hujan (Ringan, Sedang, Lebat, dll).
4.  **Peta GIS Interaktif (Folium)**: Peta lokasi stasiun pengamatan dengan radius visual dan *popup* informasi status cuaca (Aman/Waspada).
5.  **Filter Data Dinamis**:
    * Mode **Per-Tahun**: Analisis cepat satu tahun penuh.
    * Mode **Kustom**: Analisis rentang tanggal spesifik.
6.  **Tabel Data Mentah**: Fitur untuk melihat data asli yang digunakan dalam visualisasi.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman**: Python 3.x
* **Framework Web**: [Streamlit](https://streamlit.io/)
* **Pengolahan Data**: Pandas, OpenPyXL
* **Visualisasi Grafik**: Plotly Express
* **Peta & GIS**: Folium, Streamlit-Folium

---

## 📂 Struktur File

* `app_visualisasi...py`: File utama kode program Python (Script Aplikasi).
* `curah_hujan_bandung.xlsx`: Dataset sumber (Excel).
* `style.css`: File CSS untuk kustomisasi tampilan antarmuka (*Custom UI*).
* `requirements.txt`: Daftar dependensi library untuk proses deployment.

---

## 🚀 Cara Menjalankan di Lokal (Localhost)

Jika ingin menjalankan aplikasi ini di komputer sendiri tanpa internet:

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/faldel/Tubes.git](https://github.com/faldel/Tubes.git)
    ```
2.  **Masuk ke direktori project:**
    ```bash
    cd Tubes
    ```
3.  **Install library yang dibutuhkan:**
    Pastikan Python sudah terinstall, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Jalankan aplikasi:**
    ```bash
    streamlit run "NAMA_FILE_PYTHON_KAMU.py"
    ```
    *(Catatan: Ganti `NAMA_FILE_PYTHON_KAMU.py` dengan nama file python yang ada di folder)*

---

## 📅 Sumber Data

Data yang digunakan dalam visualisasi ini bersumber dari:
* **Open-Meteo** (Historical Weather Data API).
* Data mencakup parameter: Tanggal, Curah Hujan, Suhu, dan Kecepatan Angin.

---

## 👥 Identitas Pembuat

**Tugas Besar Visualisasi Data - Kelompok 3**
**Universitas Komputer Indonesia (UNIKOM)**

**Anggota Tim:**
1. ZAGAR BAYU KUSUMA
2. ASEP SAIPUL
3. MUHAMMAD FAIZ RIZQULLAH
4. MOHAMAD RIFALDY FIRDAUS
5. NAZLA MUFIDAH

---
