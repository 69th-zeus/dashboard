import streamlit as st
from stock import stock  # import your class here
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
sns.set(style='dark')

st.set_page_config(page_title="Dashboard", layout="wide")

# Sidebar Inputs
st.sidebar.title("Options")
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="MSFT")
view_mode = st.sidebar.radio("Select Your View Mode", ["Latest", "Quarterly", 'Yearly'])
dummy_mode = st.sidebar.checkbox("Enable Dummy Mode")



def display_company_header(stock_obj):
    info = stock_obj.info

    # Helper Functions (do not edit these as per instruction)
    def scale_number(num):
        """Converts large numbers to a readable string."""
        if num is None:
            return "N/A"
        try:
            num = float(num)
            if abs(num) >= 1e12:
                return f"{num/1e12:.2f} Trillion"
            elif abs(num) >= 1e9:
                return f"{num/1e9:.2f} Billion"
            elif abs(num) >= 1e6:
                return f"{num/1e6:.2f} Million"
            elif abs(num) >= 1e3:
                return f"{num/1e3:.2f}K"
            else:
                return f"{num:.2f}"
        except:
            return str(num)

    def format_ratio(value):
        """Rounds ratios to 3 decimal places."""
        try:
            return round(float(value), 3)
        except:
            return "N/A"

    def render_metric(col, label, value, formal_explanation, casual_explanation, latex_formula=None, interpretation_note=None):
        """Renders Metrics on the Screen"""
        col.metric(label, value)
        if dummy_mode:
            with col.expander("📘 Click here for explanation"):
                st.markdown(formal_explanation)
                st.markdown("---")
                if latex_formula:
                    st.latex(latex_formula)
                    st.markdown("---")
                st.markdown(casual_explanation)
                if interpretation_note:
                    st.markdown("---")
                    st.markdown("🔍 **Interpretation Guide:**")
                    st.markdown(interpretation_note)

    # General Info
    company_name = info.get("longName", stock_obj.ticker)
    ceo = info.get("companyOfficers", [{}])[0].get("name", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    exchange = info.get("exchange", "N/A")
    country = info.get("country", "N/A")
    website = info.get("website", "")
    ticker = stock_obj.ticker

    # Financial Metrics
    current_price = info.get("currentPrice")
    book_value = info.get("bookValue")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    avg_volume_10d = info.get("averageDailyVolume10Day")
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")

    # Title
    st.title(f"📊 Financial Dashboard for {company_name}")
    if website:
        st.markdown(f"🌐 [Visit Website]({website})")

    # General Info Section
    st.subheader("🧾 Company Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("CEO", ceo)
    col2.metric("Sector", sector)
    col3.metric("Industry", industry)

    col4, col5, col6 = st.columns(3)
    col4.metric("Exchange", exchange)
    col5.metric("Country", country)
    col6.metric("Ticker", ticker)

    st.markdown("---")

    # Financial Metrics Section
    st.subheader("📈 Valuation and Price Metrics")

    col7, col8, col9 = st.columns(3)
    render_metric(
        col7, "Current Price", f"${scale_number(current_price)}",
        "**Current Price** is the latest trading price of the stock on the exchange.",
        "It's the price someone's willing to pay for the stock right now.",
        interpretation_note="This value is not that useful by itself — compare it with EPS, Book Value, or peers to judge whether it's high or low."
    )
    render_metric(
        col8, "Book Value", f"${scale_number(book_value)}",
        "**Book Value** is the total value of the company's assets minus liabilities, per share.",
        "Think of it as what's left if the company sold everything and paid off all the bills.",
        latex_formula=r"\text{Book Value} = \frac{\text{Assets} - \text{Liabilities}}{\text{Outstanding Shares}}",
        interpretation_note="If the stock price is below the book value, it could be undervalued — or in trouble. Use with caution and comparison."
    )
    render_metric(
        col9, "Market Cap", scale_number(market_cap),
        "**Market Capitalization** is the total market value of a company's outstanding shares.",
        "It's how much the market thinks the company is worth — or how expensive it is to buy the whole thing.",
        latex_formula=r"\text{Market Cap} = \text{Share Price} \times \text{Total Shares}",
        interpretation_note="- Less than $2B → Small-cap (riskier, high growth potential)\n - Between $2B-$10B → Mid-cap (balanced)\n - Greater than $10B → Large-cap (stable, less risky)\n\n **May be different in you country or exchange so verify**"
    )

    col10, col11, col12 = st.columns(3)
    render_metric(
        col10, "52-Week Low", f"${scale_number(fifty_two_week_low)}",
        "**52-Week Low** is the lowest price the stock traded at in the past year.",
        "The stock was this sad at some point last year — drama!",
        interpretation_note="If current price is near this, the stock might be undervalued (or struggling). Good for bargain hunters — Proceed with caution."
    )
    render_metric(
        col11, "52-Week High", f"${scale_number(fifty_two_week_high)}",
        "**52-Week High** is the highest price the stock traded at in the past year.",
        "This is the stock’s bragging moment — peak flex mode.",
        interpretation_note="If the current price is near this, the stock might be overbought — or performing exceptionally well."
    )
    render_metric(
        col12, "Avg Volume (10D)", scale_number(avg_volume_10d),
        "**Average Volume (10D)** is the average number of shares traded daily over the last 10 days.",
        "Basically, how much people have been buying/selling it lately.",
        interpretation_note="Higher volume = more liquidity and interest.\nSudden volume spikes often signal big news or sentiment changes."
    )

    st.markdown("---")
    st.subheader("📈 Earnings and Returns")

    col13, col14, col15 = st.columns(3)
    render_metric(
        col13, "Dividend Yield", f"{format_ratio(dividend_yield)}%",
        "**Dividend Yield** shows the return from dividends relative to the stock price.",
        "How much the company pays you back for holding its shares. Kind of like cashback but fancier.",
        latex_formula=r"\text{Dividend Yield} = \left( \frac{\text{Annual Dividend}}{\text{Price}} \right) \times 100",
        interpretation_note="- Greater Than 5% → High yield (check sustainability)\n - Between 2%–5% → Healthy for stable companies\n - Less than 2% → Low, common for growth stocks"
    )
    render_metric(
        col14, "PE Ratio", format_ratio(pe_ratio),
        "**P/E Ratio** compares the stock price to its earnings per share (EPS).",
        "How expensive the stock is based on how much it earns. High P/E = You're expecting future growth — or maybe just speculating..",
        latex_formula=r"\text{P/E Ratio} = \frac{\text{Price}}{\text{EPS}}",
        interpretation_note=" - Less than 15 → Could be undervalued or troubled\n - Between 15-25 → Normal range for many sectors\n - Greater Than 25 → Growth stock or overvaluation"
    )

    render_metric(
        col15, "EPS (TTM)", format_ratio(eps),
        "**Earnings Per Share (EPS)** represents a company's net profit divided by outstanding shares (TTM = last 12 months).",
        "This is your slice of the company’s pie. Bigger EPS? More pie!",
        latex_formula=r"\text{EPS} = \frac{\text{Net Income}}{\text{Shares Outstanding}}",
        interpretation_note="Compare EPS across years or with similar companies. Higher EPS generally signals better profitability."
    )

    col16, col17, _ = st.columns(3)
    render_metric(
        col16, "PEG Ratio", format_ratio(stock_obj.peg_ratio),
        "**PEG Ratio** adjusts the P/E ratio for expected earnings growth.",
        "It tells you if you're paying too much for growth — think of it as a smarter P/E. Under 1? Could be a bargain.",
        latex_formula=r"\text{PEG Ratio} = \frac{\text{P/E Ratio}}{\text{EPS Growth Rate (\%)}}",
        interpretation_note="- Less than 1 → Could be undervalued\n- Between 1–2 → Fairly valued for many growth stocks\n- Greater than 2 → Possibly overvalued unless rapid growth continues \n\n if N\A then either data not available or Growth Rate is Negative so it'll be a Meaningless Quantity. You can verify this Below"
    )
    render_metric(
        col17, "P/B Ratio", format_ratio(stock_obj.pb_ratio),
        "**P/B Ratio** compares the market price to the book value of the company.",
        "Basically: how much are you paying for every dollar of net assets? High P/B might mean high expectations — or hype.",
        latex_formula=r"\text{P/B Ratio} = \frac{\text{Market Price per Share}}{\text{Book Value per Share}}",
        interpretation_note="- Less than 1 → Possibly undervalued or distressed\n- Between 1–3 → Normal for many industries\n- Greater than 3 → Investors expect high returns or brand value"
    )

def display_grouped_financials_q(stock_obj, plot=True):

    def scale_df(df):
        columns = [x for x in df.columns if x not in ['Year', 'Quarter']]
        new_df = df[['Year', 'Quarter']]
        for column in columns:
            max_val = df[column].abs().max()
            if pd.isna(max_val):
                scale = 1
                suffix = ''
            elif max_val >= 1e12:
                scale = 1e12
                suffix = "(Trillions)"
            elif max_val >= 1e9:
                scale = 1e9
                suffix = "(Billions)"
            elif max_val >= 1e6:
                scale = 1e6
                suffix = "(Millions)"
            else:
                scale = 1
                suffix = ''
            
            if suffix != '':
                new_col_name = f"{column} {suffix}"
                new_df[new_col_name] = df[column] / scale
            else:
                new_df[column] = df[column]
        return new_df

    COLUMN_GROUPS = {
        "Revenue & Profitability": [
            "Revenue", "Gross Profit",
            "Operating Income", "Net Income",
        ],
        "QoQ Revenue & Profitability": [
            "Revenue QoQ", "Gross Profit QoQ",
            "Operating Income QoQ","Net Income QoQ"
        ],
        "Cash Flow": [
            "Operating Cash Flow",
            "Capital Expenditure", "Free Cash Flow"
        ],
        "QoQ Cash Flow": [
            "Operating Cash Flow QoQ",
            "Free Cash Flow QoQ"
        ],
        "Balance Sheet Overview": [
            "Total Assets", "Total Liabilities", "Equity"
        ],
        "Working Capital Components": [
            "Current Assets", "Current Liabilities", "Inventory", "Cash", "Receivables"
        ],
        "Efficiency Inputs": [
            "Invested Capital", "Retained Earnings", "EBIT", "EBIT QoQ"
        ],
        "EBIT QoQ": [
            "EBIT QoQ"
        ],
        "Working Capital Derived": [
            "Working Capital"
        ]
    }

    # Define your explanation dictionary
    metric_explanations = {
        "Revenue": {
            "formal": "**Revenue** is the total amount of income generated from normal business operations.",
            "casual": "It's the top line — how much money the company made before any costs.",
            "latex": None,
            "guide": "- Higher revenue usually signals business growth.\n- Compare over time and across competitors."
        },
        "Revenue QoQ": {
            "formal": "**Revenue QoQ** shows the percentage growth or decline in revenue compared to the previous quarter.",
            "casual": "Did they sell more stuff than last quarter? That's what this shows.",
            "latex": r"\text{Revenue QoQ} = \left(\frac{R_t - R_{t-1}}{R_{t-1}}\right) \times 100",
            "guide": "- Above 5% = solid growth.\n- Negative = shrinking — investigate why."
        },
        "Gross Profit": {
            "formal": "**Gross Profit** is Revenue minus Cost of Goods Sold (COGS).",
            "casual": "What’s left after making the product but before paying the bills.",
            "latex": r"\text{Gross Profit} = \text{Revenue} - \text{COGS}",
            "guide": "- Consistent growth is a positive sign.\n- Volatility may indicate pricing or cost issues."
        },
        "Gross Profit QoQ": {
            "formal": "**Gross Profit QoQ** shows quarter-over-quarter growth in gross profit.",
            "casual": "Is the raw profit chunk growing each quarter? This answers that.",
            "latex": r"\text{Gross Profit QoQ} = \left(\frac{GP_t - GP_{t-1}}{GP_{t-1}}\right) \times 100",
            "guide": "- Look for steady or improving trends.\n- Sudden dips may signal cost issues."
        },
        "Operating Income": {
            "formal": "**Operating Income** is earnings before interest and taxes (EBIT).",
            "casual": "Profit from actual operations, before the accountants get fancy.",
            "latex": r"\text{Operating Income} = \text{Gross Profit} - \text{Operating Expenses}",
            "guide": "- Healthy operating income means the core business is profitable."
        },
        "Operating Income QoQ": {
            "formal": "**Operating Income QoQ** shows the growth in operating income over quarters.",
            "casual": "Are operations getting more efficient or just lucky?",
            "latex": r"\text{OI QoQ} = \left(\frac{OI_t - OI_{t-1}}{OI_{t-1}}\right) \times 100",
            "guide": "- Consistent growth is very bullish.\n- Sharp drops may be red flags."
        },
        "Net Income": {
            "formal": "**Net Income** is total profit after all expenses, taxes, and costs.",
            "casual": "The bottom line. What the company *actually* keeps.",
            "latex": r"\text{Net Income} = \text{Revenue} - \text{Total Expenses}",
            "guide": "- A must-watch metric for investors.\n- Negative = company lost money."
        },
        "Net Income QoQ": {
            "formal": "**Net Income QoQ** shows percentage change in net income from previous quarter.",
            "casual": "Is the final profit moving in the right direction?",
            "latex": r"\text{Net Income QoQ} = \left(\frac{NI_t - NI_{t-1}}{NI_{t-1}}\right) \times 100",
            "guide": "- Positive trend = company’s becoming more profitable.\n- Volatility can be risky."
        },
        "Operating Cash Flow": {
            "formal": "**Operating Cash Flow (OCF)** is cash generated by core business activities.",
            "casual": "Cash coming in from day-to-day operations — not investments or loans.",
            "latex": None,
            "guide": "- Positive OCF shows the business can sustain itself.\n- Negative OCF is a warning sign."
        },
        "Operating Cash Flow QoQ": {
            "formal": "**OCF QoQ** shows the quarterly growth of operating cash flow.",
            "casual": "Are they bringing in more real money from business? That’s the check.",
            "latex": r"\text{OCF QoQ} = \left(\frac{OCF_t - OCF_{t-1}}{OCF_{t-1}}\right) \times 100",
            "guide": "- Growth means strong operational efficiency.\n- Decline = dig into why."
        },
        "Capital Expenditure": {
            "formal": "**Capital Expenditure (CapEx)** refers to funds used to acquire or upgrade assets.",
            "casual": "Big spending on buildings, equipment, or new tech.",
            "latex": None,
            "guide": "- High CapEx can mean growth plans.\n- But too much = watch cash burn."
        },
        "Free Cash Flow": {
            "formal": "**Free Cash Flow (FCF)** is the cash left after CapEx — it shows real financial strength.",
            "casual": "What’s left to invest, repay debt, or reward shareholders.",
            "latex": r"\text{FCF} = \text{Operating Cash Flow} - \text{CapEx}",
            "guide": "- Positive FCF is ideal.\n- Negative FCF could mean expansion or trouble."
        },
        "Free Cash Flow QoQ": {
            "formal": "**FCF QoQ** shows growth of Free Cash Flow across quarters.",
            "casual": "Is the leftover money growing or drying up?",
            "latex": r"\text{FCF QoQ} = \left(\frac{FCF_t - FCF_{t-1}}{FCF_{t-1}}\right) \times 100",
            "guide": "- Growth = more flexibility.\n- Decline = check cash burn reasons."
        },
        "Total Assets": {
            "formal": "**Total Assets** are everything the company owns — cash, buildings, inventory, etc.",
            "casual": "The entire pile of stuff the business owns.",
            "latex": r"\text{Assets} = \text{Liabilities} + \text{Equity}",
            "guide": "- Bigger assets can mean more power.\n- Look at asset quality, not just size."
        },
        "Total Liabilities": {
            "formal": "**Total Liabilities** represent all financial debts and obligations.",
            "casual": "What the company owes — loans, bills, etc.",
            "latex": None,
            "guide": "- Watch rising liabilities.\n- Compare to assets and equity."
        },
        "Equity": {
            "formal": "**Equity** is the residual value of assets after deducting liabilities.",
            "casual": "What’s left for shareholders after paying off debts.",
            "latex": r"\text{Equity} = \text{Assets} - \text{Liabilities}",
            "guide": "- Positive equity = good.\n- Negative = serious trouble."
        },
        "Current Assets": {
            "formal": "**Current Assets** are assets expected to be converted to cash within a year.",
            "casual": "Short-term stuff: cash, inventory, receivables.",
            "latex": None,
            "guide": "- High current assets = strong short-term position."
        },
        "Current Liabilities": {
            "formal": "**Current Liabilities** are obligations due within one year.",
            "casual": "Bills and debts due soon.",
            "latex": None,
            "guide": "- Compare with current assets to assess liquidity."
        },
        "Inventory": {
            "formal": "**Inventory** includes raw materials, work-in-progress, and finished goods.",
            "casual": "Stuff sitting in the warehouse, ready to sell.",
            "latex": None,
            "guide": "- Rising inventory with flat sales = warning.\n- Compare to revenue."
        },
        "Cash": {
            "formal": "**Cash** is liquid money the company holds.",
            "casual": "Money ready to use — no strings attached.",
            "latex": None,
            "guide": "- Higher cash = safety buffer.\n- Too much idle cash? Could be better used."
        },
        "Receivables": {
            "formal": "**Receivables** are amounts owed to the company by customers.",
            "casual": "Unpaid customer bills — money they’re still waiting on.",
            "latex": None,
            "guide": "- Rising receivables = strong sales OR poor collections."
        },
        "Invested Capital": {
            "formal": "**Invested Capital** is the total capital invested by shareholders and lenders.",
            "casual": "All the money put into running the business.",
            "latex": r"\text{Invested Capital} = \text{Equity} + \text{Debt} - \text{Cash}",
            "guide": "- Used in ROIC calculations.\n- Efficiency of this capital matters."
        },
        "Retained Earnings": {
            "formal": "**Retained Earnings** are profits reinvested into the company, not paid as dividends.",
            "casual": "Past profits the company kept instead of sharing.",
            "latex": None,
            "guide": "- Growth means profit reinvestment.\n- Too much = maybe no better use found."
        },
        "EBIT": {
            "formal": "**EBIT (Earnings Before Interest & Taxes)** is core profit from operations.",
            "casual": "The profit before banks or taxmen get involved.",
            "latex": r"\text{EBIT} = \text{Revenue} - \text{COGS} - \text{Operating Expenses}",
            "guide": "- Used in valuation and efficiency ratios.\n- Excludes tax & interest noise."
        },
        "EBIT QoQ": {
            "formal": "**EBIT QoQ** shows quarter-over-quarter growth in EBIT.",
            "casual": "Is the operating engine becoming more profitable?",
            "latex": r"\text{EBIT QoQ} = \left(\frac{EBIT_t - EBIT_{t-1}}{EBIT_{t-1}}\right) \times 100",
            "guide": "- Strong signal of operational strength if rising consistently."
        },
        "Working Capital": {
            "formal": "**Working Capital** is Current Assets minus Current Liabilities.",
            "casual": "Money left to run day-to-day operations.",
            "latex": r"\text{Working Capital} = \text{Current Assets} - \text{Current Liabilities}",
            "guide": "- Positive = healthy liquidity.\n- Negative = short-term trouble risk."
        }
    }

    for group_name, cols in COLUMN_GROUPS.items():
        available_cols = [col for col in cols if col in stock_obj.qfinancials.columns]

        st.subheader(f"📘 {group_name}")

        show_df = scale_df(stock_obj.qfinancials[["Year", "Quarter"] + available_cols])
        st.dataframe(show_df)

        if plot:
            plot_df = show_df.copy()
            plot_df['Quarter_Label'] = plot_df['Year'].astype(str) + ' Q' + plot_df['Quarter'].astype(str)

            fig = go.Figure()
            for col in plot_df.columns.difference(['Year', 'Quarter', 'Quarter_Label']):
                fig.add_trace(go.Scatter(
                    x=plot_df['Quarter_Label'],
                    y=plot_df[col],
                    mode='lines+markers',
                    name=col
                ))

            fig.update_layout(
                title=group_name,
                xaxis_title='Quarter',
                yaxis_title='Values',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Dummy Mode Explanation
        if dummy_mode:
            with st.expander("🧠 Learn About These Metrics"):
                for col in available_cols:
                    exp = metric_explanations.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")

def display_grouped_financials_y(stock_obj, plot=True):

    def scale_df(df):
        columns = [x for x in df.columns if x not in ['Year']]
        new_df = df[['Year']]
        for column in columns:
            max_val = df[column].abs().max()
            if pd.isna(max_val):
                scale = 1
                suffix = ''
            elif max_val >= 1e12:
                scale = 1e12
                suffix = "(Trillions)"
            elif max_val >= 1e9:
                scale = 1e9
                suffix = "(Billions)"
            elif max_val >= 1e6:
                scale = 1e6
                suffix = "(Millions)"
            else:
                scale = 1
                suffix = ''
            
            if suffix != '':
                new_col_name = f"{column} {suffix}"
                new_df[new_col_name] = df[column] / scale
            else:
                new_df[column] = df[column]
        return new_df

    COLUMN_GROUPS = {
        "Revenue & Profitability": [
            "Revenue", "Gross Profit",
            "Operating Income", "Net Income",
        ],
        "QoQ Revenue & Profitability": [
            "Revenue YoY", "Gross Profit YoY",
            "Operating Income YoY","Net Income YoY"
        ],
        "Cash Flow": [
            "Operating Cash Flow",
            "Capital Expenditure", "Free Cash Flow"
        ],
        "YoY Cash Flow": [
            "Operating Cash Flow YoY",
            "Free Cash Flow YoY"
        ],
        "Balance Sheet Overview": [
            "Total Assets", "Total Liabilities", "Equity"
        ],
        "Working Capital Components": [
            "Current Assets", "Current Liabilities", "Inventory", "Cash", "Receivables"
        ],
        "Efficiency Inputs": [
            "Invested Capital", "Retained Earnings", "EBIT"
        ],
        "EBIT YoY": [
            "EBIT YoY"
        ],
        "Working Capital Derived": [
            "Working Capital"
        ]
    }

    # Define your explanation dictionary
    metric_explanations = {
        "Revenue": {
            "formal": "**Revenue** is the total amount of income generated from normal business operations.",
            "casual": "It's the top line — how much money the company made before any costs.",
            "latex": None,
            "guide": "- Higher revenue usually signals business growth.\n- Compare over time and across competitors."
        },
        "Revenue QoQ": {
            "formal": "**Revenue QoQ** shows the percentage growth or decline in revenue compared to the previous quarter.",
            "casual": "Did they sell more stuff than last quarter? That's what this shows.",
            "latex": r"\text{Revenue QoQ} = \left(\frac{R_t - R_{t-1}}{R_{t-1}}\right) \times 100",
            "guide": "- Above 5% = solid growth.\n- Negative = shrinking — investigate why."
        },
        "Gross Profit": {
            "formal": "**Gross Profit** is Revenue minus Cost of Goods Sold (COGS).",
            "casual": "What’s left after making the product but before paying the bills.",
            "latex": r"\text{Gross Profit} = \text{Revenue} - \text{COGS}",
            "guide": "- Consistent growth is a positive sign.\n- Volatility may indicate pricing or cost issues."
        },
        "Gross Profit QoQ": {
            "formal": "**Gross Profit QoQ** shows quarter-over-quarter growth in gross profit.",
            "casual": "Is the raw profit chunk growing each quarter? This answers that.",
            "latex": r"\text{Gross Profit QoQ} = \left(\frac{GP_t - GP_{t-1}}{GP_{t-1}}\right) \times 100",
            "guide": "- Look for steady or improving trends.\n- Sudden dips may signal cost issues."
        },
        "Operating Income": {
            "formal": "**Operating Income** is earnings before interest and taxes (EBIT).",
            "casual": "Profit from actual operations, before the accountants get fancy.",
            "latex": r"\text{Operating Income} = \text{Gross Profit} - \text{Operating Expenses}",
            "guide": "- Healthy operating income means the core business is profitable."
        },
        "Operating Income QoQ": {
            "formal": "**Operating Income QoQ** shows the growth in operating income over quarters.",
            "casual": "Are operations getting more efficient or just lucky?",
            "latex": r"\text{OI QoQ} = \left(\frac{OI_t - OI_{t-1}}{OI_{t-1}}\right) \times 100",
            "guide": "- Consistent growth is very bullish.\n- Sharp drops may be red flags."
        },
        "Net Income": {
            "formal": "**Net Income** is total profit after all expenses, taxes, and costs.",
            "casual": "The bottom line. What the company *actually* keeps.",
            "latex": r"\text{Net Income} = \text{Revenue} - \text{Total Expenses}",
            "guide": "- A must-watch metric for investors.\n- Negative = company lost money."
        },
        "Net Income QoQ": {
            "formal": "**Net Income QoQ** shows percentage change in net income from previous quarter.",
            "casual": "Is the final profit moving in the right direction?",
            "latex": r"\text{Net Income QoQ} = \left(\frac{NI_t - NI_{t-1}}{NI_{t-1}}\right) \times 100",
            "guide": "- Positive trend = company’s becoming more profitable.\n- Volatility can be risky."
        },
        "Operating Cash Flow": {
            "formal": "**Operating Cash Flow (OCF)** is cash generated by core business activities.",
            "casual": "Cash coming in from day-to-day operations — not investments or loans.",
            "latex": None,
            "guide": "- Positive OCF shows the business can sustain itself.\n- Negative OCF is a warning sign."
        },
        "Operating Cash Flow QoQ": {
            "formal": "**OCF QoQ** shows the quarterly growth of operating cash flow.",
            "casual": "Are they bringing in more real money from business? That’s the check.",
            "latex": r"\text{OCF QoQ} = \left(\frac{OCF_t - OCF_{t-1}}{OCF_{t-1}}\right) \times 100",
            "guide": "- Growth means strong operational efficiency.\n- Decline = dig into why."
        },
        "Capital Expenditure": {
            "formal": "**Capital Expenditure (CapEx)** refers to funds used to acquire or upgrade assets.",
            "casual": "Big spending on buildings, equipment, or new tech.",
            "latex": None,
            "guide": "- High CapEx can mean growth plans.\n- But too much = watch cash burn."
        },
        "Free Cash Flow": {
            "formal": "**Free Cash Flow (FCF)** is the cash left after CapEx — it shows real financial strength.",
            "casual": "What’s left to invest, repay debt, or reward shareholders.",
            "latex": r"\text{FCF} = \text{Operating Cash Flow} - \text{CapEx}",
            "guide": "- Positive FCF is ideal.\n- Negative FCF could mean expansion or trouble."
        },
        "Free Cash Flow QoQ": {
            "formal": "**FCF QoQ** shows growth of Free Cash Flow across quarters.",
            "casual": "Is the leftover money growing or drying up?",
            "latex": r"\text{FCF QoQ} = \left(\frac{FCF_t - FCF_{t-1}}{FCF_{t-1}}\right) \times 100",
            "guide": "- Growth = more flexibility.\n- Decline = check cash burn reasons."
        },
        "Total Assets": {
            "formal": "**Total Assets** are everything the company owns — cash, buildings, inventory, etc.",
            "casual": "The entire pile of stuff the business owns.",
            "latex": r"\text{Assets} = \text{Liabilities} + \text{Equity}",
            "guide": "- Bigger assets can mean more power.\n- Look at asset quality, not just size."
        },
        "Total Liabilities": {
            "formal": "**Total Liabilities** represent all financial debts and obligations.",
            "casual": "What the company owes — loans, bills, etc.",
            "latex": None,
            "guide": "- Watch rising liabilities.\n- Compare to assets and equity."
        },
        "Equity": {
            "formal": "**Equity** is the residual value of assets after deducting liabilities.",
            "casual": "What’s left for shareholders after paying off debts.",
            "latex": r"\text{Equity} = \text{Assets} - \text{Liabilities}",
            "guide": "- Positive equity = good.\n- Negative = serious trouble."
        },
        "Current Assets": {
            "formal": "**Current Assets** are assets expected to be converted to cash within a year.",
            "casual": "Short-term stuff: cash, inventory, receivables.",
            "latex": None,
            "guide": "- High current assets = strong short-term position."
        },
        "Current Liabilities": {
            "formal": "**Current Liabilities** are obligations due within one year.",
            "casual": "Bills and debts due soon.",
            "latex": None,
            "guide": "- Compare with current assets to assess liquidity."
        },
        "Inventory": {
            "formal": "**Inventory** includes raw materials, work-in-progress, and finished goods.",
            "casual": "Stuff sitting in the warehouse, ready to sell.",
            "latex": None,
            "guide": "- Rising inventory with flat sales = warning.\n- Compare to revenue."
        },
        "Cash": {
            "formal": "**Cash** is liquid money the company holds.",
            "casual": "Money ready to use — no strings attached.",
            "latex": None,
            "guide": "- Higher cash = safety buffer.\n- Too much idle cash? Could be better used."
        },
        "Receivables": {
            "formal": "**Receivables** are amounts owed to the company by customers.",
            "casual": "Unpaid customer bills — money they’re still waiting on.",
            "latex": None,
            "guide": "- Rising receivables = strong sales OR poor collections."
        },
        "Invested Capital": {
            "formal": "**Invested Capital** is the total capital invested by shareholders and lenders.",
            "casual": "All the money put into running the business.",
            "latex": r"\text{Invested Capital} = \text{Equity} + \text{Debt} - \text{Cash}",
            "guide": "- Used in ROIC calculations.\n- Efficiency of this capital matters."
        },
        "Retained Earnings": {
            "formal": "**Retained Earnings** are profits reinvested into the company, not paid as dividends.",
            "casual": "Past profits the company kept instead of sharing.",
            "latex": None,
            "guide": "- Growth means profit reinvestment.\n- Too much = maybe no better use found."
        },
        "EBIT": {
            "formal": "**EBIT (Earnings Before Interest & Taxes)** is core profit from operations.",
            "casual": "The profit before banks or taxmen get involved.",
            "latex": r"\text{EBIT} = \text{Revenue} - \text{COGS} - \text{Operating Expenses}",
            "guide": "- Used in valuation and efficiency ratios.\n- Excludes tax & interest noise."
        },
        "EBIT QoQ": {
            "formal": "**EBIT QoQ** shows quarter-over-quarter growth in EBIT.",
            "casual": "Is the operating engine becoming more profitable?",
            "latex": r"\text{EBIT QoQ} = \left(\frac{EBIT_t - EBIT_{t-1}}{EBIT_{t-1}}\right) \times 100",
            "guide": "- Strong signal of operational strength if rising consistently."
        },
        "Working Capital": {
            "formal": "**Working Capital** is Current Assets minus Current Liabilities.",
            "casual": "Money left to run day-to-day operations.",
            "latex": r"\text{Working Capital} = \text{Current Assets} - \text{Current Liabilities}",
            "guide": "- Positive = healthy liquidity.\n- Negative = short-term trouble risk."
        }
    }

    for group_name, cols in COLUMN_GROUPS.items():
        available_cols = [col for col in cols if col in stock_obj.yfinancials.columns]

        st.subheader(f"📘 {group_name}")

        show_df = scale_df(stock_obj.yfinancials[["Year"] + available_cols])
        st.dataframe(show_df)

        if plot:
            plot_df = show_df.copy()

            fig = go.Figure()
            for col in plot_df.columns.difference(['Year']):
                fig.add_trace(go.Scatter(
                    x=plot_df['Year'],
                    y=plot_df[col],
                    mode='lines+markers',
                    name=col
                ))

            fig.update_layout(
                title=group_name,
                xaxis_title='Quarter',
                yaxis_title='Values',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Dummy Mode Explanation
        if dummy_mode:
            with st.expander("🧠 Learn About These Metrics"):
                for col in available_cols:
                    exp = metric_explanations.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")


# --- Load Stock Data ---
if ticker:
    stock_obj = stock(ticker)
    stock_obj.calculate_quarterly_ratios()
    stock_obj.calculate_yearly_ratios()

    display_company_header(stock_obj)

    # --- Display Mode Logic ---
    if view_mode == "Latest":
        st.subheader("📅 Latest Quarter")
    elif view_mode == 'Quarterly':
        display_grouped_financials_q(stock_obj)
    elif view_mode == 'Yearly':
        display_grouped_financials_y(stock_obj)

