import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- PANEL AYARLARI ---
st.set_page_config(page_title="Enerji Otomasyon Paneli", layout="wide")

# --- SOL MENÜ (NAVİGASYON) ---
st.sidebar.title("🚀 Enerji Yönetim Merkezi")
menu = st.sidebar.radio("Giriş Panelleri", ["📊 Ana Dashboard", "📟 OSOS Sayaç Girişi", "🔌 Inverter Giriş Ekranı", "⚙️ Ayarlar"])

# --- 1. OSOS GİRİŞ EKRANI ---
if menu == "📟 OSOS Sayaç Girişi":
    st.header("OSOS Otomatik Sayaç Bağlantısı")
    st.info("Resmi sayaç verilerini çekmek için OSOS kullanıcı bilgilerinizi giriniz.")
    
    with st.form("osos_form"):
        kullanici = st.text_input("OSOS Kullanıcı Adı")
        sifre = st.text_input("OSOS Şifre", type="password")
        sayac_no = st.text_input("Sayaç Seri No")
        bağlan = st.form_submit_button("OSOS Sistemine Bağlan")
        
        if bağlan:
            st.warning("OSOS Sistemine bağlantı isteği gönderildi... (API onayı bekleniyor)")

# --- 2. INVERTER GİRİŞ EKRANI ---
elif menu == "🔌 Inverter Giriş Ekranı":
    st.header("Sungrow iSolarCloud Entegrasyonu")
    st.info("İnverter üretim verilerini saatlik çekmek için API bilgilerini giriniz.")
    
    with st.form("inverter_form"):
        api_user = st.text_input("Sungrow Kullanıcı Adı")
        api_pass = st.text_input("Sungrow Şifre", type="password")
        plant_id = st.text_input("Santral (Plant) ID")
        guncelleme_sikligi = st.selectbox("Veri Çekme Sıklığı", ["1 Saatlik", "15 Dakikalık", "Günlük"])
        
        kaydet = st.form_submit_button("API Bağlantısını Doğrula")
        
        if kaydet:
            st.success(f"Sungrow Santral ID {plant_id} başarıyla tanımlandı.")

# --- 3. ANA DASHBOARD (OTOMATİK VERİ GÖSTERİMİ) ---
elif menu == "📊 Ana Dashboard":
    st.title("Gerçek Zamanlı Üretim & Sayaç Analizi")
    
    # Otomatik Veri Çekme Butonu
    if st.button("🔄 Verileri Şimdi Güncelle"):
        with st.spinner('OSOS ve Sungrow verileri senkronize ediliyor...'):
            time.sleep(2) # Simülasyon
            st.success("Saatlik veriler başarıyla güncellendi!")

    # Örnek Grafik ve Karşılaştırma
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Saatlik Üretim Grafiği")
        # Örnek saatlik veri
        saatler = [f"{i}:00" for i in range(8, 18)]
        uretim = [10, 50, 150, 400, 650, 800, 750, 450, 200, 50]
        fig = go.Figure(data=[go.Scatter(x=saatler, y=uretim, mode='lines+markers', name='Üretim (kWh)')])
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Sayaç vs Inverter Farkı")
        # Örnek fark grafiği
        fig2 = go.Figure(data=[
            go.Bar(name='Inverter', x=['Toplam'], y=[4500]),
            go.Bar(name='Sayaç', x=['Toplam'], y=[4410])
        ])
        st.plotly_chart(fig2, use_container_width=True)

# --- 4. AYARLAR ---
elif menu == "⚙️ Ayarlar":
    st.header("Sistem Ayarları")
    st.write("E-posta Bildirimleri")
    st.checkbox("Veri farkı %5'i geçerse SMS gönder")
    st.checkbox("Gün sonu raporunu PDF olarak mail at")
