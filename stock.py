import yfinance as yf
import numpy as np
import pandas as pd

class stock():
    def __init__(self, ticker):
        # Intilializing Data Points
        self.ticker = ticker
        self.stock = yf.Ticker(self.ticker)
        
        # Getting Quarterly Data from yfinance
        self.q_income_stmt = self.stock.quarterly_financials.T.sort_index()
        self.q_balance_sheet = self.stock.quarterly_balance_sheet.T.sort_index()
        self.q_cashflow_stmt = self.stock.quarterly_cashflow.T.sort_index()
        self.info = self.stock.info

        # Getting yearly Data from yfinance
        self.y_income_stmt = self.stock.financials.T.sort_index()
        self.y_balance_sheet = self.stock.balance_sheet.T.sort_index()
        self.y_cashflow_stmt = self.stock.cashflow.T.sort_index()
        self.info = self.stock.info
        
        # Calculating Some Basic Things
        self.q_dates = self.q_income_stmt.index.intersection(self.q_balance_sheet.index).intersection(self.q_cashflow_stmt.index)
        self.y_dates = self.y_income_stmt.index.intersection(self.y_balance_sheet.index).intersection(self.y_cashflow_stmt.index)
        self.qratios = pd.DataFrame(index=self.q_dates)
        self.qfinancials = pd.DataFrame(index=self.q_dates)
        self.qratios['Quarter'] = self.q_dates.to_series().apply(lambda x:((x.month - 1) // 3) + 1)
        self.qratios['Year'] = self.q_dates.to_series().apply(lambda x:x.year)
        self.qfinancials['Quarter'] = self.q_dates.to_series().apply(lambda x:((x.month - 1) // 3) + 1)
        self.qfinancials['Year'] = self.q_dates.to_series().apply(lambda x:x.year)
        self.latest_quarter = self.q_dates[-1]
        self.latest_year = self.y_dates[-1]
    
    def get_safe_value(self, df, key, date, default=np.nan):
        series = df.get(key)
        return series.get(date) if series is not None else default

    def calculate_quarterly_ratios(self):
        for date in self.q_dates:
            try:
                # Calculating Financials
                revenue = self.q_income_stmt.loc[date, "Total Revenue"]
                net_income = self.q_income_stmt.loc[date, "Net Income"]
                gross_profit = self.q_income_stmt.loc[date, "Gross Profit"]
                operating_income = self.q_income_stmt.loc[date, "Operating Income"]
                total_assets = self.q_balance_sheet.loc[date, "Total Assets"]
                total_liabilities = self.q_balance_sheet.loc[date, "Total Liabilities Net Minority Interest"]
                equity = self.q_balance_sheet.loc[date, "Stockholders Equity"]
                current_assets = self.q_balance_sheet.loc[date, "Current Assets"]
                current_liabilities = self.q_balance_sheet.loc[date, "Current Liabilities"]
                
                inventory = self.get_safe_value(self.q_balance_sheet, "Inventory", date, default=np.nan)
                cash = self.get_safe_value(self.q_balance_sheet, "Cash And Cash Equivalents", date, default=np.nan)
                receivables = self.get_safe_value(self.q_balance_sheet, "Accounts Receivable", date, default=np.nan)
                invested_capital = self.get_safe_value(self.q_balance_sheet, "Invested Capital", date, default=np.nan)
                retained_earnings = self.get_safe_value(self.q_balance_sheet, "Retained Earnings", date, default=np.nan)
                ebit = self.get_safe_value(self.q_income_stmt, "EBIT", date, default=np.nan)
                if pd.isna(ebit):
                    ebit = self.get_safe_value(self.q_income_stmt, "Operating Income", date, default=np.nan)

                op_cash_flow = self.q_cashflow_stmt.loc[date, "Operating Cash Flow"]
                capex = self.get_safe_value(self.q_cashflow_stmt, "Capital Expenditure", date, default=0)
                free_cash_flow = op_cash_flow - capex
                working_capital = current_assets - current_liabilities

                # Storing the above Financials
                self.qfinancials.loc[date, "Revenue"] = revenue
                self.qfinancials.loc[date, "Net Income"] = net_income
                self.qfinancials.loc[date, "Gross Profit"] = gross_profit
                self.qfinancials.loc[date, "Operating Income"] = operating_income

                self.qfinancials.loc[date, "Total Assets"] = total_assets
                self.qfinancials.loc[date, "Total Liabilities"] = total_liabilities
                self.qfinancials.loc[date, "Equity"] = equity
                self.qfinancials.loc[date, "Current Assets"] = current_assets
                self.qfinancials.loc[date, "Current Liabilities"] = current_liabilities
                self.qfinancials.loc[date, "Inventory"] = inventory
                self.qfinancials.loc[date, "Cash"] = cash
                self.qfinancials.loc[date, "Receivables"] = receivables
                self.qfinancials.loc[date, "Invested Capital"] = invested_capital
                self.qfinancials.loc[date, "Retained Earnings"] = retained_earnings
                self.qfinancials.loc[date, "EBIT"] = ebit
                self.qfinancials.loc[date, "Free Cash Flow"] = free_cash_flow

                self.qfinancials.loc[date, "Operating Cash Flow"] = op_cash_flow
                self.qfinancials.loc[date, "Capital Expenditure"] = capex
                self.qfinancials.loc[date, "Free Cash Flow"] = free_cash_flow
                self.qfinancials.loc[date, "Working Capital"] = working_capital

                # Calculating and storing Financials
                self.qratios.loc[date, "Net Profit Margin"] = net_income / revenue
                self.qratios.loc[date, "Gross Margin"] = gross_profit / revenue
                self.qratios.loc[date, "Operating Margin"] = operating_income / revenue
                self.qratios.loc[date, "ROA"] = net_income / total_assets
                self.qratios.loc[date, "ROE"] = net_income / equity
                self.qratios.loc[date, "Current Ratio"] = current_assets / current_liabilities
                self.qratios.loc[date, "Quick Ratio"] = (current_assets - inventory) / current_liabilities
                self.qratios.loc[date, "Cash Ratio"] = cash / current_liabilities
                self.qratios.loc[date, "Debt-to-Equity"] = total_liabilities / equity
                self.qratios.loc[date, "Debt Ratio"] = total_liabilities / total_assets
                self.qratios.loc[date, "Cash Flow Margin"] = op_cash_flow / revenue
                self.qratios.loc[date, "Inventory Turnover"] = revenue / inventory if inventory else np.nan
                self.qratios.loc[date, "Asset Turnover"] = revenue / total_assets
                self.qratios.loc[date, "Receivables Turnover"] = revenue / receivables if receivables else np.nan
                self.qratios.loc[date, "CapEx Intensity"] = capex / revenue if revenue else np.nan
                self.qratios.loc[date, "ROCE"] = operating_income / invested_capital if invested_capital else np.nan
                self.qratios.loc[date, "FCF Conversion"] = free_cash_flow / net_income if net_income else np.nan

                # Altman-Z Score
                market_cap = self.info.get("marketCap")
                if all(pd.notnull([working_capital, total_assets, retained_earnings, ebit, market_cap, total_liabilities, revenue])):
                    A = working_capital / total_assets
                    B = retained_earnings / total_assets
                    C = ebit / total_assets
                    D = market_cap / total_liabilities
                    E = revenue / total_assets
                    z_score = 1.2 * A + 1.4 * B + 3.3 * C + 0.6 * D + 1.0 * E
                    self.qratios.loc[date, "Altman Z-Score"] = z_score
                else:
                    self.qratios.loc[date, "Altman Z-Score"] = np.nan

                # PEG, P/B, Integerst Coverage for Last Quarter
                if date == self.latest_quarter:
                    trailing_pe = self.info.get("trailingPE", None)
                    eps_growth = self.info.get("earningsGrowth", None)  # Usually in decimal (e.g. 0.12)
                    print(trailing_pe, eps_growth)
                    self.peg_ratio = trailing_pe / (eps_growth * 100) if trailing_pe and eps_growth and eps_growth > 0 else "N/A"

                    
                    # Data Not Available
                    # interest_expense = self.q_income_stmt.get("Interest Expense", pd.Series([np.nan])).get(date)
                    # interest_coverage = ebit / abs(interest_expense) if interest_expense and interest_expense != 0 else np.nan
                    # self.ratios.loc[date, "Interest Coverage"] = interest_coverage

                    current_price = self.info.get("currentPrice")
                    shares_outstanding = self.info.get("sharesOutstanding")
                    book_value_per_share = equity / shares_outstanding if shares_outstanding else np.nan
                    self.pb_ratio = current_price / book_value_per_share if book_value_per_share else np.nan

                    growth_cols = [ "Revenue", "Net Income", "Gross Profit", "Operating Income", "Operating Cash Flow", "Free Cash Flow", "EBIT" ]

                    for col in growth_cols:
                        if col in self.qfinancials.columns:
                            self.qfinancials[f"{col} QoQ"] = self.qfinancials[col].pct_change(fill_value=np.nan, fill_method=None).round(4) * 100

            except Exception as e:
                print(f"[{date}] Skipped due to error: {e}")
        
        self.format_ratios(type = 'q')
        self.qfinancials.dropna()
        self.qratios.dropna()

    def calculate_yearly_ratios(self):
        self.yratios = pd.DataFrame(index=self.y_dates)
        self.yfinancials = pd.DataFrame(index=self.y_dates)
        self.yfinancials['Year'] = self.y_dates.to_series().apply(lambda x: x.year)

        for date in self.y_dates:
            try:
                # Pull values from yearly financials
                revenue = self.y_income_stmt.loc[date, "Total Revenue"]
                net_income = self.y_income_stmt.loc[date, "Net Income"]
                gross_profit = self.y_income_stmt.loc[date, "Gross Profit"]
                operating_income = self.y_income_stmt.loc[date, "Operating Income"]
                total_assets = self.y_balance_sheet.loc[date, "Total Assets"]
                total_liabilities = self.y_balance_sheet.loc[date, "Total Liabilities Net Minority Interest"]
                equity = self.y_balance_sheet.loc[date, "Stockholders Equity"]
                current_assets = self.y_balance_sheet.loc[date, "Current Assets"]
                current_liabilities = self.y_balance_sheet.loc[date, "Current Liabilities"]

                inventory = self.get_safe_value(self.y_balance_sheet, "Inventory", date)
                cash = self.get_safe_value(self.y_balance_sheet, "Cash And Cash Equivalents", date)
                receivables = self.get_safe_value(self.y_balance_sheet, "Accounts Receivable", date)
                invested_capital = self.get_safe_value(self.y_balance_sheet, "Invested Capital", date)
                retained_earnings = self.get_safe_value(self.y_balance_sheet, "Retained Earnings", date)
                ebit = self.get_safe_value(self.y_income_stmt, "EBIT", date)
                if pd.isna(ebit):
                    ebit = self.get_safe_value(self.y_income_stmt, "Operating Income", date)

                op_cash_flow = self.y_cashflow_stmt.loc[date, "Operating Cash Flow"]
                capex = self.get_safe_value(self.y_cashflow_stmt, "Capital Expenditure", date, default=0)
                free_cash_flow = op_cash_flow - capex
                working_capital = current_assets - current_liabilities

                # Store financials
                self.yfinancials.loc[date, "Revenue"] = revenue
                self.yfinancials.loc[date, "Net Income"] = net_income
                self.yfinancials.loc[date, "Gross Profit"] = gross_profit
                self.yfinancials.loc[date, "Operating Income"] = operating_income
                self.yfinancials.loc[date, "Total Assets"] = total_assets
                self.yfinancials.loc[date, "Total Liabilities"] = total_liabilities
                self.yfinancials.loc[date, "Equity"] = equity
                self.yfinancials.loc[date, "Current Assets"] = current_assets
                self.yfinancials.loc[date, "Current Liabilities"] = current_liabilities
                self.yfinancials.loc[date, "Inventory"] = inventory
                self.yfinancials.loc[date, "Cash"] = cash
                self.yfinancials.loc[date, "Receivables"] = receivables
                self.yfinancials.loc[date, "Invested Capital"] = invested_capital
                self.yfinancials.loc[date, "Retained Earnings"] = retained_earnings
                self.yfinancials.loc[date, "EBIT"] = ebit
                self.yfinancials.loc[date, "Operating Cash Flow"] = op_cash_flow
                self.yfinancials.loc[date, "Capital Expenditure"] = capex
                self.yfinancials.loc[date, "Free Cash Flow"] = free_cash_flow
                self.yfinancials.loc[date, "Working Capital"] = working_capital

                # Ratios
                self.yratios.loc[date, "Net Profit Margin"] = net_income / revenue
                self.yratios.loc[date, "Gross Margin"] = gross_profit / revenue
                self.yratios.loc[date, "Operating Margin"] = operating_income / revenue
                self.yratios.loc[date, "ROA"] = net_income / total_assets
                self.yratios.loc[date, "ROE"] = net_income / equity
                self.yratios.loc[date, "Current Ratio"] = current_assets / current_liabilities
                self.yratios.loc[date, "Quick Ratio"] = (current_assets - inventory) / current_liabilities
                self.yratios.loc[date, "Cash Ratio"] = cash / current_liabilities
                self.yratios.loc[date, "Debt-to-Equity"] = total_liabilities / equity
                self.yratios.loc[date, "Debt Ratio"] = total_liabilities / total_assets
                self.yratios.loc[date, "Cash Flow Margin"] = op_cash_flow / revenue
                self.yratios.loc[date, "Inventory Turnover"] = revenue / inventory if inventory else np.nan
                self.yratios.loc[date, "Asset Turnover"] = revenue / total_assets
                self.yratios.loc[date, "Receivables Turnover"] = revenue / receivables if receivables else np.nan
                self.yratios.loc[date, "CapEx Intensity"] = capex / revenue if revenue else np.nan
                self.yratios.loc[date, "ROCE"] = operating_income / invested_capital if invested_capital else np.nan
                self.yratios.loc[date, "FCF Conversion"] = free_cash_flow / net_income if net_income else np.nan

                growth_cols = [ "Revenue", "Net Income", "Gross Profit", "Operating Income",    "Operating Cash Flow", "Free Cash Flow", "EBIT" ]

                for col in growth_cols:
                    if col in self.yfinancials.columns:
                        self.yfinancials[f"{col} YoY"] = self.yfinancials[col].pct_change(fill_value=np.nan, fill_method=None).round(4) * 100
            except Exception as e:
                print(f"[Yearly {date}] Skipped due to error: {e}")

        # Optional: format like quarterly
        self.format_ratios(type = 'y')
        self.yfinancials.dropna(inplace = True)
        self.yratios.dropna(inplace=True)

    def format_ratios(self, type):
        percent_columns = [
            "Net Profit Margin", "Gross Margin", "Operating Margin",
            "ROA", "ROE", "Cash Flow Margin", "CapEx Intensity",
            "FCF Conversion"
        ]

        ratio_columns = [
            "Current Ratio", "Quick Ratio", "Cash Ratio",
            "Debt-to-Equity", "Debt Ratio", "Inventory Turnover",
            "Asset Turnover", "Receivables Turnover",
            "ROCE", "Altman Z-Score", "PEG Ratio", "Price-to-Book"
        ]

        if type == 'q':
            for col in percent_columns:
                if col in self.qratios.columns:
                    self.qratios[col] = self.qratios[col].round(5)

            for col in ratio_columns:
                if col in self.qratios.columns:
                    self.qratios[col] = self.qratios[col].round(4)
        elif type == 'r':
            for col in percent_columns:
                if col in self.yratios.columns:
                    self.yratios[col] = self.yratios[col].round(5)

            for col in ratio_columns:
                if col in self.yratios.columns:
                    self.yratios[col] = self.yratios[col].round(4)