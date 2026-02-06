import streamlit as st
import pandas as pd
import plotly.express as px
import os

from config import APP_NAME, TAGLINE
from database.db import init_db
from services.auth import authenticate
from services.ai_insights import generate_ai_insight

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title=APP_NAME, layout="wide")

# ------------------ DB INIT ------------------
conn = init_db("database/users.db")

# ------------------ HEADER ------------------
st.title(APP_NAME)
st.caption(TAGLINE)

# ------------------ SESSION INIT ------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ================== LOGIN ==================
if st.session_state.user is None:
    st.subheader("Login")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(conn, username_input, password_input)
        if user:
            st.session_state.user = user  # (username, role)
            st.success(f"Logged in as {user[0]}")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ================== MAIN APP ==================
else:
    # 🔐 SAFE UNPACKING (NO CRASH)
    username, role = st.session_state.user

    st.sidebar.success(f"Logged in as {username}")

    # -------- ADMIN PANEL --------
    if role == "Admin":
        st.sidebar.markdown("### 👤 Create New User")

        new_user = st.sidebar.text_input("New Username")
        new_pass = st.sidebar.text_input("New Password", type="password")

        if st.sidebar.button("Create User"):
            if new_user and new_pass:
                from database.db import create_user
                create_user(conn, new_user, new_pass)
                st.sidebar.success("User created successfully")
            else:
                st.sidebar.error("Username and password required")

    # -------- DATA LOAD --------
    df = None
    demo_path = "sample_data/demo_sales.csv"

    if st.sidebar.button("Load Demo Data"):
        if os.path.exists(demo_path):
            df = pd.read_csv(demo_path)
        else:
            st.error("Demo data file not found.")

    uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded is not None:
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
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Revenue", f"${df['Revenue'].fillna(0).sum():,.2f}")

    with c2:
        st.metric("Units Sold", int(df['Units Sold'].fillna(0).sum()))

    with c3:
        st.metric("Top Region", df["Region"].mode()[0])

    # -------- CHARTS --------
    st.subheader("Analytics Overview")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(df, x="Region", y="Revenue", title="Revenue by Region", color="Region")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(df, names="Category", values="Units Sold", title="Units Sold by Category")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Revenue Trend")
    fig3 = px.line(df.sort_values("Date"), x="Date", y="Revenue", title="Revenue Over Time")
    st.plotly_chart(fig3, use_container_width=True)

    # -------- AI INSIGHTS --------
    st.subheader("AI Insights")
    st.info("AI-generated insights are advisory.")
    st.write(generate_ai_insight(df))

    # -------- EXPORT --------
    st.subheader("Export Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", csv, "insightforge_data.csv", "text/csv")

    # -------- EMAIL (DEMO) --------
    with st.expander("Email Report"):
        st.text_input("Recipient Email")
        st.button("Send Report", disabled=True)

# ------------------ FOOTER ------------------
st.markdown(
    "<center><small>InsightForge v1.0 • AI-Powered Business Analytics</small></center>",
    unsafe_allow_html=True
)
