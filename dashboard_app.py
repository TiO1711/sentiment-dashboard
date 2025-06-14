
import streamlit as st
import pandas as pd
import datetime

# Beispielhafte Dummy-Daten
data = {
    "Asset": ["DAX", "EUR/USD", "Gold", "Bitcoin"],
    "H4_1": [-0.3, 0.1, 0.4, 0.3],
    "H4_2": [-0.4, 0.2, 0.3, 0.2],
    "H4_3": [-0.2, -0.1, 0.2, 0.1],
    "H4_4": [-0.1, 0.05, 0.3, 0.2]
}
df = pd.DataFrame(data)
df.set_index("Asset", inplace=True)

st.title("Sentiment Dashboard für DAX, EUR/USD, Gold & Bitcoin")

st.write("Zeitraum:", datetime.datetime.now().strftime("%Y-%m-%d"))
st.write("Letzte 4 H4-Kerzen (jeweils 4 Stunden)")

st.dataframe(df.style.background_gradient(cmap='RdYlGn', axis=1))

st.subheader("Trendbewertung")
for asset in df.index:
    trend = df.loc[asset].diff().sum()
    if trend > 0.05:
        st.markdown(f"**{asset}:** 📈 _Steigend_")
    elif trend < -0.05:
        st.markdown(f"**{asset}:** 📉 _Fallend_")
    else:
        st.markdown(f"**{asset}:** ➖ _Stabil_")

