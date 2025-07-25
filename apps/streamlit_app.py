import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('🚴‍♂️ Rider Experience Dashboard')

# KPI summary
st.header('Key Performance Indicators')
kpi_df = pd.read_csv('../reports/ab_summary.csv')
st.dataframe(kpi_df)

st.header('Exploratory Analysis')
st.image('../reports/screenshots/loyalty_tiers.png', caption='Loyalty Tier Distribution')
st.image('../reports/screenshots/rider_clusters.png', caption='Rider Performance Clusters')
st.image('../reports/screenshots/ab_test_comparison.png', caption='A/B Test Results')

#Loyalty Tiers
st.header('🛡 Loyalty Tier Explorer')
df_loyalty = pd.read_csv('../data/processed/riders_loyalty.csv')
tier = st.selectbox("Select Tier", options=df_loyalty['Loyalty_Tier'].unique())
st.dataframe(df_loyalty[df_loyalty['Loyalty_Tier'] == tier])
