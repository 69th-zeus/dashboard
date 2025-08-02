import streamlit as st
from stock import stock  # import your class here
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from data import *
sns.set(style='dark')

st.set_page_config(page_title="Dashboard", layout="wide")

# Sidebar Inputs
st.sidebar.title("Options")
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="MSFT")
view_mode = st.sidebar.radio("Select Your View Mode", ["Quarterly", 'Yearly'])
dummy_mode = st.sidebar.checkbox("Enable Dummy Mode")
plot_f = st.sidebar.checkbox("Plot Financial's Graphs")
plot_r = st.sidebar.checkbox("Plot Ratios' Graphs")
about_project = st.sidebar.checkbox("Display About Page")

def scale_df(df):
        columns = [x for x in df.columns if x not in ['Year', 'Quarter']]
        new_df = df[['Year', 'Quarter']] if 'Quarter' in df.columns else df[['Year']]
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
                new_df[new_col_name] = (df[column] / scale)
            else:
                new_df[column] = df[column]
            new_df.dropna(inplace = True)
        return new_df

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

def display_company_header():
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

    col1.metric("Exchange", exchange)
    col2.metric("Country", country)
    col3.metric("Ticker", ticker)

    st.markdown("---")

    # Financial Metrics Section
    st.subheader("📈 Valuation and Price Metrics")

    col4, col5, col6 = st.columns(3)

    render_metric(
        col4, "Current Price", f"${scale_number(current_price)}",
        HEADER_METRIC.get("Current Price")['formal'],
        HEADER_METRIC.get("Current Price")['casual'],
        latex_formula=HEADER_METRIC.get("Current Price")['latex'],
        interpretation_note=HEADER_METRIC.get("Current Price")['guide']
    )

    render_metric(
        col5, "Book Value", f"${scale_number(book_value)}",
        HEADER_METRIC.get("Book Value")['formal'],
        HEADER_METRIC.get("Book Value")['casual'],
        latex_formula=HEADER_METRIC.get("Book Value")['latex'],
        interpretation_note=HEADER_METRIC.get("Book Value")['guide']
    )

    render_metric(
        col6, "Market Cap", scale_number(market_cap),
        HEADER_METRIC.get("Market Cap")['formal'],
        HEADER_METRIC.get("Market Cap")['casual'],
        latex_formula=HEADER_METRIC.get("Market Cap")['latex'],
        interpretation_note=HEADER_METRIC.get("Market Cap")['guide']
    )

    render_metric(
        col4, "52-Week Low", f"${scale_number(fifty_two_week_low)}",
        HEADER_METRIC.get("52-Week Low")['formal'],
        HEADER_METRIC.get("52-Week Low")['casual'],
        latex_formula=HEADER_METRIC.get("52-Week Low").get('latex', None),
        interpretation_note=HEADER_METRIC.get("52-Week Low")['guide']
    )

    render_metric(
        col5, "52-Week High", f"${scale_number(fifty_two_week_high)}",
        HEADER_METRIC.get("52-Week High")['formal'],
        HEADER_METRIC.get("52-Week High")['casual'],
        latex_formula=HEADER_METRIC.get("52-Week High").get('latex', None),
        interpretation_note=HEADER_METRIC.get("52-Week High")['guide']
    )

    render_metric(
        col6, "Avg Volume (10D)", scale_number(avg_volume_10d),
        HEADER_METRIC.get("Avg Volume (10D)")['formal'],
        HEADER_METRIC.get("Avg Volume (10D)")['casual'],
        latex_formula=HEADER_METRIC.get("Avg Volume (10D)").get('latex', None),
        interpretation_note=HEADER_METRIC.get("Avg Volume (10D)")['guide']
    )

    st.markdown("---")
    st.subheader("📈 Earnings and Returns")

    col7, col8, col9 = st.columns(3)

    render_metric(
        col7, "Dividend Yield", f"{format_ratio(dividend_yield)}%",
        HEADER_METRIC.get("Dividend Yield")['formal'],
        HEADER_METRIC.get("Dividend Yield")['casual'],
        latex_formula=HEADER_METRIC.get("Dividend Yield").get('latex', None),
        interpretation_note=HEADER_METRIC.get("Dividend Yield")['guide']
    )

    render_metric(
        col8, "PE Ratio", format_ratio(pe_ratio),
        HEADER_METRIC.get("PE Ratio")['formal'],
        HEADER_METRIC.get("PE Ratio")['casual'],
        latex_formula=HEADER_METRIC.get("PE Ratio").get('latex', None),
        interpretation_note=HEADER_METRIC.get("PE Ratio")['guide']
    )

    render_metric(
        col9, "EPS (TTM)", format_ratio(eps),
        HEADER_METRIC.get("EPS (TTM)")['formal'],
        HEADER_METRIC.get("EPS (TTM)")['casual'],
        latex_formula=HEADER_METRIC.get("EPS (TTM)").get('latex', None),
        interpretation_note=HEADER_METRIC.get("EPS (TTM)")['guide']
    )

    render_metric(
        col7, "PEG Ratio", format_ratio(stock_obj.peg_ratio),
        HEADER_METRIC.get("PEG Ratio")['formal'],
        HEADER_METRIC.get("PEG Ratio")['casual'],
        latex_formula=HEADER_METRIC.get("PEG Ratio").get('latex', None),
        interpretation_note=HEADER_METRIC.get("PEG Ratio")['guide']
    )

    render_metric(
        col8, "P/B Ratio", format_ratio(stock_obj.pb_ratio),
        HEADER_METRIC.get("P/B Ratio")['formal'],
        HEADER_METRIC.get("P/B Ratio")['casual'],
        latex_formula=HEADER_METRIC.get("P/B Ratio").get('latex', None),
        interpretation_note=HEADER_METRIC.get("P/B Ratio")['guide']
    )

    st.markdown("---")
    st.subheader("📈 Advanced Valuation Metrics")

    col10, col11, col12 = st.columns(3)

    render_metric(
        col10, "EV/FCF", format_ratio(stock_obj.ev_fcf),
        HEADER_METRIC["EV/FCF"]["formal"],
         HEADER_METRIC["EV/FCF"]["casual"],
        latex_formula= HEADER_METRIC["EV/FCF"]["latex"],
        interpretation_note= HEADER_METRIC["EV/FCF"]["guide"]
    )

    render_metric(
        col11, "FCF Yield", f"{format_ratio(stock_obj.fcf_yield)}%",
        HEADER_METRIC["FCF Yield"]["formal"],
         HEADER_METRIC["FCF Yield"]["casual"],
        latex_formula= HEADER_METRIC["FCF Yield"]["latex"],
        interpretation_note= HEADER_METRIC["FCF Yield"]["guide"]
    )

    render_metric(
        col12, "EV/EBITDA", format_ratio(stock_obj.ev_ebit),
         HEADER_METRIC["EV/EBITDA"]["formal"],
         HEADER_METRIC["EV/EBITDA"]["casual"],
        latex_formula= HEADER_METRIC["EV/EBITDA"]["latex"],
        interpretation_note= HEADER_METRIC["EV/EBITDA"]["guide"]
    )

    render_metric(
        col10, "Dividend Payout Ratio", f"{format_ratio(stock_obj.dividend_payout_ratio)}%",
         HEADER_METRIC["Dividend Payout Ratio"]["formal"],
         HEADER_METRIC["Dividend Payout Ratio"]["casual"],
        latex_formula= HEADER_METRIC["Dividend Payout Ratio"]["latex"],
        interpretation_note= HEADER_METRIC["Dividend Payout Ratio"]["guide"]
    )


    st.subheader(f"📈 Historical Price Chart for {stock_obj.ticker}")

    if view_mode == 'Yearly':
        hist_data = stock_obj.ypricehistory
        report_dates = stock_obj.y_dates
    else:
        hist_data = stock_obj.qpricehistory
        report_dates = stock_obj.q_dates

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=hist_data.index,
                    open=hist_data['Open'],
                    high=hist_data['High'],
                    low=hist_data['Low'],
                    close=hist_data['Close'], name='Price'))
    
    for date in report_dates:
        fig.add_shape(
            type='line',
            x0=date,
            x1=date,
            y0=hist_data['Low'].min(),
            y1=hist_data['High'].max(),
            line=dict(color='royalblue', width=1, dash='dot'),
            xref='x',
            yref='y'
        )

    if view_mode == 'Yearly':
        fig.update_layout(
            title=f'{stock_obj.info.get("longName", stock_obj.ticker)} Stock Price Over Last 5 Years',
            yaxis_title=f'Price in {info.get("financialCurrency")}',
            xaxis_rangeslider_visible=True,
            hovermode='x unified',
            template='plotly_dark',
            height=800,
            yaxis=dict(
                fixedrange=False
            )
        )
    else:
        fig.update_layout(
            title=f'{stock_obj.info.get("longName", stock_obj.ticker)} Stock Price Over Last Year',
            yaxis_title=f'Price in {info.get("financialCurrency")}',
            xaxis_rangeslider_visible=True,
            hovermode='x unified',
            template='plotly',
            height=800,
            yaxis=dict(
                fixedrange=False
            )
        )
    st.plotly_chart(fig, use_container_width=True)
    
    if dummy_mode:
        with st.expander("📘 Click here for explanation"):
            st.markdown(HISTORICAL_CHART["formal"])
            st.markdown("---")
            st.markdown(HISTORICAL_CHART["casual"])
            st.markdown("---")
            st.markdown("🔍 **Interpretation Guide:**")
            st.markdown(HISTORICAL_CHART["guide"])

