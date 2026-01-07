import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- KULLANICI GİRİŞ AYARLARI ---
# Buradaki kullanıcı adı ve şifreyi kendine göre değiştirebilirsin
USER_LOGIN = "admin"
USER_PASS = "enerji123"

st.set_page_config(page_title="HES/GES Yönetim Paneli", layout="wide")

# --- GİRİŞ KONTROLÜ ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 Santral Yönetim Girişi")
    user = st.text_input("Kullanıcı Adı")
    pw = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if user == USER_LOGIN and pw == USER_PASS:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")

if not st.session_state["authenticated"]:
    login()
else:
    # --- ANA PANEL ---
    st.sidebar.title("🛠️ Veri Giriş Ekranı")
    st.sidebar.write(f"Hoş geldin, **{USER_LOGIN}**")
    
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("☀️ GES & 💧 HES Veri Takip Sistemi")

    # 1. MANUEL VERİ GİRİŞİ (SOL MENÜ)
    with st.sidebar.form("veri_formu"):
        tarih = st.date_input("Analiz Tarihi", datetime.now())
        st.write("---")
        st.subheader("İnvertör Verileri")
        inv_kwh = st.number_input("İnvertör Toplam (kWh)", min_value=0.0)
        
        st.subheader("Sayaç Verileri")
        sayac_kwh = st.number_input("Resmi Sayaç (kWh)", min_value=0.0)
        
        submit = st.form_submit_button("Sisteme İşle ve Kaydet")

    # 2. HESAPLAMA VE GÖSTERİM
    if inv_kwh > 0 and sayac_kwh > 0:
        fark = inv_kwh - sayac_kwh
        kayip_orani = (fark / inv_kwh) * 100

        # Üst Özet Kartları
        c1, c2, c3 = st.columns(3)
        c1.metric("İnvertör Toplam", f"{inv_kwh} kWh")
        c2.metric("Sayaç Toplam", f"{sayac_kwh} kWh")
        c3.metric("Fark / Kayıp", f"%{round(kayip_orani, 2)}", delta=f"{round(fark, 1)} kWh", delta_color="inverse")

        # Karşılaştırma Grafiği
        fig = go.Figure(data=[
            go.Bar(name='İnvertör', x=['Üretim Kıyaslama'], y=[inv_kwh], marker_color='#FFA500'),
            go.Bar(name='Sayaç', x=['Üretim Kıyaslama'], y=[sayac_kwh], marker_color='#1E90FF')
        ])
        fig.update_layout(barmode='group', height=450)
        st.plotly_chart(fig, use_container_width=True)

        # Durum Analizi
        if kayip_orani > 5:
            st.warning(f"⚠️ Kayıp Oranı Yüksek! (%{round(kayip_orani, 2)}) Sayaç veya kablo bağlantılarını kontrol edin.")
        else:
            st.success("✅ Veriler Tutarlı. Kayıp oranı normal sınırlar içerisinde.")
    else:
        st.info("👈 Lütfen sol menüden güncel sayaç ve invertör değerlerini girerek 'Sisteme İşle' butonuna basın.")

    # Alt Bilgi
    st.divider()
    st.caption(f"Veri Giriş Saati: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
