import pandas as pd
import streamlit as st
import altair as alt
from fpdf import FPDF

# ---------------------------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------------------------
st.set_page_config(
    page_title="Expense Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Dashboard (2024)")
st.write("An interactive and recruiter-friendly financial dashboard.")

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
uploaded_file = st.file_uploader("Upload your data.csv file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, header=0)
    df.columns = ["Date", "Item", "Amount", "Category"]
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
else:
    st.warning("⬆️ Upload your **data.csv** file to load the dashboard.")
    st.stop()

# ---------------------------------------------
# KPI CARDS
# ---------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_spend = df["Amount"].sum()
monthly_totals = df.groupby("Month")["Amount"].sum()
avg_month = monthly_totals.mean()
top_category = df.groupby("Category")["Amount"].sum().idxmax()
top_cat_amount = df.groupby("Category")["Amount"].sum().max()

col1.metric("Total Spend (2024)", f"${total_spend:,.2f}")
col2.metric("Average Monthly Spend", f"${avg_month:,.2f}")
col3.metric("Highest Category", top_category)
col4.metric("Amount in Highest Category", f"${top_cat_amount:,.2f}")

st.markdown("---")

# ---------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------
st.sidebar.header("Filters")

months_available = sorted(df["Month"].unique())
categories_available = sorted(df["Category"].unique())

month_filter = st.sidebar.multiselect(
    "Select Month(s)",
    options=months_available,
    default=months_available
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=categories_available,
    default=categories_available
)

filtered_df = df[df["Month"].isin(month_filter)]
filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

# ---------------------------------------------
# CATEGORY PIE CHART
# ---------------------------------------------
st.subheader("📊 Spending by Category")

cat_breakdown = filtered_df.groupby("Category")["Amount"].sum().reset_index()

pie_chart = alt.Chart(cat_breakdown).mark_arc().encode(
    theta="Amount",
    color="Category",
    tooltip=["Category", "Amount"]
)

st.altair_chart(pie_chart, use_container_width=True)

# ---------------------------------------------
# MONTHLY TREND LINE
# ---------------------------------------------
st.subheader("📈 Monthly Spending Trend")

monthly = filtered_df.groupby("Month")["Amount"].sum().reset_index()

line_chart = alt.Chart(monthly).mark_line(point=True).encode(
    x=alt.X("Month:O"),
    y="Amount",
    tooltip=["Month", "Amount"],
    color=alt.value("#4A90E2")
)

st.altair_chart(line_chart, use_container_width=True)

# ---------------------------------------------
# TOP CATEGORY BAR
# ---------------------------------------------
st.subheader("🏆 Top Spending Categories")

top_cats = filtered_df.groupby("Category")["Amount"].sum().reset_index().sort_values(
    "Amount", ascending=False
)

bar_chart = alt.Chart(top_cats).mark_bar().encode(
    x="Amount",
    y=alt.Y("Category", sort="-x"),
    tooltip=["Category", "Amount"],
    color="Category"
)

st.altair_chart(bar_chart, use_container_width=True)

# ---------------------------------------------
# STACKED MONTHLY BAR
# ---------------------------------------------
st.subheader("📦 Monthly Expense Composition (Stacked)")

stacked = filtered_df.groupby(["Month", "Category"])["Amount"].sum().reset_index()

stacked_bar = alt.Chart(stacked).mark_bar().encode(
    x=alt.X("Month:O"),
    y="Amount:Q",
    color="Category:N",
    tooltip=["Month", "Category", "Amount"]
).properties(height=400)

st.altair_chart(stacked_bar, use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# PDF GENERATION FUNCTION (FIXED)
# ------------------------------------------------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Expense Report (2024)", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Total Spending: ${total_spend:,.2f}", ln=True)
    pdf.cell(0, 10, f"Average Monthly Spend: ${avg_month:,.2f}", ln=True)
    pdf.cell(0, 10, f"Top Category: {top_category}", ln=True)
    pdf.cell(0, 10, f"Top Category Amount: ${top_cat_amount:,.2f}", ln=True)

    # Convert PDF string to bytes
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes

# ------------------------------------------------
# DOWNLOAD PDF BUTTON
# ------------------------------------------------
st.subheader("📄 Download PDF Report")

pdf_bytes = generate_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf_bytes,
    file_name="Expense_Report.pdf",
    mime="application/pdf"
)

st.success("Dashboard Loaded Successfully 🎉")
