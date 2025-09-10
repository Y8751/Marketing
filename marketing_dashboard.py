# ========================
# 1. Import Libraries
# ========================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Page setup
st.set_page_config(page_title="Marketing Dashboard", layout="wide")
st.title("Marketing Campaign Performance Dashboard")

# ========================
# 2. File Upload
# ========================
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Campaign_Data")

    # ========================
    # 3. Basic Metrics
    # ========================
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["Conversion_Rate"] = df["Conversions"] / df["Clicks"]
    df["CPC"] = df["Total_Spend"] / df["Clicks"]
    df["CPA"] = df["Total_Spend"] / df["Conversions"]
    df["ROAS"] = df["Revenue_Generated"] / df["Total_Spend"]

    # ========================
    # 4. Sidebar Filters
    # ========================
    channels = ["All"] + sorted(df["Marketing_Channel"].dropna().unique())
    choice = st.sidebar.selectbox("Filter by Channel", channels)
    if choice != "All":
        df = df[df["Marketing_Channel"] == choice]

    top_n_campaigns = st.sidebar.slider("Top N Campaigns", 1, 20, 5)
    top_n_channels = st.sidebar.slider("Top N Channels", 1, 10, 3)
    months_to_show = st.sidebar.slider("Months for Time Analysis", 1, 36, 12)

    # ========================
    # 5. KPI Summary
    # ========================
    st.subheader("Key Performance Indicators (KPIs)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impressions", f"{df['Impressions'].sum():,.0f}")
    col2.metric("Total Clicks", f"{df['Clicks'].sum():,.0f}")
    col3.metric("Total Conversions", f"{df['Conversions'].sum():,.0f}")
    col4.metric("Total Spend ($)", f"{df['Total_Spend'].sum():,.2f}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Total Revenue ($)", f"{df['Revenue_Generated'].sum():,.2f}")
    col6.metric("Avg CTR", f"{df['CTR'].mean():.2%}")
    col7.metric("Overall ROAS", f"{df['ROAS'].mean():.2f}")

    # ========================
    # 6. Campaign Performance
    # ========================
    st.subheader("Campaign Performance")
    camp_perf = df.groupby("Campaign_Name").agg({
        "Impressions": "sum",
        "Clicks": "sum",
        "Conversions": "sum",
        "Total_Spend": "sum",
        "Revenue_Generated": "sum"
    }).reset_index()
    camp_perf["ROAS"] = camp_perf["Revenue_Generated"] / camp_perf["Total_Spend"]

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=camp_perf, x="Campaign_Name", y="ROAS", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    st.dataframe(camp_perf, use_container_width=True)

    # ========================
    # 7. Channel Performance
    # ========================
    st.subheader("Channel Performance")
    channel_perf = df.groupby("Marketing_Channel").agg({
        "Impressions": "sum",
        "Clicks": "sum",
        "Conversions": "sum",
        "Total_Spend": "sum",
        "Revenue_Generated": "sum"
    }).reset_index()
    channel_perf["ROAS"] = channel_perf["Revenue_Generated"] / channel_perf["Total_Spend"]

    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(data=channel_perf, x="Marketing_Channel", y="ROAS", ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    st.dataframe(channel_perf, use_container_width=True)

    # ========================
    # 8. Top Campaigns & Channels
    # ========================
    st.subheader("Top Performing Campaigns & Channels")
    top_campaigns = camp_perf.sort_values("ROAS", ascending=False).head(top_n_campaigns)
    st.write(f"Top {top_n_campaigns} Campaigns by ROAS:")
    st.dataframe(top_campaigns[["Campaign_Name", "Conversions", "Revenue_Generated", "ROAS"]])

    top_channels = channel_perf.sort_values("ROAS", ascending=False).head(top_n_channels)
    st.write(f"Top {top_n_channels} Channels by ROAS:")
    st.dataframe(top_channels[["Marketing_Channel", "Conversions", "Revenue_Generated", "ROAS"]])

    # ========================
    # 9. Demographics Analysis
    # ========================
    st.subheader("Demographics Analysis")
    demo_perf = df.groupby(["Age_Group","Gender"]).agg({
        "Conversions":"sum","Revenue_Generated":"sum"
    }).reset_index()

    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.barplot(data=demo_perf, x="Age_Group", y="Conversions", hue="Gender", ax=ax3)
    st.pyplot(fig3)

    # ========================
    # 10. Time Analysis
    # ========================
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df["Month"] = df["Start_Date"].dt.to_period("M").astype(str)

    time_perf = df.groupby("Month").agg({
        "Impressions":"sum","Clicks":"sum","Conversions":"sum",
        "Total_Spend":"sum","Revenue_Generated":"sum"
    }).reset_index()
    time_perf["ROAS"] = time_perf["Revenue_Generated"] / time_perf["Total_Spend"]

    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.lineplot(data=time_perf.tail(months_to_show), x="Month", y="ROAS", marker="o", ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    # ========================
    # 11. Budget Allocation Recommendations
    # ========================
    st.subheader("Budget Allocation Recommendations")

    def detailed_budget_recommendations(camp_perf, channel_perf):
        recs = []

        # Campaigns
        for _, row in camp_perf.iterrows():
            if row["ROAS"] > 2.0:
                recs.append(f"✅ Campaign '{row['Campaign_Name']}' is high-performing. Increase budget.")
            elif row["ROAS"] < 1.0:
                recs.append(f"⚠️ Campaign '{row['Campaign_Name']}' is low-performing. Reduce budget.")
            else:
                recs.append(f"ℹ️ Campaign '{row['Campaign_Name']}' is medium-performing. Monitor performance.")

        # Channels
        for _, row in channel_perf.iterrows():
            if row["ROAS"] > 2.0:
                recs.append(f"✅ Channel '{row['Marketing_Channel']}' is strong. Increase investment.")
            elif row["ROAS"] < 1.0:
                recs.append(f"⚠️ Channel '{row['Marketing_Channel']}' is weak. Reduce investment.")
            else:
                recs.append(f"ℹ️ Channel '{row['Marketing_Channel']}' is medium-performing. Monitor investment.")

        return recs

    recommendations = detailed_budget_recommendations(camp_perf, channel_perf)
    for r in recommendations:
        st.write("- " + r)

else:
    st.info("Upload your Excel file to start the analysis.")
