# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Unemployment Analysis", layout="wide")

st.title("📊 Unemployment Analysis in India (Pre vs During COVID)")

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("Unemployment in India.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Covid Period'] = df['Date'].apply(lambda x: 'Pre-COVID' if x < pd.to_datetime('2020-03-01') else 'During-COVID')
    return df

df = load_data()

st.markdown("This dashboard explores unemployment trends in India before and during the COVID-19 pandemic using real data.")

# ---- Data Preview ----
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)

# ---- Average Unemployment Rate: Pre-COVID vs During-COVID ----
st.subheader("📉 Average Unemployment Rate: Pre-COVID vs During-COVID")
avg_unemp = df.groupby('Covid Period')['Estimated Unemployment Rate (%)'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=avg_unemp, x='Covid Period', y='Estimated Unemployment Rate (%)', palette='Set2', ax=ax1)
ax1.set_ylabel('Unemployment Rate (%)')
ax1.set_ylim(0, avg_unemp['Estimated Unemployment Rate (%)'].max() + 2)
st.pyplot(fig1)

# ---- Seasonal Trends ----
st.subheader("📆 Unemployment Trend Over Time")

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df, x='Date', y='Estimated Unemployment Rate (%)', hue='Region', ax=ax2)
ax2.set_ylabel('Unemployment Rate (%)')
st.pyplot(fig2)

# ---- Region-wise Comparison ----
st.subheader("🌍 Region-wise Unemployment Rate Comparison")

region = st.selectbox("Select a Region", sorted(df['Region'].unique()))
region_df = df[df['Region'] == region]

fig3, ax3 = plt.subplots()
sns.lineplot(data=region_df, x='Date', y='Estimated Unemployment Rate (%)', ax=ax3, color='teal')
ax3.set_title(f"Unemployment Trend in {region}")
st.pyplot(fig3)

# ---- Insights ----
st.subheader("🧠 Key Insights")

st.markdown("""
- **COVID-19 Impact**: There is a noticeable increase in unemployment rates starting March 2020.
- **Regional Variation**: Certain states/regions experienced sharper unemployment spikes than others.
- **Seasonal Trends**: Monthly patterns suggest economic disruption aligned with lockdowns.

### 📌 Policy Recommendations:
- Launch targeted employment schemes in severely affected regions.
- Promote remote job training and upskilling programs.
- Strengthen labor market data collection for real-time insights.
""")
