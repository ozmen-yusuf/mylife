import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os

# Sayfa Ayarları
st.set_page_config(page_title="Kişisel Yaşam & Performans Paneli", page_icon="⚡", layout="centered")

DATA_FILE = "kisisel_veriler.csv"

def veri_yukle():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "Tarih" in df.columns:
            df["Tarih"] = pd.to_datetime(df["Tarih"]).dt.date
        return df
    else:
        return pd.DataFrame(columns=["Tarih", "Modul", "Detay_1", "Detay_2", "Deger", "Notlar"])

df = veri_yukle()

# --- STREAK (SERİ) HESAPLAMA MANTIĞI ---
def streak_hesapla(veri_df):
    if veri_df.empty:
        return 0
    benzersiz_tarihler = sorted(veri_df["Tarih"].unique(), reverse=True)
    bugun = date.today()
    
    en_yakin = benzersiz_tarihler[0]
    if en_yakin < bugun - timedelta(days=1):
        return 0
        
    streak = 0
    beklenen_tarih = en_yakin
    for t in benzersiz_tarihler:
        if t == beklenen_tarih:
            streak += 1
            beklenen_tarih -= timedelta(days=1)
        else:
            break
    return streak

aktif_streak = streak_hesapla(df)

# Başlık ve Streak Göstergesi
col_baslik, col_streak = st.columns([3, 1])
with col_baslik:
    st.title("⚡ Yaşam & Performans Paneli")
with col_streak:
    st.markdown(f"<h3 style='text-align: right; color: #FF4B4B;'>🔥 {aktif_streak} Gün</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right; font-size: 12px; color: gray;'>Aktif Seri (Streak)</p>", unsafe_allow_html=True)

st.markdown("---")

# Sekmeler
sekme1, sekme2, sekme3, sekme4, sekme5, sekme6, sekme7, sekme8, sekme9 = st.tabs([
    "🏠 Özet & Hızlı", "➕ Akıllı Ekle", "💰 Finans", "😴 Uyku", 
    "🧠 Ruh Hali", "🏋️ Spor", "💧 Su", "📱 Ekran", "📋 Veri Yönetimi"
])

