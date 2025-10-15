import streamlit as st
from scanner import fetch_futures_data

st.set_page_config(page_title="Binance Futures Scanner PRO", layout="wide")

st.title("📊 Binance Futures Advanced Market Scanner")
st.caption("Powered by CCXT + Streamlit | Real-time market metrics")

with st.spinner("Fetching Binance Futures data..."):
    df = fetch_futures_data(limit=150)

st.subheader("🔥 Top 10 Most Volatile Pairs (24H)")
top10 = df.head(10)
st.dataframe(top10.style.background_gradient(subset=['Volatility Index'], cmap='coolwarm'))

st.subheader("📈 Full Market Overview")
st.dataframe(df.style.applymap(
    lambda v: "color:green" if isinstance(v, (int,float)) and v > 0 else "color:red" if isinstance(v, (int,float)) and v < 0 else None,
    subset=['% Change (24H)']
))

# Optional expansion panels
with st.expander("🧭 Explanation of Metrics"):
    st.markdown("""
    - **% Change (24H)** → Persentase kenaikan/penurunan harga dalam 24 jam terakhir  
    - **Volatility Index** → Mengukur seberapa besar fluktuasi harga dalam periode terakhir  
    - **Whale Bias** → Estimasi dominasi order besar (buy vs sell wall)  
    - **Fear & Greed** → Kombinasi volatilitas, volume, dan funding rate → 0 = Fear, 100 = Greed  
    - **Top Volatile** → Pair dengan perubahan harga paling dinamis  
    """)

st.success("✅ Data successfully loaded. Updated in real-time from Binance Futures.")
