import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="📊 Marketing Dashboard", layout="wide")
st.title("📊 Marketing Campaign Performance Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Campaign_Data")

    # Metrics
    df["CTR"] = df["Clicks"]/df["Impressions"]
    df["Conversion_Rate"] = df["Conversions"]/df["Clicks"]
    df["CPC"] = df["Total_Spend"]/df["Clicks"]
    df["CPA"] = df["Total_Spend"]/df["Conversions"]
    df["ROAS"] = df["Revenue_Generated"]/df["Total_Spend"]

    # Sidebar Filters
    channels = ["All"] + sorted(df["Marketing_Channel"].unique())
    channel_choice = st.sidebar.selectbox("Filter by Channel", channels)
    if channel_choice != "All":
        df = df[df["Marketing_Channel"] == channel_choice]

    # KPIs
    st.subheader("📌 KPIs Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impressions", f"{df['Impressions'].sum():,.0f}")
    col2.metric("Total Clicks", f"{df['Clicks'].sum():,.0f}")
    col3.metric("Total Conversions", f"{df['Conversions'].sum():,.0f}")
    col4.metric("Total Spend ($)", f"{df['Total_Spend'].sum():,.2f}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Total Revenue ($)", f"{df['Revenue_Generated'].sum():,.2f}")
    col6.metric("Avg CTR", f"{df['CTR'].mean():.2%}")
    col7.metric("Overall ROAS", f"{df['ROAS'].mean():.2f}")

    # Campaign Performance
    st.subheader("📊 Campaign Performance")
    camp_perf = df.groupby("Campaign_Name").agg({
        "Impressions":"sum","Clicks":"sum","Conversions":"sum",
        "Total_Spend":"sum","Revenue_Generated":"sum"
    }).reset_index()
    camp_perf["ROAS"] = camp_perf["Revenue_Generated"]/camp_perf["Total_Spend"]

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=camp_perf, x="Campaign_Name", y="ROAS", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # Channel Performance
    st.subheader("📊 Channel Performance")
    channel_perf = df.groupby("Marketing_Channel").agg({
        "Impressions":"sum","Clicks":"sum","Conversions":"sum",
        "Total_Spend":"sum","Revenue_Generated":"sum"
    }).reset_index()
    channel_perf["ROAS"] = channel_perf["Revenue_Generated"]/channel_perf["Total_Spend"]

    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(data=channel_perf, x="Marketing_Channel", y="ROAS", ax=ax2)
    st.pyplot(fig2)

    # Demographics
    st.subheader("👥 Demographic Insights")
    demo_perf = df.groupby(["Age_Group","Gender"]).agg({
        "Conversions":"sum","Revenue_Generated":"sum"
    }).reset_index()

    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.barplot(data=demo_perf, x="Age_Group", y="Conversions", hue="Gender", ax=ax3)
    st.pyplot(fig3)

    # Time Trends
    st.subheader("⏳ Time Trends")
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df["Month"] = df["Start_Date"].dt.to_period("M").astype(str)

    time_perf = df.groupby("Month").agg({
        "Impressions":"sum","Clicks":"sum","Conversions":"sum",
        "Total_Spend":"sum","Revenue_Generated":"sum"
    }).reset_index()
    time_perf["ROAS"] = time_perf["Revenue_Generated"]/time_perf["Total_Spend"]

    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.lineplot(data=time_perf, x="Month", y="ROAS", marker="o", ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

else:
    st.info("📂 Upload your Excel file to start the analysis.")

    # ===============================
    # 1. Top-Performing Campaigns & Channels
    # ===============================
    st.subheader("🏆 Top-Performing Campaigns & Channels")

    top_campaigns = camp_perf.sort_values("ROAS", ascending=False).head(5)
    st.write("🔝 Top 5 Campaigns by ROAS:")
    st.dataframe(top_campaigns[["Campaign_Name", "Conversions", "Revenue_Generated", "ROAS"]])

    top_channels = channel_perf.sort_values("ROAS", ascending=False).head(3)
    st.write("🔝 Top Channels by ROAS:")
    st.dataframe(top_channels[["Marketing_Channel", "Conversions", "Revenue_Generated", "ROAS"]])

    # ===============================
    # 2. Demographic Insights
    # ===============================
    st.subheader("👥 Demographic Insights")

    top_demo = demo_perf.sort_values("Conversions", ascending=False).head(5)
    st.write("🔝 Top 5 Demographics by Conversions:")
    st.dataframe(top_demo[["Age_Group", "Gender", "Conversions", "Revenue_Generated"]])

    # ===============================
    # 3. Seasonal / Temporal Trends
    # ===============================
    st.subheader("📅 Seasonal / Temporal Trends")

    best_months = time_perf.sort_values("ROAS", ascending=False).head(3)
    st.write("🔝 Best Months by ROAS:")
    st.dataframe(best_months[["Month", "Conversions", "Revenue_Generated", "ROAS"]])

    # ===============================
    # 4. Budget Allocation Recommendations
    # ===============================
    st.subheader("💡 Budget Allocation Recommendations")

    recs = []

    # حملات قوية (ROAS > 2)
    strong_campaigns = camp_perf[camp_perf["ROAS"] > 2]
    if not strong_campaigns.empty:
        recs.append(f"✅ Increase budget for high-performing campaigns: {', '.join(strong_campaigns['Campaign_Name'].tolist())}")

    # حملات ضعيفة (ROAS < 1)
    weak_campaigns = camp_perf[camp_perf["ROAS"] < 1]
    if not weak_campaigns.empty:
        recs.append(f"⚠️ Reduce/stop budget for low-performing campaigns: {', '.join(weak_campaigns['Campaign_Name'].tolist())}")

    # قنوات قوية وضعيفة
    strong_channels = channel_perf[channel_perf["ROAS"] > 2]
    if not strong_channels.empty:
        recs.append(f"✅ Focus more investment on strong channels: {', '.join(strong_channels['Marketing_Channel'].tolist())}")

    weak_channels = channel_perf[channel_perf["ROAS"] < 1]
    if not weak_channels.empty:
        recs.append(f"⚠️ Reconsider budget for weak channels: {', '.join(weak_channels['Marketing_Channel'].tolist())}")

    if recs:
        for r in recs:
            st.write("- " + r)
    else:
        st.info("No major budget reallocation recommendations at this time.")
