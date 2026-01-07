import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- PANEL YAPILANDIRMASI ---
st.set_page_config(page_title="Enerji Portföy Yönetimi", layout="wide")

# --- SOL MENÜ: SANTRAL VE MOD SEÇİMİ ---
st.sidebar.title("🏢 Santral Yönetimi")

# 1. Adım: Hangi Santral?
santral_turu = st.sidebar.selectbox("Santral Türü", ["Güneş Enerjisi (GES)", "Hidroelektrik (HES)"])

if santral_turu == "Güneş Enerjisi (GES)":
    secilen_santral = st.sidebar.selectbox("Santral Seçin", ["GES-1 (Merkez)", "GES-2 (Saha)", "Yeni GES Ekle+"])
else:
    secilen_santral = st.sidebar.selectbox("Santral Seçin", ["HES-1 (Baraj)", "HES-2 (Regülatör)"])

st.sidebar.divider()

# 2. Adım: Hangi İşlem?
menu = st.sidebar.radio(
    f"📍 {secilen_santral} Menüsü", 
    ["📊 Genel Dashboard", "📟 OSOS Sayaç Ayarları", "🔌 Inverter/Türbin Bağlantısı", "📝 Manuel Veri Girişi"]
)

# --- 1. OSOS SAYAÇ AYARLARI ---
if menu == "📟 OSOS Sayaç Ayarları":
    st.header(f"📟 {secilen_santral} - OSOS Bağlantı Ayarları")
    st.info(f"Bu bölümdeki ayarlar sadece **{secilen_santral}** sayacını etkiler.")
    
    with st.form("osos_config"):
        col1, col2 = st.columns(2)
        with col1:
            osos_kullanici = st.text_input("OSOS Kullanıcı Adı")
            osos_sifre = st.text_input("OSOS Şifre", type="password")
        with col2:
            sayac_no = st.text_input("Sayaç Seri No / ID")
            api_endpoint = st.text_input("OSOS Servis Adresi (URL)")
        
        test_et = st.form_submit_button("Bağlantıyı Test Et")
        if test_et:
            st.warning(f"{secilen_santral} OSOS sistemi sorgulanıyor...")

# --- 2. INVERTER / TÜRBİN BAĞLANTISI ---
elif menu == "🔌 Inverter/Türbin Bağlantısı":
    if "GES" in santral_turu:
        st.header(f"🔌 {secilen_santral} - Sungrow Inverter API")
        with st.form("ges_api"):
            st.text_input("iSolarCloud AppKey")
            st.text_input("Plant ID (Santral No)")
            st.form_submit_button("GES Verilerini Senkronize Et")
    else:
        st.header(f"🌀 {secilen_santral} - Türbin & SCADA Bağlantısı")
        with st.form("hes_api"):
            st.text_input("HES SCADA IP Adresi")
            st.text_input("Türbin Modbus ID")
            st.form_submit_button("HES Verilerini Senkronize Et")

# --- 3. ANA DASHBOARD ---
elif menu == "📊 Genel Dashboard":
    st.title(f"📈 {secilen_santral} - Performans Paneli")
    
    # Üretim Özet Kartları
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Anlık Üretim", "450 kW", "+12 kW")
    c2.metric("Günlük Toplam", "3.2 MWh", "0.4 MWh")
    c3.metric("OSOS Sayaç", "3.15 MWh")
    c4.metric("Sistem Kaybı", "%1.5", "-0.2%", delta_color="normal")

    # Saatlik Karşılaştırma Grafiği
    st.subheader("Saatlik OSOS vs Inverter Kıyaslaması")
    saatler = [f"{i}:00" for i in range(24)]
    # Örnek veri
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=saatler, y=[0,0,0,0,0,10,100,300,500,700,850,900,880,700,400,150,20,0,0,0,0,0,0,0], 
                             name="Inverter (Otomatik)", line=dict(color='orange', width=3)))
    fig.add_trace(go.Scatter(x=saatler, y=[0,0,0,0,0,8,95,280,480,680,830,880,860,680,380,140,15,0,0,0,0,0,0,0], 
                             name="OSOS (Sayaç)", line=dict(color='blue', dash='dash')))
    
    st.plotly_chart(fig, use_container_width=True)

# --- 4. MANUEL VERİ GİRİŞİ ---
elif menu == "📝 Manuel Veri Girişi":
    st.header(f"📝 {secilen_santral} - Manuel Veri Düzenleme")
    st.write("Otomatik verilerin gelmediği durumlarda burayı kullanın.")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Tarih")
        st.number_input("Manuel İnverter Girişi (kWh)")
    with col2:
        st.time_input("Saat")
        st.number_input("Manuel Sayaç Girişi (kWh)")
    st.button("Veriyi Sisteme İşle")
