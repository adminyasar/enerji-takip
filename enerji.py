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
        st.header(f