# --- 1. SEKME: ANA ÖZET & HIZLI BUTONLAR ---
with sekme1:
    st.subheader("🎯 Günlük Durum ve Hızlı Ekleme")
    
    # Hızlı Butonlar (Tek tıkla kayıt)
    st.markdown("#### ⚡ Tek Tıkla Hızlı Kayıtlar")
    col_h1, col_h2, col_h3 = st.columns(3)
    
    bugun_tarih = date.today()
    
    with col_h1:
        if st.button("💧 +0.5 Litre Su İçtim"):
            yeni_hizli = pd.DataFrame([{"Tarih": bugun_tarih, "Modul": "Su Tüketimi", "Detay_1": "Günlük Su Takibi", "Detay_2": "-", "Deger": 0.5, "Notlar": "Hızlı su eklendi"}])
            df = pd.concat([df, yeni_hizli], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("0.5L su eklendi! 💧")
            st.rerun()
            
    with col_h3:
        if st.button("🏋️ Antrenman Tamamlandı"):
            yeni_hizli = pd.DataFrame([{"Tarih": bugun_tarih, "Modul": "Spor", "Detay_1": "Ağırlık / Fitness", "Detay_2": "Standart İdman", "Deger": 9.0, "Notlar": "Hızlı spor kaydı"}])
            df = pd.concat([df, yeni_hizli], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("İdman işlendi! 🔥")
            st.rerun()

    st.markdown("---")
    st.subheader("📊 Günlük Hedef Durumu")
    
    bugun_df = df[df["Tarih"] == bugun_tarih] if not df.empty else pd.DataFrame()
    
    if not bugun_df.empty:
        bugun_su = bugun_df[bugun_df["Modul"] == "Su Tüketimi"]["Deger"].sum()
        bugun_harcama = bugun_df[bugun_df["Modul"] == "Finans"]["Deger"].sum()
        bugun_uyku_seri = bugun_df[bugun_df["Modul"] == "Uyku"]
        bugun_uyku = bugun_uyku_seri["Deger"].values[0] if not bugun_uyku_seri.empty else 0
    else:
        bugun_su, bugun_harcama, bugun_uyku = 0.0, 0.0, 0.0

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Bugünkü Su", f"{bugun_su} L", "Hedef: 2.5 L")
    col_m2.metric("Bugünkü Harcama", f"{bugun_harcama:,.2f} TL")
    col_m3.metric("Uyku Süresi", f"{bugun_uyku} Saat")

    st.markdown("---")
    st.subheader("💡 Akıllı Analiz & İçgörüler")
    if len(df) > 5:
        uyku_veri = df[df["Modul"] == "Uyku"]
        ruh_veri = df[df["Modul"] == "Ruh Hali"]
        if not uyku_veri.empty and not ruh_veri.empty:
            ortalama_uyku_genel = uyku_veri["Deger"].mean()
            st.info(f"📈 **Sistem Notu:** Kayıtlarına göre ortalama uyku süren **{ortalama_uyku_genel:.1f} saat** seviyesinde seyrediyor.")
        else:
            st.info("Daha fazla veri girdikçe korelasyon önerileri belirecek.")
    else:
        st.info("Analizlerin aktifleşmesi için birkaç günlük daha veri girişi yapmalısın.")


# --- 2. SEKME: AKILLI VERİ GİRİŞİ ---
with sekme2:
    st.subheader("📝 Detaylı Akıllı Veri Girişi")
    
    tarih = st.date_input("Tarih", datetime.now())
    modul = st.selectbox("Hangi Alanı Kaydediyorsun?", [
        "Finans", "Uyku", "Ruh Hali", "Spor", 
        "Su Tüketimi", "Ekran Süresi", "Gelişim"
    ])
    
    st.markdown("---")
    
    detay_1, detay_2, deger = "-", "-", 0.0
    
    if modul == "Finans":
        st.markdown("### 💰 Finans Detayları")
        detay_1 = st.selectbox("Harcama Kategorisi", ["Market / Gıda", "Dışarıda Yemek", "Fatura", "Giyim", "Eğlence", "Diğer"])
        detay_2 = st.selectbox("Ödeme Yöntemi", ["Kredi Kartı", "Nakit", "IBAN / Havale"])
        deger = st.number_input("Tutar (TL)", min_value=0.0, step=10.0, format="%.2f")
    elif modul == "Uyku":
        st.markdown("### 😴 Uyku Detayları")
        detay_1 = st.selectbox("Uyku Kalitesi", ["Mükemmel", "İyi", "Orta", "Kötü"])
        detay_2 = "Normal Uyku"
        deger = st.number_input("Kaç Saat Uyudun?", min_value=0.0, max_value=24.0, value=7.5, step=0.5)
    elif modul == "Ruh Hali":
        st.markdown("### 🧠 Ruh Hali Detayları")
        detay_1 = st.selectbox("Genel Hissiyat", ["Enerjik & Motive", "Normal / Nötr", "Yorgun / Stresli", "Mutlu"])
        detay_2 = "-"
        deger = float(st.slider("Ruh Hali Skoru (1 = Kötü, 10 = Harika)", 1, 10, 7))
    elif modul == "Spor":
        st.markdown("### 🏋️ Spor Detayları")
        detay_1 = st.selectbox("Antrenman Türü", ["Ağırlık / Fitness", "Kardiyo", "Dinlenme Günü"])
        detay_2 = st.text_input("Çalışılan Bölge / Detay", placeholder="Örn: Göğüs - Kol")
        deger = float(st.slider("Antrenman Verimi / Yoğunluğu (1-10)", 1, 10, 8))
    elif modul == "Su Tüketimi":
        st.markdown("### 💧 Su Detayları")
        detay_1 = "Günlük Su Takibi"
        detay_2 = "-"
        deger = st.number_input("İçilen Su Miktarı (Litre)", min_value=0.0, max_value=10.0, value=2.5, step=0.25)
    elif modul == "Ekran Süresi":
        st.markdown("### 📱 Ekran Süresi Detayları")
        detay_1 = st.selectbox("Cihaz Ağırlığı", ["Telefon Ağırlıklı", "Bilgisayar / Kodlama", "Dengeli"])
        detay_2 = "-"
        deger = st.number_input("Toplam Ekran Süresi (Saat)", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
    elif modul == "Gelişim":
        st.markdown("### 📚 Gelişim Detayları")
        detay_1 = st.selectbox("Gelişim Türü", ["Kitap Okuma", "Kodlama / Yazılım", "Yabancı Dil / Kurs"])
        detay_2 = st.text_input("Ne Çalıştın / Hangi Kitap?", placeholder="Örn: Clean Code / Pandas")
        deger = st.number_input("Miktar (Kitap için Sayfa / Diğerleri için Dakika)", min_value=0.0, step=1.0)

    notlar = st.text_input("Ekstra Not / Açıklama", placeholder="Gününle ilgili ufak bir detay...")
    st.markdown("---")
    
    if st.button("Sisteme Kaydet 🚀", type="primary"):
        yeni_veri = pd.DataFrame([{
            "Tarih": tarih,
            "Modul": modul,
            "Detay_1": detay_1,
            "Detay_2": detay_2,
            "Deger": deger,
            "Notlar": notlar
        }])
        df = pd.concat([df, yeni_veri], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Başarıyla kaydedildi kanka! ({modul}) 🔥")
        st.rerun()

# --- ANALİZ SEKMELERİ ---
with sekme3:
    st.subheader("💰 Finans & Harcama Analizi")
    finans_df = df[df["Modul"] == "Finans"]
    if not finans_df.empty:
        toplam = finans_df["Deger"].sum()
        st.metric("Toplam Harcama", f"{toplam:,.2f} TL")
        st.bar_chart(finans_df.groupby("Detay_1")["Deger"].sum())
        st.dataframe(finans_df[["Tarih", "Detay_1", "Detay_2", "Deger", "Notlar"]], use_container_width=True)
    else:
        st.info("Finans kaydı yok.")

with sekme4:
    st.subheader("😴 Uyku Takibi")
    uyku_df = df[df["Modul"] == "Uyku"]
    if not uyku_df.empty:
        st.metric("Ortalama Uyku Süresi", f"{uyku_df['Deger'].mean():.1f} Saat")
        st.line_chart(uyku_df.set_index("Tarih")["Deger"])
    else:
        st.info("Uyku verisi yok.")

with sekme5:
    st.subheader("🧠 Ruh Hali Grafiği")
    ruh_df = df[df["Modul"] == "Ruh Hali"]
    if not ruh_df.empty:
        st.line_chart(ruh_df.set_index("Tarih")["Deger"])
    else:
        st.info("Ruh hali verisi yok.")

with sekme6:
    st.subheader("🏋️ Spor ve Antrenman Geçmişi")
    spor_df = df[df["Modul"] == "Spor"]
    if not spor_df.empty:
        st.dataframe(spor_df[["Tarih", "Detay_1", "Detay_2", "Deger", "Notlar"]], use_container_width=True)
    else:
        st.info("Spor kaydı yok.")

with sekme7:
    st.subheader("💧 Su Tüketimi")
    su_df = df[df["Modul"] == "Su Tüketimi"]
    if not su_df.empty:
        st.line_chart(su_df.set_index("Tarih")["Deger"])
    else:
        st.info("Su tüketim verisi yok.")

with sekme8:
    st.subheader("📱 Ekran Süresi Takibi")
    ekran_df = df[df["Modul"] == "Ekran Süresi"]
    if not ekran_df.empty:
        st.metric("Ortalama Günlük Ekran Süresi", f"{ekran_df['Deger'].mean():.1f} Saat")
        st.line_chart(ekran_df.set_index("Tarih")["Deger"])
    else:
        st.info("Ekran süresi verisi yok.")

# --- 9. SEKME: VERİ YÖNETİMİ & SİLME ---
with sekme9:
    st.subheader("📋 Veri Yönetimi & Hatalı Kayıtları Silme")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 🗑️ Kayıt Sil")
        silinecek_index = st.number_input("Silmek istediğin satırın index numarasını gir:", min_value=0, max_value=max(0, len(df)-1), step=1)
        
        if st.button("Seçili Kaydı Sil", type="primary"):
            df = df.drop(index=silinecek_index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Kayıt başarıyla silindi kanka!")
            st.rerun()
            
        st.markdown("---")
        st.download_button(
            label="📥 Tüm Verileri CSV Olarak İndir",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='kisisel_yasam_verileri.csv',
            mime='text/csv',
        )
    else:
        st.info("Yönetilebilecek kayıt bulunmuyor.")
