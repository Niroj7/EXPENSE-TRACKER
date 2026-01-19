<div align="center">

<h1><b>💰 PERSONAL EXPENSE TRACKER —- Personal Finance Manager</b></h1>
<h3><b>Tkinter + Streamlit + Python</b></h3>

A modern, end-to-end expense tracking system combining a Tkinter desktop application  
with a Streamlit analytics dashboard for deep financial insights.

</div>


---
<div align="center"> <h2><b>🔍 OVERVIEW</b></h2> </div>

The Expense Tracker is a simple and beginner-friendly financial tool that helps you record expenses and analyze your spending.
You add expenses through a Tkinter desktop app, and explore visual analytics using a Streamlit dashboard.

It is designed to be easy to use, visually clean, and perfect for showcasing your skills in Python, Tkinter, Pandas, and Streamlit.

-------------------------------

<div align="center">

<h2><b>⭐ FEATURES</b></h2>

<table>
<tr>

<td align="center" width="33%">
<h3><b>🧾 Add Expenses</b></h3>
<p>Quickly add items, amounts, and categories<br>Auto-saved to CSV</p>
</td>

<td align="center" width="33%">
<h3><b>🎛️ Smart Filters</b></h3>
<p>Filter by month & category<br>Min–max amount search</p>
</td>

<td align="center" width="33%">
<h3><b>📊 Visual Insights</b></h3>
<p>Pie charts • Trends • Bar charts<br>Category & monthly analytics</p>
</td>

</tr>
<tr>

<td align="center" width="33%">
<h3><b>📄 PDF Report</b></h3>
<p>Auto-generated summary<br>Downloadable for reporting</p>
</td>

<td align="center" width="33%">
<h3><b>🖥️ Clean UI</b></h3>
<p>Simple Tkinter interface<br>Beginner-friendly design</p>
</td>

<td align="center" width="33%">
<h3><b>🚀 Streamlit Dashboard</b></h3>
<p>Interactive charts & KPIs<br>Upload CSV for analytics</p>
</td>

</tr>
</table>

</div>

-------------------------------------


# 🌐 Live Streamlit Dashboard
👉 https://expense-tracker-kupudust2wwrzubaskytrd.streamlit.app


--------------------------------------------------------------------------------------------

**Visuals of  Streamlit Dashboard.**

---

<div align="center">
<table>
<tr>

<td align="center">
<img src="str 1.png" width="420"><br>
<sub>
<b>📁 Upload & Landing Page</b><br>
  <i>
    
    • Upload CSV to generate dashboard
    • Clean & modern UI design  
    • Validates file format instantly  
  </i>
</sub>
</td>

<td align="center">
<img src="str 2.png" width="420"><br>
<sub>
<b>📈 Category Overview</b><br>
  <i>
    
    • Pie chart of spending distribution  
    • Monthly spending trend line chart  
    • Filters by month & category  
</i>

</sub>
</td>

<td align="center">
<img src="str 3.png" width="420"><br>
<sub>
<b>📊 Advanced Analytics</b><br>
  <i>
    
       • Top spending categories bar chart  
       • Stacked monthly expense comparison  
       • Downloadable PDF report 
       
   
</sub>
</sub>
</td>

</tr>
</table>
</div>

---

# 🖥️ Tkinter Desktop Application (GUI)

Since GUI apps cannot run online, recruiters can preview the full interface using these screenshots.

---

## ✨ Add Expense Screen

Simple and fast input form for adding new expenses with item, amount, and category fields.

<div align="center">
<img src="gui 0.png" width="55%">
<br>
<sub>
<I>
  
        • Input fields for item, amount & category  
        • Auto-saves entries to CSV  
        • Clean & beginner-friendly layout  
</I>
</sub>
</div>

---

## ✨ View / Filter & Analytics Preview (Side-by-Side)

<table>
<tr>

<td align="center">
<b>📌 View / Filter</b><br>
<img src="gui 1.png" width="420"><br>
<sub>
  <I>
    
    • Filter by month, category, min/max amount  
    • Full table viewer for all expenses  
    • Export filtered results to CSV 
    
  </I> 

</sub>
</td>

<td align="center">
<b>📌 Monthly Breakdown</b><br>
<img src="gui 2.png" width="420"><br>
<sub>
  <I>
  
  
  
    Displays expenses filtered for May
    Supports category + min/max amount filtering
    Export filtered results to CSV
        
  </I>
        
</sub>

</td>

</tr>
</table>

---

## 📊 Yearly Breakdown & Monthly Trend

<table>
<tr>

<td align="center">
<b>📌 Yearly Breakdown</b><br>
<img src="gui 3.png" width="420"><br>
<sub>
  <I>
    
    Shows total spending distribution for the full year
    Highlights which categories you spent the most on
    Easy visual comparison across all expense categories
        
</I>
        

</sub>
</td>

<td align="center">
<b>📌 Monthly Trend Overview</b><br>
<img src="gui 3.png" width="420"><br>
<sub>
  <I>
        • Trendline for monthly spending  
        • Shows seasonal/recurring expenses  
        • Useful for budgeting forecasts 
  </I>
</sub>
</td>

</tr>
</table>

---
 ⚙️ **Tech Stack**

| Tool / Framework | Purpose |
|------------------|----------|
| **Python** | Core application logic |
| **Tkinter** | Desktop GUI interface |
| **Pandas** | Data processing & filtering |
| **Matplotlib** | chart visualizations in Tkinter |
| **Streamlit** | Interactive web dashboard |
| **FPDF** | Automated PDF report generation |
| **CSV** | Data storage for expenses |



---

# 📦 **Project Structure**
      
      EXPENSE-TRACKER
      │── data.csv
      │── Tracker.py
      │── tracker_gui.py
      │── streamlit_app.py
      │── gui 0.png
      │── gui 1.png
      │── gui 2.png
      │── gui 3.png
      │── str 1.png
      │── str 2.png
      │── str 3.png
      │── README.md

- -  -- - ----- -------------------

<h1>🚀 How to Run Locally</h1>

**✅ 1. Clone the Repository**

      git clone https://github.com/Niroj7/EXPENSE-TRACKER.git
      cd EXPENSE-TRACKER

**✅ 2. Install Dependencies**
       
        pip install -r requirements.txt

<b> 🖥️ 3. Run the Tkinter Desktop Application</b>
         
          python tracker_gui.py



**📊  Now Also Run the Streamlit Dashboard**

            streamlit run streamlit_app.py


**All expenses are saved to:**

              data.csv


  -----------------------
 <b>🌟 Happy Coding & Happy Learning!<b>




