import requests
import pandas as pd

def kategori_intensitas_curah_hujan(curah_hujan):
    """
    Kategori:
    - Tanpa Hujan: 0 mm
    - Ringan: 0.1 - 10 mm
    - Sedang: 10.1 - 20 mm
    - Lebat: 20.1 - 50 mm
    - Sangat Lebat: > 50 mm
    
    Args:
        curah_hujan: nilai curah hujan dalam mm
    
    Returns:
        kategori intensitas curah hujan
    """
    try:
        nilai = float(curah_hujan) if curah_hujan else 0
        
        if nilai == 0:
            return "Tidak Hujan"
        elif nilai <= 10:
            return "Ringan"
        elif nilai <= 20:
            return "Sedang"
        elif nilai <= 50:
            return "Lebat"
        else:
            return "Sangat Lebat"
    except:
        return "N/A"

def scrape_openmeteo_api():
    """Scraping data curah hujan dari Open-Meteo API dengan kategori intensitas"""
    
    print("=" * 70)
    print("SCRAPING DATA CURAH HUJAN BANDUNG DENGAN KATEGORI INTENSITAS")
    print("=" * 70)
    
    try:
        # Koordinat Bandung
        latitude = -6.9175
        longitude = 107.6025
        
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2023-01-01&end_date=2025-12-31&daily=precipitation_sum,temperature_2m_max,temperature_2m_min,wind_speed_10m_max&temperature_unit=celsius&wind_speed_unit=kmh&timezone=Asia/Jakarta"
        
        print(f"[INFO] Mengambil data dari Open-Meteo API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse data dengan kategori intensitas
        records = []
        for i, date in enumerate(data['daily']['time']):
            curah_hujan = data['daily']['precipitation_sum'][i]
            keceptan_angin = data['daily']['wind_speed_10m_max'][i]
            records.append({
                'Tanggal': date,
                'Curah Hujan (mm)': curah_hujan,
                'Kecepatan Angin (km/h)': keceptan_angin,
                'Intensitas': kategori_intensitas_curah_hujan(curah_hujan),
                'Suhu rata-rata (°C)': (data['daily']['temperature_2m_max'][i] + data['daily']['temperature_2m_min'][i]) / 2,
            })
        
        df = pd.DataFrame(records)
        
        # Simpan ke Excel
        df.to_excel('curah_hujan_bandung.xlsx', index=False, sheet_name='Data Curah Hujan')
        
        print(f"\n[SUKSES] Data berhasil diunduh: {len(records)} records")
        print(f"[SUKSES] File tersimpan: curah_hujan_bandung.xlsx")
        
        # Tampilkan preview data
        print("\n" + "=" * 70)
        print("PREVIEW DATA (10 baris pertama):")
        print("=" * 70)
        print(df.head(10).to_string())
        
        # Tampilkan statistik intensitas
        print("\n" + "=" * 70)
        print("STATISTIK INTENSITAS CURAH HUJAN:")
        print("=" * 70)
        intensitas_counts = df['Intensitas'].value_counts().sort_index()
        print(intensitas_counts)
        
        print("\n" + "=" * 70)
        print("RINGKASAN STATISTIK:")
        print("=" * 70)
        print(f"Total hari: {len(df)}")
        print(f"Total curah hujan: {df['Curah Hujan (mm)'].sum():.2f} mm")
        print(f"Rata-rata curah hujan: {df['Curah Hujan (mm)'].mean():.2f} mm")
        print(f"Suhu rata-rata: {df['Suhu rata-rata (°C)'].mean():.2f} °C")
        print(f"Rata-rata kecepatan angin: {df['Kecepatan Angin (km/h)'].mean():.2f} km/h")
        
        return df
        
    except Exception as e:
        print(f"[ERROR] Gagal mengunduh data: {e}")
        return None

# ========== MAIN PROGRAM ==========
if __name__ == "__main__":
    print("\n" + "[START] Memulai proses scraping...\n")
    
    result = scrape_openmeteo_api()
    
    print("\n" + "=" * 70)
    print("[SELESAI] Scraping selesai!")
    print("=" * 70)
    
    if result is not None:
        print("\n[INFO] File Excel telah dibuat dengan kolom:")
        print("  - Tanggal")
        print("  - Curah Hujan (mm)")
        print("  - Kecepatan Angin (km/h)")
        print("  - Intensitas (Tanpa Hujan / Ringan / Sedang / Lebat / Sangat Lebat)")
        print("  - Suhu rata-rata (°C)")
