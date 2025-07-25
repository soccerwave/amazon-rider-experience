import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# main path of project
BASE_DIR = Path(os.getcwd())
cleaned_path = BASE_DIR / "data" / "processed" / "cleaned_amazon.csv"
riders_path = BASE_DIR / "data" / "processed" / "riders_loyalty.csv"

# upload new file (optional)
st.sidebar.header("🔄 Upload New Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ New dataset loaded.")
else:
    df = pd.read_csv(cleaned_path)

# fixed data (loyalty)
df_riders = pd.read_csv(riders_path)

# checking to see if data is good or not
required_cols = ['Pickup_Delay_Minutes', 'Delivery_Speed_KMPH', 'Agent_Rating', 'Delivery_Time', 'Vehicle', 'Traffic']
if not all(col in df.columns for col in required_cols):
    st.error("⛔ The dataset is missing required columns.")
    st.stop()

# dashboard
st.title("📦 Rider Performance Dashboard – Amazon Delivery")
st.write("تعداد ردیف‌ها:", len(df))

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Avg Pickup Delay (min)", f"{df['Pickup_Delay_Minutes'].mean():.2f}")
with col2:
    st.metric("🚀 Median Delivery Speed (km/h)", f"{df['Delivery_Speed_KMPH'].median():.2f}")
with col3:
    on_time = (df['Delivery_Time'] <= 45).mean()
    st.metric("⏱️ On-Time Delivery Rate", f"{on_time:.0%}")

# Filters
st.sidebar.header("Filter Options")
vehicle_filter = st.sidebar.selectbox("Select Vehicle Type", ["All"] + sorted(df['Vehicle'].dropna().unique()))
traffic_filter = st.sidebar.selectbox("Select Traffic Condition", ["All"] + sorted(df['Traffic'].dropna().unique()))

filtered_df = df.copy()
if vehicle_filter != "All":
    filtered_df = filtered_df[filtered_df["Vehicle"] == vehicle_filter]
if traffic_filter != "All":
    filtered_df = filtered_df[filtered_df["Traffic"] == traffic_filter]

# Delivery Speed fig
st.subheader("🚚 Delivery Speed Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['Delivery_Speed_KMPH'], bins=30, kde=True, ax=ax1)
st.pyplot(fig1)

# Delivery Time based on Traffic fig
st.subheader("🚦 Avg Delivery Time by Traffic")
fig2, ax2 = plt.subplots()
sns.barplot(data=filtered_df, x="Traffic", y="Delivery_Time", ci=False, ax=ax2)
st.pyplot(fig2)

# Loyalty fig
st.subheader("🏅 Loyalty Tier Distribution")
fig3, ax3 = plt.subplots()
tier_colors = {"Gold": "gold", "Silver": "silver", "Bronze": "peru"}
df_riders['Loyalty_Tier'].value_counts().plot(kind="bar",
    color=[tier_colors.get(t, "gray") for t in df_riders['Loyalty_Tier'].unique()], ax=ax3)
ax3.set_ylabel("Number of Riders")
st.pyplot(fig3)
