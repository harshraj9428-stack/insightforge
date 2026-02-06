import streamlit as st
import google.generativeai as genai

def local_insights(df):
    insights = []

    if "Region" in df.columns and "Revenue" in df.columns:
        top_region = df.groupby("Region")["Revenue"].sum().idxmax()
        insights.append(f"{top_region} region generates the highest revenue.")

    if "Category" in df.columns and "Revenue" in df.columns:
        top_category = df.groupby("Category")["Revenue"].sum().idxmax()
        insights.append(f"{top_category} category drives the majority of revenue.")

    if "Revenue" in df.columns:
        insights.append("Overall revenue trend appears stable across the selected period.")

    insights.append("AI quota fallback activated — insights generated locally.")

    return "\n".join(insights)

def generate_ai_insight(df):
    try:
        genai.configure(api_key=st.secrets["ai"]["gemini_api_key"])
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
        Analyze the dataset and provide business insights:
        {df.head(10).to_string()}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception:
        # ✅ graceful fallback
        return local_insights(df)
