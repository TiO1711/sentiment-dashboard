
import streamlit as st
import pandas as pd
import numpy as np
from combined_sentiment_fetcher import get_combined_sentiment

st.set_page_config(page_title="Sentiment Dashboard", layout="wide", page_icon="📊")

st.title("📊 Multi-Asset Sentiment Dashboard")

# Auswahl der Assets
asset_options = {
    "DAX40": "DAX+OR+Deutscher+Aktienindex",
    "EUR/USD": "Euro+OR+EUR+USD+Wechselkurs",
    "Gold": "Gold+OR+XAU+Goldpreis",
    "Bitcoin": "Bitcoin+OR+BTC+Kryptowährung"
}

selected_asset = st.selectbox("🌍 Wähle einen Markt:", list(asset_options.keys()))
rss_fallback_url = "https://www.finanzen.net/rss/news/dax"  # als Platzhalter, da nur ein RSS-Feed enthalten ist

# Manuelle Anpassung der Abfrage für get_combined_sentiment
with st.spinner(f"🔎 Analysiere aktuelle Nachrichten für {selected_asset}..."):
    from combined_sentiment_fetcher import sentiment_score, clean_text, API_KEY
    import requests
    import feedparser

    query = asset_options[selected_asset]
    url_newsapi = f"https://newsapi.org/v2/everything?q={query}&language=de&pageSize=10&sortBy=publishedAt&apiKey={API_KEY}"
    r = requests.get(url_newsapi)
    news_titles = [article["title"] for article in r.json().get("articles", [])]
    score_newsapi = sentiment_score(" ".join(clean_text(t) for t in news_titles))

    feed = feedparser.parse(rss_fallback_url)
    rss_titles = [entry.title for entry in feed.entries[:10]]
    score_rss = sentiment_score(" ".join(clean_text(t) for t in rss_titles))

    combined_score = round((score_newsapi + score_rss) / 2, 3)
    all_headlines = news_titles + rss_titles

# Anzeige der Bewertung
st.metric(label="📈 Kombinierter Sentiment-Score", value=combined_score)
st.caption(f"Teilwerte: NewsAPI = {score_newsapi:.2f}, Finanzen.net RSS = {score_rss:.2f}")

# Ergebnis-Einschätzung
if combined_score >= 0.6:
    st.success("📗 Empfehlung: LONG – starke positive Marktstimmung")
elif combined_score <= -0.6:
    st.error("📕 Empfehlung: SHORT – negative Marktstimmung")
else:
    st.warning("📙 Empfehlung: NoTrade – neutrale oder uneindeutige Lage")

# Schlagzeilen anzeigen
st.subheader("📰 Verwendete Schlagzeilen")
for headline in all_headlines:
    st.markdown(f"• {headline}")

st.markdown("---")
st.caption("© 2025 – Kombinierte NLP-Sentimentanalyse (NewsAPI + Finanzen.net RSS)")
