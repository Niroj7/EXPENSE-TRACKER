import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Expense Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Dashboard (2024)")
st.write("An interactive and recruiter-friendly financial dashboard.")

# -----------------------------
# LOAD DATA
# -----------------------------
uploaded_file = st.file_uploader("Upload your data.csv file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, header=None)
    df.columns = ["Date", "Item", "Amount", "Category"]
    df["Amount"] = df["Amount"].astype(float)
    df["Month"] = pd.to_datetime(df["Date"]).dt.month
else:
    st.warning("Please upload your data.csv file to view the dashboard.")
    st.stop()

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

total_spend = df["Amount"].sum()
avg_month = df.groupby("Month")["Amount"].sum().mean()
top_category = df.groupby("Category")["Amount"].sum().idxmax()
top_cat_amount = df.groupby("Category")["Amount"].sum().max()

col1.metric("Total Spend (2024)", f"${total_spend:,.2f}")
col2.metric("Average Monthly Spend", f"${avg_month:,.2f}")
col3.metric("Highest Category", top_category)
col4.metric("Amount in Highest Category", f"${top_cat_amount:,.2f}")

st.markdown("---")

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

month_filter = st.sidebar.multiselect(
    "Select Month(s)",
    options=sorted(df["Month"].unique()),
    default=sorted(df["Month"].unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered_df = df[df["Month"].isin(month_filter)]
filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

# -----------------------------
# CATEGORY BREAKDOWN (PIE CHART)
# -----------------------------
st.subheader("📊 Spending by Category")

cat_breakdown = filtered_df.groupby("Category")["Amount"].sum().reset_index()

pie = alt.Chart(cat_breakdown).mark_arc().encode(
    theta="Amount",
    color="Category",
    tooltip=["Category", "Amount"]
)

st.altair_chart(pie, use_container_width=True)

# -----------------------------
# MONTHLY SPENDING TREND
# -----------------------------
st.subheader("📈 Monthly Spending Trend")

monthly = filtered_df.groupby("Month")["Amount"].sum().reset_index()

line = alt.Chart(monthly).mark_line(point=True).encode(
    x=alt.X("Month:O"),
    y="Amount",
    tooltip=["Month", "Amount"],
    color=alt.value("#4A90E2")
)

st.altair_chart(line, use_container_width=True)

# -----------------------------
# TOP CATEGORIES (BAR CHART)
# -----------------------------
st.subheader("🏆 Top Spending Categories")

top_cats = filtered_df.groupby("Category")["Amount"].sum().reset_index().sort_values(
    "Amount", ascending=False
)

bars = alt.Chart(top_cats).mark_bar().encode(
    x="Amount",
    y=alt.Y("Category", sort="-x"),
    tooltip=["Category", "Amount"],
    color="Category"
)

st.altair_chart(bars, use_container_width=True)

# -----------------------------
# MONTHLY STACKED BAR
# -----------------------------
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
st.success("Dashboard loaded successfully! 🎉")