def display_grouped_financials_q():
    for group_name, cols in FINANCIAL_GROUPS_Q.items():
        available_cols = [col for col in cols if col in stock_obj.qfinancials.columns]

        st.subheader(f"📘 {group_name}")

        show_df = scale_df(stock_obj.qfinancials[["Year", "Quarter"] + available_cols])
        st.dataframe(show_df.reset_index(drop=True))

        if plot_f:
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
                    exp = FINANCIAL_METRIC_EXPLANATIONS_Q.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")

def display_grouped_ratios_q():
    def adjust_ratios(df):
        columns = [x for x in df.columns if x not in ['Year', 'Quarter']]
        new_df = df[['Year', 'Quarter']]
        for column in columns:
            new_df[column] = df[column].round(2)
        new_df.dropna(inplace = True)
        return new_df

    for group_name, cols in RATIO_GROUPS.items():
        available_cols = [col for col in cols if col in stock_obj.qratios.columns]
        if not available_cols:
            continue

        st.subheader(f"📘 {group_name}")
        show_df = adjust_ratios(stock_obj.qratios[["Year", "Quarter"] + available_cols])
        st.dataframe(show_df.reset_index(drop = True))

        if plot_r:
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

        if dummy_mode:
            with st.expander("📘 Explanation of Ratios"):
                for col in available_cols:
                    exp = RATIO_EXPLANATIONS.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")

