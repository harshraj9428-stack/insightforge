import streamlit as st
import pandas as pd
import plotly.express as px
import os

from config import APP_NAME, TAGLINE
from database.db import init_db
from services.auth import authenticate
from services.ai_insights import generate_ai_insight

# ------------------ PAGE CONFIG ------------------
# ✅ THIS MUST BE FIRST STREAMLIT CALL
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)
# ------------------ DB INIT ------------------
conn = init_db("database/users.db")

# ------------------ HEADER ------------------
st.title(APP_NAME)
st.caption(TAGLINE)

# ------------------ SESSION ------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ LOGIN ------------------
if not st.session_state.user:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(conn, username, password)
        if user:
            st.session_state.user = user
            st.success(f"Logged in as {user[0]}")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------ MAIN APP ------------------
else:
    st.sidebar.success(f"Logged in as {st.session_state.user[0]}")

    # -------- DATA LOAD --------
    df = None
    demo_path = "sample_data/demo_sales.csv"

    if st.sidebar.button("Load Demo Data"):
        if os.path.exists(demo_path):
            df = pd.read_csv(demo_path)
        else:
            st.error("Demo data file not found.")

    uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)

    if df is None:
        st.info("Upload CSV or load demo data to continue.")
        st.stop()

    # -------- BASIC CLEANING --------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # -------- KPIs --------
    st.subheader("Key Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Revenue", f"${df['Revenue'].fillna(0).sum():,.2f}")

    with col2:
        st.metric("Units Sold", int(df['Units Sold'].fillna(0).sum()))

    with col3:
        st.metric("Top Region", df["Region"].mode()[0])

    # -------- CHARTS --------
    st.subheader("Analytics Overview")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            df,
            x="Region",
            y="Revenue",
            title="Revenue by Region",
            color="Region"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(
            df,
            names="Category",
            values="Units Sold",
            title="Units Sold by Category"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Revenue Trend")

    fig3 = px.line(
        df.sort_values("Date"),
        x="Date",
        y="Revenue",
        title="Revenue Over Time"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # -------- AI INSIGHTS --------
    st.subheader("AI Insights")
    st.info("AI-generated insights are advisory.")
    st.write(generate_ai_insight(df))

    # -------- EXPORT --------
    st.subheader("Export Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download as CSV",
        csv,
        "insightforge_data.csv",
        "text/csv"
    )

    # -------- EMAIL (DEMO MODE) --------
    with st.expander("Email Report"):
        email = st.text_input("Recipient Email")
        if st.button("Send Report"):
            st.success("Email module connected (demo mode).")

# ------------------ FOOTER ------------------
st.markdown(
    "<center><small>InsightForge v1.0 • AI-Powered Business Analytics</small></center>",
    unsafe_allow_html=True
)
