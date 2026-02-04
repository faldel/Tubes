import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from datetime import date
from folium.plugins import Fullscreen

# ==========================================
# FITUR 1: PENGATURAN TAMPILAN
# Mengatur judul web, ikon, warna tema, dan lokasi stasiun.
# ==========================================
st.set_page_config(page_title="Dashboard Hujan Kota Bandung", page_icon="🌧️", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ File '{file_name}' tidak ditemukan.")

local_css("style.css") 
COLORS = {
    'hujan': '#3498db', 'angin': '#2ecc71', 'suhu': '#ff4b4b',
    'intensitas': {
        'Tidak Hujan': '#b2bec3', 'Ringan': '#62DF77', 'Sedang': '#00cec9', 
        'Lebat': '#0984e3', 'Sangat Lebat': '#6c5ce7'
    }
}

STATION_COORDS = [-6.9175, 107.6025]
BULAN_MAP = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}

# ==========================================
# FITUR 2: AMBIL DATA
# Proses membaca file Excel dan merapikan format tanggal agar siap diolah.
# ==========================================
@st.cache_data 
def load_data():
    try:
        df = pd.read_excel('curah_hujan_bandung.xlsx')
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def format_indo(tgl):
    return f"{tgl.day} {BULAN_MAP[tgl.month]} {tgl.year}"

df = load_data()
if df.empty:
    st.error("⚠️ File data tidak ditemukan."); st.stop()

MAX_HUJAN = df['Curah Hujan (mm)'].max() * 1.2
MAX_ANGIN = 50 
MAX_SUHU = 50 

# ==========================================
# FITUR 3: MENU FILTER
# Membuat menu di samping (sidebar) untuk memilih tahun atau tanggal tertentu.
# ==========================================
with st.sidebar:
    st.write("") 
    with st.container(border=True):
        st.write("### 📅 Pengaturan Waktu")
        mode_filter = st.radio("Mode Filter:", ["Per-Tahun", "Kustomisasi"], horizontal=False)
        
        if mode_filter == "Per-Tahun":
            available_years = sorted(df['Tanggal'].dt.year.unique())
            pilihan_tahun = st.selectbox("Pilih Tahun:", available_years, index=len(available_years)-1)
            start_date, end_date = pd.Timestamp(f"{pilihan_tahun}-01-01"), pd.Timestamp(f"{pilihan_tahun}-12-31")
            note_text = f"Tahun {pilihan_tahun}"
        else:
            batas_min, batas_max = df['Tanggal'].min().date(), df['Tanggal'].max().date()
            input_start = st.date_input("Mulai Tanggal:", value=batas_min, min_value=batas_min, max_value=batas_max)
            input_end = st.date_input("Sampai Tanggal:", value=batas_max, min_value=batas_min, max_value=batas_max)
            if input_start > input_end: st.error("Rentang Tanggal Salah"); st.stop()
            start_date, end_date = pd.Timestamp(input_start), pd.Timestamp(input_end)
            note_text = f"{format_indo(input_start)} - {format_indo(input_end)}"

    st.write("")
    with st.container(border=True):
        st.write("### ⚙️ View Options")
        show_map = st.toggle("Tampilkan Peta GIS", value=True)

filtered_df = df[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]

# ==========================================
# FITUR 4: RINGKASAN DATA (ANGKA UTAMA)
# Menampilkan rata-rata dan nilai tertinggi dalam bentuk kotak informasi.
# ==========================================
st.title("🌧️ Dashboard Hujan Kota Bandung")
st.markdown(f'<div class="title-badge">📅 Periode Analisis: {note_text}</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
metrics_config = [
    ("Rata-rata Curah Hujan", filtered_df['Curah Hujan (mm)'].mean(), "mm", COLORS['hujan'], m1),
    ("Curah Hujan Tertinggi", filtered_df['Curah Hujan (mm)'].max(), "mm", COLORS['hujan'], m2),
    ("Rata-rata Kecepatan Angin", filtered_df['Kecepatan Angin (km/h)'].mean(), "km/h", COLORS['angin'], m3),
    ("Suhu Rata-rata", filtered_df['Suhu rata-rata (°C)'].mean(), "°C", COLORS['suhu'], m4)
]

for label, val, unit, color, col in metrics_config:
    display_val = f"{val:.1f}" if pd.notnull(val) else "0.0"
    col.markdown(f'''
        <div class="metric-container" style="border-left: 5px solid {color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {color};">{display_val} {unit}</div>
        </div>
    ''', unsafe_allow_html=True)

# ==========================================
# FITUR 5: GRAFIK INTERAKTIF
# Visualisasi tren hujan, angin, dan suhu menggunakan tab agar lebih rapih.
# ==========================================
def make_plotly_chart(data, y_col, color_hex, chart_type='bar', y_max=None):
    if data.empty: return px.bar()
    
    clean_labels = {y_col: y_col.replace('rata-rata', '')}

    if chart_type == 'bar':
        fig = px.bar(data, x='Tanggal', y=y_col, template='plotly_dark', hover_data={'Tanggal': False}, labels=clean_labels)
        fig.update_traces(marker_color=color_hex, marker_line_width=0, opacity=0.9)
    else:
        fig = px.area(data, x='Tanggal', y=y_col, template='plotly_dark', hover_data={'Tanggal': False}, labels=clean_labels)
        c = color_hex.lstrip('#')
        r, g, b = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        fig.update_traces(line_color=color_hex, fillcolor=f"rgba({r},{g},{b},0.2)")

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(t=20, l=0, r=0, b=0), 
        hovermode="x unified",
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', showline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', showline=False, zeroline=False, range=[0, y_max])
    )
    return fig

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌧️ Tren Hujan", "💨 Tren Angin", "🌡️ Tren Suhu", "📊 Distribusi", "📂 Data Mentah"])

