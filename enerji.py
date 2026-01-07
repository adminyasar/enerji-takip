import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Panel Başlığı
st.set_page_config(page_title="HES/GES Takip", layout="wide")
st.title("☀️ Enerji Üretim & Sayaç Karşılaştırma")

# Yan Menü - Veri Girişi
st.sidebar.header("📊 Günlük Veri Girişi")
tarih = st.sidebar.date_input("Tarih Seç", datetime.now())
sungrow_kwh = st.sidebar.number_input("Sungrow Toplam Üretim (kWh)", min_value=0.0)
sayac_kwh = st.sidebar.number_input("Resmi Sayaç Verisi (kWh)", min_value=0.0)

# Kıyaslama ve Hesaplama
if sungrow_kwh > 0:
    fark = sungrow_kwh - sayac_kwh
    kayip_orani = (fark / sungrow_kwh) * 100

    # Özet Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("Sungrow", f"{sungrow_kwh} kWh")
    c2.metric("Sayaç", f"{sayac_kwh} kWh")
    c3.metric("Fark / Kayıp", f"%{round(kayip_orani, 2)}", delta=f"{round(fark, 1)} kWh", delta_color="inverse")

    # Grafik
    fig = go.Figure(data=[
        go.Bar(name='Inverter (Sungrow)', x=['Üretim'], y=[sungrow_kwh], marker_color='orange'),
        go.Bar(name='Resmi Sayaç', x=['Üretim'], y=[sayac_kwh], marker_color='blue')
    ])
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Uyarı Sistemi
    if kayip_orani > 5:
        st.error(f"🚨 UYARI: Kayıp %5'in üzerinde (%{round(kayip_orani, 2)})! Hattı kontrol edin.")
    else:
        st.success("✅ Veriler Normal: Kayıp oranı kabul edilebilir seviyede.")
else:
    st.info("Lütfen sol taraftan verileri girip Enter'a basın.")