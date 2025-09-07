import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================
# 1. Title & Upload
# ========================
st.set_page_config(page_title="📊 Marketing Campaign Dashboard", layout="wide")

st.title("📊 Marketing Campaign Performance Dashboard")
st.write("Analyze and optimize marketing strategies using KPIs, demographics, and trends.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Campaign_Data")

    # ========================
    # 2. Data Cleaning & Metrics
    # ========================
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["Conversion_Rate"] = df["Conversions"] / df["Clicks"]
    df["CPC"] = df["Total_Spend"] / df["Clicks"]
    df["CPA"] = df["Total_Spend"] / df["Conversions"]
    df["ROAS"] = df["Revenue_Generated"] / df["Total_Spend"]

    # ========================
    # 3. KPIs Summary
    # ========================
    st.header("📌 KPIs Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impressions", f"{df['Impressions'].sum():,.0f}")
    col2.metric("Total Clicks", f"{df['Clicks'].sum():,.0f}")
    col3.metric("Total Conversions", f"{df['Conversions'].sum():,.0f}")
    col4.metric("Total Spend ($)", f"{df['Total_Spend'].sum():,.2f}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Total Revenue ($)", f"{df['Revenue_Generated'].sum():,.2f}")
    col6.metric("Average CTR", f"{df['CTR'].mean():.2%}")
    col7.metric("Overall ROAS", f"{df['ROAS'].mean():.2f}")

    # ========================
    # 4. Campaign Performance
    # ========================
    st.header("📊 Campaign Performance")
    camp_perf = df.groupby("Campaign_Name").agg({
        "Impressions": "sum", "Clicks": "sum", "Conversions": "sum",
        "Total_Spend": "sum", "Revenue_Generated": "sum"
    }).reset_index()
    camp_perf["ROAS"] = camp_perf["Revenue_Generated"] / camp_perf["Total_Spend"]

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=camp_perf, x="Campaign_Name", y="ROAS", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title("ROAS per Campaign")
    st.pyplot(fig)

    # ========================
    # 5. Channel Performance
    # ========================
    st.header("📊 Channel Performance")
    channel_perf = df.groupby("Marketing_Channel").agg({
        "Impressions": "sum", "Clicks": "sum", "Conversions": "sum",
        "Total_Spend": "sum", "Revenue_Generated": "sum"
    }).reset_index()
    channel_perf["ROAS"] = channel_perf["Revenue_Generated"] / channel_perf["Total_Spend"]

    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(data=channel_perf, x="Marketing_Channel", y="ROAS", ax=ax2)
    plt.title("ROAS per Channel")
    st.pyplot(fig2)

    # ========================
    # 6. Demographic Insights
    # ========================
    st.header("👥 Demographic Insights")
    demo_perf = df.groupby(["Age_Group","Gender"]).agg({
        "Conversions":"sum","Revenue_Generated":"sum"
    }).reset_index()

    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.barplot(data=demo_perf, x="Age_Group", y="Conversions", hue="Gender", ax=ax3)
    plt.title("Conversions by Age & Gender")
    st.pyplot(fig3)

    # ========================
    # 7. Time-based Analysis
    # ========================
    st.header("⏳ Time-based Trends")
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df["Month"] = df["Start_Date"].dt.to_period("M").astype(str)

    time_perf = df.groupby("Month").agg({
        "Impressions":"sum","Clicks":"sum","Conversions":"sum",
        "Total_Spend":"sum","Revenue_Generated":"sum"
    }).reset_index()
    time_perf["ROAS"] = time_perf["Revenue_Generated"] / time_perf["Total_Spend"]

    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.lineplot(data=time_perf, x="Month", y="ROAS", marker="o", ax=ax4)
    plt.xticks(rotation=45)
    plt.title("ROAS Over Time")
    st.pyplot(fig4)

else:
    st.warning("📂 Please upload an Excel file to start the analysis.")
