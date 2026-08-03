import streamlit as st
import pandas as pd
import numpy as np
from fredapi import Fred
import plotly.graph_objects as go
import plotly.express as px

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Macro Data Dashboard", layout="wide")

st.title("📈 Makroekonomik Veri Analitiği Panosu")
st.markdown("FRED API üzerinden canlı çekilen veri seti ile ABD enflasyon, faiz ve makro dinamikler analizi.")

# Sidebar - API Key Girişi
st.sidebar.header("Ayarlar")
API_KEY = st.sidebar.text_input("FRED API Key", type="password", help="FRED sitesinden aldığınız 32 karakterlik anahtar.")

if not API_KEY:
    st.warning("⚠️ Lütfen analizi görüntülemek için sol menüye FRED API anahtarınızı girin.")
    st.stop()

@st.cache_data(ttl=3600)
def load_data(api_key):
    try:
        fred = Fred(api_key=api_key)
        series = {
            'CPI': 'CPIAUCSL',
            'Fed_Rate': 'FEDFUNDS',
            'Unemployment': 'UNRATE'
        }
        df = pd.DataFrame({k: fred.get_series(v) for k, v in series.items()})
        df = df[df.index >= '2015-01-01']
        df['Inflation_YoY'] = df['CPI'].pct_change(12) * 100
        df['Real_Rate'] = df['Fed_Rate'] - df['Inflation_YoY']
        return df.ffill().dropna()
    except Exception as e:
        st.error(f"Veri çekilirken hata oluştu: {e}")
        return None

df_raw = load_data(API_KEY)

if df_raw is not None:
    # Sidebar Filtreleri
    st.sidebar.header("Filtreler")
    selected_years = st.sidebar.slider(
        "Yıl Aralığı Seçin", 
        int(df_raw.index.year.min()), 
        int(df_raw.index.year.max()), 
        (2015, int(df_raw.index.year.max()))
    )

    # Filtrelenmiş Veri
    df = df_raw[(df_raw.index.year >= selected_years[0]) & (df_raw.index.year <= selected_years[1])]

    # Üst Bilgi Kartları (KPI Metrics)
    col1, col2, col3 = st.columns(3)
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    col1.metric("Yıllık Enflasyon", f"%{latest['Inflation_YoY']:.2f}", f"{latest['Inflation_YoY'] - prev['Inflation_YoY']:.2f}%")
    col2.metric("Fed Faizi", f"%{latest['Fed_Rate']:.2f}", f"{latest['Fed_Rate'] - prev['Fed_Rate']:.2f}%")
    col3.metric("İşsizlik Oranı", f"%{latest['Unemployment']:.2f}", f"{latest['Unemployment'] - prev['Unemployment']:.2f}%")

    st.divider()

    # Ana Zaman Serisi Grafiği
    st.subheader("📊 Enflasyon ve Politika Faizi Zaman Serisi")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Inflation_YoY'], name='Enflasyon (%)', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=df.index, y=df['Fed_Rate'], name='Fed Faizi (%)', line=dict(color='blue', dash='dash', width=2)))
    fig.update_layout(template='plotly_white', hovermode='x unified', margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # İSTATİSTİKSEL ANALİZ
    st.subheader("🔬 İstatistiksel Analiz: Korelasyon ve Nedensellik (Causality)")

    col_corr1, col_corr2 = st.columns([1, 1])

    with col_corr1:
        corr_val = df['Inflation_YoY'].corr(df['Fed_Rate'])
        st.markdown(f"**Pearson Korelasyon Katsayısı (r):** `{corr_val:.3f}`")
        
        fig_scatter = px.scatter(
            df, x='Inflation_YoY', y='Fed_Rate', 
            trendline="ols",
            labels={'Inflation_YoY': 'Enflasyon (%)', 'Fed_Rate': 'Fed Faizi (%)'},
            title="Enflasyon vs Fed Faizi Serpme Grafiği"
        )
        fig_scatter.update_layout(template='plotly_white')
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_corr2:
        st.markdown("**Gecikmeli (Lag) Korelasyon Analizi:**")
        st.caption("Faiz kararları enflasyona anında etki etmez. Aşağıdaki tablo, faizin kaç ay geriden geldiğini gösterir.")
        
        lags = [0, 3, 6, 9, 12]
        lag_corrs = {}
        for lag in lags:
            lag_corrs[f"{lag} Ay Gecikmeli"] = df['Inflation_YoY'].corr(df['Fed_Rate'].shift(-lag))
        
        df_lag = pd.DataFrame(list(lag_corrs.items()), columns=['Gecikme Süresi', 'Korelasyon'])
        st.dataframe(df_lag, hide_index=True, use_container_width=True)
        
        st.warning("""
        ⚠️ **Caution (İstatistiksel Uyarı):** 
        Yüksek korelasyon doğrudan bir **nedensellik (causality)** olduğunu kanıtlamaz. 
        Merkez bankaları faizi enflasyona tepki olarak artırır (gecikmeli etki). Gerçek nedensellik analizi için *Granger Nedensellik Testi* gibi zaman serisi testleri uygulanmalıdır.
        """)

    with st.expander("Ham Veriyi Görüntüle"):
        st.dataframe(df.tail(20))