with tab1: st.plotly_chart(make_plotly_chart(filtered_df, 'Curah Hujan (mm)', COLORS['hujan'], 'bar', MAX_HUJAN), use_container_width=True)
with tab2: st.plotly_chart(make_plotly_chart(filtered_df, 'Kecepatan Angin (km/h)', COLORS['angin'], 'area', MAX_ANGIN), use_container_width=True)
with tab3: st.plotly_chart(make_plotly_chart(filtered_df, 'Suhu rata-rata (°C)', COLORS['suhu'], 'area', MAX_SUHU), use_container_width=True)
with tab4:
    if not filtered_df.empty:
        cnt = filtered_df['Intensitas'].value_counts().reset_index()
        cnt.columns = ['Intensitas', 'Total Hari']
        fig_dist = px.bar(cnt, x='Total Hari', y='Intensitas', orientation='h', color='Intensitas', color_discrete_map=COLORS['intensitas'], template='plotly_dark')
        fig_dist.update_traces(marker_opacity=0.7)
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', showline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', showline=False)
        )
        st.plotly_chart(fig_dist, use_container_width=True)
with tab5:
    df_display = filtered_df.copy(); df_display['Tanggal'] = df_display['Tanggal'].dt.date
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# ==========================================
# FITUR 6: PETA DIGITAL (GIS)
# Menampilkan lokasi stasiun di peta Bandung dengan indikator status cuaca.
# ==========================================
if show_map:
    st.markdown("---")
    
    total_hujan = filtered_df['Curah Hujan (mm)'].sum()
    total_hari, angin_min, angin_max = len(filtered_df), filtered_df['Kecepatan Angin (km/h)'].min(), filtered_df['Kecepatan Angin (km/h)'].max()
    
    suhu_min = filtered_df['Suhu rata-rata (°C)'].min()
    suhu_max = filtered_df['Suhu rata-rata (°C)'].max()
    suhu_display = f"{suhu_min:.1f} - {suhu_max:.1f}" if not filtered_df.empty else "0.0 - 0.0"

    if total_hujan > 200: status_text, warna_marker = "Curah Hujan Tinggi", "red"
    elif total_hujan > 50: status_text, warna_marker = "Curah Hujan Sedang", "orange"
    else: status_text, warna_marker = "Curah Hujan Rendah", "green"
    st.markdown('<div class="title-badge">📍 Analisis Lokasi & Radius Data</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        m = folium.Map(location=STATION_COORDS, zoom_start=12, tiles='CartoDB dark_matter')
        Fullscreen(position='topright', title='Perbesar', title_cancel='Keluar').add_to(m)
        folium.Circle(location=STATION_COORDS, radius=5000, color=warna_marker, fill=True, fill_color=warna_marker, fill_opacity=0.15, tooltip=f"Status: {status_text}").add_to(m)
        
        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; width: 420px; color: #333; line-height: 1.5;">
            <div style="background-color: #26293a; color: white; padding: 12px 15px; border-radius: 8px 8px 0 0; border-bottom: 3px solid {warna_marker};">
                <h5 style="margin: 0; font-size: 15px;">📍 Stasiun Geofisika Bandung</h5>
            </div>
            <div style="padding: 15px; background-color: white; border-radius: 0 0 8px 8px;">
                <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #f2f2f2;">
                        <td style="padding: 6px 0; width: 140px;"><b>Periode</b></td><td style="width: 10px;">:</td><td style="text-align: right;">{note_text}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f2f2f2;">
                        <td style="padding: 6px 0;"><b>Total Curah Hujan</b></td><td>:</td><td style="text-align: right;">{total_hujan:.1f} mm</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f2f2f2;">
                        <td style="padding: 6px 0;"><b>Angin Min/Max</b></td><td>:</td><td style="text-align: right;">{angin_min:.1f} - {angin_max:.1f} km/h</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f2f2f2;">
                        <td style="padding: 6px 0;"><b>Suhu Min/Max</b></td><td>:</td><td style="text-align: right;">{suhu_display} °C</td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0;"><b>Total Hari</b></td><td>:</td><td style="text-align: right;">{total_hari} Hari</td>
                    </tr>
                </table>
                <div style="margin-top: 10px; padding: 6px; background: {warna_marker}; color: white; text-align: center; border-radius: 4px; font-size: 11px; font-weight: bold;">
                    {status_text.upper()}
                </div>
            </div>
        </div>
        """
        
        folium.Marker(STATION_COORDS, popup=folium.Popup(popup_html, max_width=450), icon=folium.Icon(color=warna_marker, icon="info-sign")).add_to(m)
        st_folium(m, height=550, use_container_width=True)