def display_grouped_financials_y():
    for group_name, cols in FINANCIAL_GROUPS_Y.items():
        available_cols = [col for col in cols if col in stock_obj.yfinancials.columns]

        st.subheader(f"📘 {group_name}")

        show_df = scale_df(stock_obj.yfinancials[["Year"] + available_cols])
        st.dataframe(show_df.reset_index(drop = True))

        if plot_f:
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
                xaxis_title='Years',
                yaxis_title='Values',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Dummy Mode Explanation
        if dummy_mode:
            with st.expander("🧠 Learn About These Metrics"):
                for col in available_cols:
                    exp = FINANCIAL_METRIC_EXPLANATIONS_Y.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")

def display_grouped_ratios_y():
    def adjust_ratios(df):
        columns = [x for x in df.columns if x not in ['Year']]
        new_df = df[['Year']]
        for column in columns:
            new_df[column] = df[column].round(2)
        new_df.dropna(inplace = True)
        return new_df

    for group_name, cols in RATIO_GROUPS.items():
        available_cols = [col for col in cols if col in stock_obj.yratios.columns]
        if not available_cols:
            continue

        st.subheader(f"📘 {group_name}")
        show_df = adjust_ratios(stock_obj.yratios[["Year"] + available_cols])
        st.dataframe(show_df.reset_index(drop = True))

        if plot_r:
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
                xaxis_title='Years',
                yaxis_title='Values',
                hovermode='x unified',
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)

        if dummy_mode:
            with st.expander("📘 Explanation of Ratios"):
                for col in available_cols:
                    exp = RATIO_EXPLANATIONS.get(col)
                    if exp:
                        st.markdown(f"### 🔍 {col}")
                        st.markdown(exp["formal"])
                        if exp.get("latex"):
                            st.latex(exp["latex"])
                        st.markdown(exp["casual"])
                        st.markdown("🔎 **Interpretation Guide:**")
                        st.markdown(exp["guide"])
                        st.markdown("---")

