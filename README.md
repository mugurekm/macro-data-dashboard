# macro-data-dashboard
FRED API ile Canlı Makroekonomik Veri Panosu
# 📈 Macroeconomic Data & Analytics Dashboard

FRED (Federal Reserve Economic Data) API'si üzerinden canlı çekilen zaman serisi verileri ile ABD ekonomisindeki enflasyon, politika faizi ve işsizlik dinamiklerini analiz eden interaktif bir veri analitiği panosu.

## 📌 Proje Hakkında
Bu proje, makroekonomik değişkenler arasındaki gecikmeli (lagged) ilişkileri ve istatistiksel dinamikleri incelemek amacıyla geliştirilmiştir. Yalnızca durağan verileri görselleştirmekle kalmayıp, zaman serisi analizleri ve korelasyon metrikleri sunar.

### 🔑 Öne Çıkan Özellikler
* **Canlı Veri Mimarisi:** FRED API entegrasyonu ile otomatik güncellenen veri akışı.
* **İnteraktif Dashboard:** Streamlit ve Plotly kullanılarak oluşturulmuş, tarih bazlı filtrelenebilir dinamik arayüz.
* **Zaman Serisi & Gecikme Analizi (Lag Analysis):** Enflasyon ile Fed politika faizleri arasındaki gecikmeli korelasyon (0, 3, 6, 9 ve 12 aylık) hesaplamaları.
* **İstatistiksel Metrikler:** Pearson Korelasyon Katsayısı, OLS Trend analizi ve *Korelasyon vs Nedensellik (Causality)* değerlendirmeleri.

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.x
* **Veri Kaynağı:** FRED API (`fredapi`)
* **Veri İşleme & Analiz:** `pandas`, `numpy`
* **Görselleştirme:** `plotly`
* **Web Arayüzü:** `streamlit`

---

## 📊 İstatistiksel Çıkarımlar & Bulgular

1. **Anlık İlişki (0 Ay Gecikmeli):** Enflasyon ile Politika Faizi arasındaki anlık Pearson korelasyonu düşük seviyededir ($r \approx 0.08$). Bu durum, merkez bankalarının enflasyona anlık değil, tepkisel yaklaştığını gösterir.
2. **Gecikmeli Etki (Lag Effect):** Gecikme süresi 12 aya çıkarıldığında korelasyon kuvvetlenerek $r \approx 0.70$ seviyesine ulaşmaktadır. Analiz, Fed'in faiz kararlarının enflasyon hareketlerini yaklaşık 9-12 ay geriden takip ettiğini doğrulamaktadır.

>  İstatistiksel Uyarı (Caution): Yüksek korelasyon doğrudan bir nedensellik (causality) kanıtı değildir. Zaman serilerindeki bu gecikmeli ilişkinin doğrulanması için ekonometrik *Granger Nedensellik Testi* metodolojisi dikkate alınmalıdır.

---

 **Yerel Kurulum ve Çalıştırma**

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/mugurekm/macro-data-dashboard.git
   cd macro-data-dashboard```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt```

3.uygulamayı başlatın 
```bash
streamlit run app.py```


 
