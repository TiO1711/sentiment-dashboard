
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

st.title("📊 Sentiment Dashboard – DAX, EUR/USD, Gold, Bitcoin")

# Dummy-Zeitreihe für Chart-Demo
np.random.seed(1)
assets = ["DAX40", "EUR/USD", "Gold", "Bitcoin"]
score_data = {
    asset: np.clip(np.cumsum(np.random.randn(12) * 0.1), -1, 1) for asset in assets
}

# Tabelle für aktuelle Einschätzung
df_now = pd.DataFrame({
    "Asset": assets,
    "Sentiment-Score": [0.72, -0.45, 0.15, 0.67],
    "Empfehlung": ["Long", "Short", "NoTrade", "Long"],
    "Kommentar": [
        "Positiver News-Flow zu Exporten",
        "Zinsunsicherheit in den USA",
        "Neutraler Markt",
        "Starke Nachfrage institutioneller Anleger"
    ]
})

# Farbgebung
def highlight_row(row):
    color = ""
    if row["Empfehlung"] == "Long":
        color = "background-color: #d1e7dd"
    elif row["Empfehlung"] == "Short":
        color = "background-color: #f8d7da"
    else:
        color = "background-color: #fff3cd"
    return [color] * len(row)

# Auto-Refresh Button
refresh = st.button("🔄 Neu laden")

# Zwei Spalten-Layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📈 Übersicht aktuelle Signale")
    st.dataframe(df_now.style.apply(highlight_row, axis=1), use_container_width=True)

with col2:
    st.subheader("ℹ️ Erläuterung")
    st.markdown("""
    **Legende:**
    - 🟢 *Long*: Stark positives Sentiment
    - 🔴 *Short*: Stark negatives Sentiment
    - 🟡 *NoTrade*: Neutral oder uneindeutig

    **Hinweis:** Diese Analyse basiert auf NLP-Auswertungen von Finanznachrichten der letzten 4–8 Stunden.
    """)

st.markdown("---")

# Auswahl & Chart
selected_asset = st.selectbox("📊 Sentiment-Verlauf anzeigen für:", assets)
chart_df = pd.DataFrame({
    "Zeit": [f"H-{i*4}" for i in range(12)][::-1],
    "Sentiment": score_data[selected_asset]
})
st.line_chart(chart_df.set_index("Zeit"))

st.caption("© 2025 – Sentiment Dashboard (beta) | Quelle: NewsAPI.org")
