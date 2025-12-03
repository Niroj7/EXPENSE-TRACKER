import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CSV_FILE = "data.csv"

# ----------------------- CSV UTILITIES -----------------------
def load_data():
    try:
        df = pd.read_csv(CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Amount"] = df["Amount"].astype(float)
        df["Month"] = df["Date"].dt.month
        df["MonthName"] = df["Date"].dt.strftime("%B")
        df["Quarter"] = df["Date"].dt.quarter
        return df
    except:
        return pd.DataFrame(columns=["Date", "Item", "Amount", "Category", "Month", "MonthName", "Quarter"])

def save_expense(item, amount, category):
    df = load_data()
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Item": item,
        "Amount": float(amount),
        "Category": category
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# ----------------------- ADD EXPENSE -----------------------
def add_expense():
    item = entry_item.get()
    amount = entry_amount.get()
    category = category_var.get()

    if not item or not amount or not category:
        messagebox.showerror("Error", "All fields required!")
        return

    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Amount must be numeric.")
        return

    save_expense(item, amount, category)
    messagebox.showinfo("Success", "Expense added successfully!")
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    refresh_table()

# ----------------------- FILTERING -----------------------
def apply_filters():
    df = load_data()

    month = month_var.get()
    category = filter_category_var.get()
    min_amt = min_amount_var.get()
    max_amt = max_amount_var.get()

    if month != "All":
        df = df[df["Month"] == int(month)]

    if category != "All":
        df = df[df["Category"] == category]

    if min_amt:
        df = df[df["Amount"] >= float(min_amt)]

    if max_amt:
        df = df[df["Amount"] <= float(max_amt)]

    refresh_table(df)
    update_summary(df)

# ----------------------- SUMMARY PANEL -----------------------
def update_summary(df):
    summary_total["text"] = f"${df['Amount'].sum():,.2f}"
    summary_avg["text"] = f"${df['Amount'].mean():,.2f}" if len(df)>0 else "$0.00"
    summary_max["text"] = f"${df['Amount'].max():,.2f}" if len(df)>0 else "$0.00"
    summary_count["text"] = str(len(df))

# ----------------------- EXPORT -----------------------
def export_filtered():
    df = table_to_dataframe()
    if df.empty:
        messagebox.showerror("Error", "No data to export.")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if filename:
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", "Exported successfully!")

# ----------------------- TABLE DISPLAY -----------------------
def table_to_dataframe():
    rows = []
    for row in table.get_children():
        rows.append(table.item(row)["values"])
    return pd.DataFrame(rows, columns=["Date", "Item", "Amount", "Category"])

def refresh_table(df=None):
    if df is None:
        df = load_data()

    for row in table.get_children():
        table.delete(row)

    for _, r in df.iterrows():
        table.insert("", tk.END, values=[r["Date"].strftime("%Y-%m-%d"), r["Item"], r["Amount"], r["Category"]])

# ----------------------- DASHBOARD -----------------------
def show_dashboard():
    df = load_data()

    if df.empty:
        messagebox.showerror("Error", "No data available.")
        return

    # -------- POPUP TO SELECT MONTH --------
    month_input = simpledialog.askinteger(
        "Select Month",
        "Enter month number (1–12):",
        minvalue=1,
        maxvalue=12
    )
    if month_input is None:
        return

    month_name = datetime(2024, month_input, 1).strftime("%B")
    selected_df = df[df["Month"] == month_input]

    # -------- COMPARISON MONTHS --------
    months_to_plot = [month_input]
    if month_input > 1:
        months_to_plot.append(month_input - 1)
    if month_input > 2:
        months_to_plot.append(month_input - 2)

    months_to_plot = sorted(months_to_plot)

    comparison_names = [datetime(2024, m, 1).strftime("%B") for m in months_to_plot]
    comparison_values = [df[df["Month"] == m]["Amount"].sum() for m in months_to_plot]

    # -------- DASHBOARD WINDOW --------
    dash = tk.Toplevel(root)
    dash.title("Analytics Dashboard")
    dash.geometry("1500x900")

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    plt.tight_layout(pad=6)

    # =========================================
    # 1️⃣ MONTHLY PIE CHART (NO % on slices)
    # Percentages shown in LEGEND instead
    # =========================================
    if len(selected_df) > 0:
        monthly_pie = selected_df.groupby("Category")["Amount"].sum()
    else:
        monthly_pie = pd.Series([1], index=["No Data"])

    total_month_amt = monthly_pie.sum()
    percent_labels = [
        f"{cat} ({round(val/total_month_amt*100,1)}%)"
        for cat, val in zip(monthly_pie.index, monthly_pie.values)
    ]

    axes[0][0].pie(
        monthly_pie.values,
        startangle=90,
        radius=1.2
    )
    axes[0][0].set_title(f"Monthly Breakdown ({month_name})", fontsize=14)

    axes[0][0].legend(
        percent_labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10
    )

    # =========================================
    # 2️⃣ COMPARISON BAR CHART
    # =========================================
    axes[0][1].bar(
        comparison_names,
        comparison_values,
        color=["#6A5ACD", "#4CAF50", "#FF9800"]
    )
    axes[0][1].set_title(f"{month_name} vs Previous Months", fontsize=14)
    axes[0][1].set_ylabel("Total Spending ($)", fontsize=12)

    # =========================================
    # 3️⃣ YEARLY CATEGORY PIE (LEGEND % ONLY)
    # =========================================
    yearly_pie = df.groupby("Category")["Amount"].sum()
    total_year_amt = yearly_pie.sum()
    year_percent = [
        f"{cat} ({round(val/total_year_amt*100,1)}%)"
        for cat, val in zip(yearly_pie.index, yearly_pie.values)
    ]

    axes[1][0].pie(
        yearly_pie.values,
        startangle=90,
        radius=1.2
    )
    axes[1][0].set_title("Yearly Spending Breakdown", fontsize=14)

    axes[1][0].legend(
        year_percent,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10
    )

    # =========================================
    # 4️⃣ CATEGORY MONTHLY TREND (LINE GRAPH)
    # =========================================
    trend = df.groupby(["Category", "Month"])["Amount"].sum().unstack(fill_value=0)

    for category in trend.index:
        axes[1][1].plot(
            trend.columns,
            trend.loc[category],
            marker="o",
            linewidth=2,
            label=category
        )

    axes[1][1].set_title("Category Monthly Trend", fontsize=14)
    axes[1][1].set_xlabel("Month")
    axes[1][1].set_ylabel("Amount")
    axes[1][1].legend(fontsize=6, loc="upper left")

    # =========================================
    # DRAW DASHBOARD
    # =========================================
    canvas = FigureCanvasTkAgg(fig, master=dash)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ============================================================
#                         GUI LAYOUT
# ============================================================

root = tk.Tk()
root.title("Professional Expense Tracker")
root.geometry("1300x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ----------------------- TAB 1: ADD EXPENSE -----------------------
tab1 = tk.Frame(notebook, bg="#eef2ff")
notebook.add(tab1, text="Add Expense")

tk.Label(tab1, text="Item:", bg="#eef2ff").pack()
entry_item = tk.Entry(tab1)
entry_item.pack()

tk.Label(tab1, text="Amount:", bg="#eef2ff").pack()
entry_amount = tk.Entry(tab1)
entry_amount.pack()

category_var = tk.StringVar()
tk.Label(tab1, text="Category:", bg="#eef2ff").pack()
ttk.Combobox(
    tab1,
    textvariable=category_var,
    values=[
        "Food", "Transport", "Housing", "Education", "Medical",
        "Insurance", "Utilities", "Shopping", "Fitness",
        "Entertainment"
    ]
).pack()

tk.Button(
    tab1,
    text="Add Expense",
    bg="#1FA055",
    fg="Black",
    font=("Arial", 12, "bold"),
    command=add_expense
).pack(pady=10)

# ----------------------- TAB 2: VIEW & FILTER -----------------------
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="View / Filter")

filter_frame = tk.Frame(tab2)
filter_frame.pack(side="left", fill="y", padx=10)

tk.Label(filter_frame, text="Filters", font=("Arial", 14, "bold")).pack()

month_var = tk.StringVar(value="All")
tk.Label(filter_frame, text="Month:").pack()
ttk.Combobox(filter_frame, textvariable=month_var, values=["All"] + [f"{i}" for i in range(1,13)]).pack()

filter_category_var = tk.StringVar(value="All")
tk.Label(filter_frame, text="Category:").pack()
ttk.Combobox(
    filter_frame,
    textvariable=filter_category_var,
    values=[
        "All", "Food", "Transport", "Housing", "Education",
        "Medical", "Insurance", "Utilities", "Shopping",
        "Fitness", "Entertainment"
    ]
).pack()

min_amount_var = tk.StringVar()
max_amount_var = tk.StringVar()

tk.Label(filter_frame, text="Min Amount:").pack()
tk.Entry(filter_frame, textvariable=min_amount_var).pack()

tk.Label(filter_frame, text="Max Amount:").pack()
tk.Entry(filter_frame, textvariable=max_amount_var).pack()

tk.Button(
    filter_frame,
    text="APPLY FILTERS",
    bg="#2D3BFF",
    fg="Blue",
    font=("Arial", 16, "bold"),
    command=apply_filters
).pack(pady=16)

tk.Button(
    filter_frame,
    text="EXPORT FILTERED CSV",
    bg="#C10F0F",
    fg="Red",
    font=("Arial", 16, "bold"),
    command=export_filtered
).pack()

# SUMMARY PANEL
summary_frame = tk.Frame(filter_frame, pady=20)
summary_frame.pack()

tk.Label(summary_frame, text="Summary", font=("Arial", 14, "bold")).pack()

tk.Label(summary_frame, text="Total Spending").pack()
summary_total = tk.Label(summary_frame, text="$0.00", font=("Arial", 12))
summary_total.pack()

tk.Label(summary_frame, text="Average Spending").pack()
summary_avg = tk.Label(summary_frame, text="$0.00")
summary_avg.pack()

tk.Label(summary_frame, text="Max Expense").pack()
summary_max = tk.Label(summary_frame, text="$0.00")
summary_max.pack()

tk.Label(summary_frame, text="Transactions").pack()
summary_count = tk.Label(summary_frame, text="0")
summary_count.pack()

# ----------------------- TABLE -----------------------
table_frame = tk.Frame(tab2)
table_frame.pack(side="right", fill="both", expand=True)

columns = ["Date", "Item", "Amount", "Category"]
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)

table.pack(fill="both", expand=True)

refresh_table()

# ----------------------- TAB 3: ANALYTICS -----------------------
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="Analytics")

tk.Button(
    tab3,
    text="OPEN FULL ANALYTICS DASHBOARD",
    bg="#6A5ACD",
    fg="Green",
    font=("Arial", 16, "bold"),
    command=show_dashboard
).pack(pady=60)

root.mainloop()
