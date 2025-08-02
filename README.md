Welcome to this **Financial Dashboard**, an educational tool designed to analyze public companies using real financial data.  
It offers both **insightful analysis** for investors and **guided explanations** for learners through **Dummy Mode**.

---

📦 Tech Stack - 
- 🐍 Python 3.11+

- 🔹 Streamlit

- 📊 Plotly

- 🟦 yfinance

- 🧮 pandas, numpy

- 🎨 seaborn, matplotlib

---

### 🔍 What This Project Does
- Retrieves real-time **financial statements** from Yahoo Finance (Income, Balance Sheet, Cash Flow)
- Computes over **30+ financial ratios and metrics**
- Presents **historical stock prices** with quarterly and yearly overlays
- Supports **interactive plotting** for visual trend analysis
- Offers advanced insights through:
    - 📊 **Piotroski F-Score**
    - 🧮 **DuPont Analysis**
    - 💡 **Valuation ratios** (PEG, EV/EBITDA, FCF Yield, P/B, etc.)

---

### 🧠 What is Dummy Mode?

When enabled, it transforms every metric card into an **interactive explanation module**.

Each metric comes with:
- 📘 **Formal definition**  
- 😄 **Casual description**  
- 🧮 **LaTeX-based formula**  
- 🔍 **Interpretation guide**

> ✅ Use Dummy Mode to understand *what a metric means*, *how it's calculated*, and *why it matters*.

**How to Enable:**
- Go to the **Sidebar** → Enable ✅ `Dummy Mode`

---

### 🛠 Key Features Overview

| Feature | Description |
|--------|-------------|
| 📈 **Metric Cards** | Key financial metrics with optional explanations |
| 📉 **Interactive Charts** | Stock price plots with earnings highlights |
| 🧠 **Dummy Mode** | Learn what every number means |
| 📊 **Grouped Tables** | Financials and ratios grouped by type (profitability, liquidity, etc.) |
| 📈 **Advanced Analysis** | Includes Piotroski F-Score and DuPont breakdown |
| 🧾 **Quarterly & Yearly Modes** | View short-term vs long-term trends |

---

### ⚠ Approximations & Data Limitations

This dashboard uses Yahoo Finance APIs, which means some limitations apply:

- **Missing Fields**: Yahoo Finance does not always provide:
    - Equity Issuance (used in Piotroski)
    - Some CapEx breakdowns
    - Interest Burden / Effective Tax Rate (for full DuPont)
- **Simplified Models**: Where full decomposition isn't possible, simplified formulas are used

📌 **These can cause differences** compared to platforms like Bloomberg, GuruFocus, or TIKR.

---

### 📢 Please Verify Before Using!

Do **not** make investment decisions without verifying metrics using reliable sources like:

- SEC EDGAR Filings
- Yahoo Finance (manually)
- Morningstar
- TIKR or Koyfin

The dashboard does not replace due diligence.

---

### 💾 Save Your Dashboard View (PDF Export)

You can save your dashboard as a PDF report by printing the page.

**To do this safely:**
1. Press **`Ctrl + P`** or open browser’s **Print → Save as PDF**
2. Before saving, ensure:
    - ✅ "Background graphics" is **enabled**
    - ✅ Zoom is set to **80%**
    - ✅ Layout is **Landscape**
    - ✅ Expand all desired explanation sections which you want in the final PDF

> 🔐 This avoids content getting cut off or omitted

---

### 🙌 Thank You!

This tool was built to **empower your financial analysis** and make learning metrics **easier and fun**.  
If you enjoy it or want to contribute new ideas, feel free to fork or expand this project!