def display_dupont_analysis(type):
    if type == 'q':
        latest_data = stock_obj.qratios.iloc[-1]
    else:
        latest_data = stock_obj.yratios.iloc[-1]

    npm = latest_data.get("Net Profit Margin", 0)
    asset_turnover = latest_data.get("Asset Turnover", 0)
    leverage = latest_data.get("Financial Leverage", 0)
    roe = latest_data.get("ROE", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Profit Margin", f"{npm:.2f}%", help="How much profit the company makes per dollar of sales.", label_visibility='visible')
    col2.metric("Asset Turnover", f"{asset_turnover:.2f}x", help="How efficiently the company uses its assets to generate sales.")
    col3.metric("Financial Leverage", f"{leverage:.2f}x", help="How much the company relies on debt to finance its assets.")
    col4.metric("Calculated ROE", f"{roe:.2f}%", help="The final return generated for shareholders.")

    if dummy_mode:
        with st.expander("📘 Click here for explanation of DuPont Analysis"):
            st.markdown(DUPONT_EXPLANATION["formal"])
            st.markdown("---")
            st.latex(DUPONT_EXPLANATION["latex"])
            st.markdown("---")
            st.markdown(DUPONT_EXPLANATION["casual"])
            st.markdown("---")
            st.markdown("🔍 **Interpretation Guide:**")
            st.markdown(DUPONT_EXPLANATION["guide"])

def display_piotroski_score():
    st.write("If The Company Issue No New Shares betwen Year in Index and the Previous Year then type 1 Otherwise 0 in the the below table")
    f_score_y = stock_obj.f_score_y
    new_shares_issued = st.data_editor(f_score_y["No New Shares Issued"],
                               key = 'piotroski_editor',
                               use_container_width= True,
                               disabled=['Year'])
    
    f_score_y["No New Shares Issued"] = new_shares_issued.astype(int)
    score_cols = [col for col in f_score_y.columns if col != "F Score"]
    f_score_y["F Score"] = f_score_y[score_cols].sum(axis = 1)

    st.dataframe(f_score_y)

    if dummy_mode:
        with st.expander("📘 Click here for explanation of Piotroski F-Score"):
            st.markdown(PIOTROSKI_EXPLANATION["formal"])
            st.markdown("---")
            st.markdown(PIOTROSKI_EXPLANATION["casual"])
            st.markdown("---")
            st.markdown("🔍 **Interpretation Guide:**")
            st.markdown(PIOTROSKI_EXPLANATION["guide"])

def get_data():
    stock_obj = stock(ticker)
    stock_obj.calculate_quarterly_ratios()
    stock_obj.calculate_yearly_ratios()
    stock_obj.one_time_ratios()
    stock_obj.piotroski_f_score_yearly()
    return stock_obj

def about_page():
    st.title("📘 About This Financial Dashboard")
    st.markdown(ABOUT_PAGE)

def main():
    global stock_obj
    if not about_project:
        if ticker:
            stock_obj = get_data()
            display_company_header()

            if view_mode == 'Quarterly':
                st.title("Financials")
                display_grouped_financials_q()
                st.title("Ratios")
                display_grouped_ratios_q()
                st.title("DuPont Analysis")
                display_dupont_analysis(type = 'q')
            elif view_mode == 'Yearly':
                st.title("Financials")
                display_grouped_financials_y()
                st.title("Ratios")
                display_grouped_ratios_y()
                st.title("DuPont Analysis")
                display_dupont_analysis(type = 'y')
                st.title("Piotroski F Score")
                display_piotroski_score()

            if stock_obj.errors:
                st.warning("⚠️ Some data couldn't be retrieved:")
                for err in stock_obj.errors:
                    st.text(f"- {err}")
    else:
        about_page()
        
main()