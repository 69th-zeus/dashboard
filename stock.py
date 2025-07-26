import yfinance as yf
import numpy as np
import pandas as pd

class stock():
    def __init__(self, ticker):
        # Intilializing Data Points
        self.ticker = ticker
        self.stock = yf.Ticker(self.ticker)

        self.errors = []
        
        try:
            self.q_income_stmt = self.stock.quarterly_financials.T.sort_index()
            self.q_balance_sheet = self.stock.quarterly_balance_sheet.T.sort_index()
            self.q_cashflow_stmt = self.stock.quarterly_cashflow.T.sort_index()
            self.info = self.stock.info

            # Getting yearly Data from yfinance
            self.y_income_stmt = self.stock.financials.T.sort_index()
            self.y_balance_sheet = self.stock.balance_sheet.T.sort_index()
            self.y_cashflow_stmt = self.stock.cashflow.T.sort_index()

            self.ypricehistory = self.stock.history(period="7y")
            self.qpricehistory = self.stock.history(period="2y")

            if self.info.get('longName') is None:
                 self.errors.append(f"Could not retrieve company information for ticker '{ticker}'. It may be an invalid ticker.")
                 return

        except Exception as e:
            self.errors.append(f"Failed to fetch financial data for {ticker}. Error: {e}")
            return
        
        # Calculating Some Basic Things
        self.q_dates = self.q_income_stmt.index.intersection(self.q_balance_sheet.index).intersection(self.q_cashflow_stmt.index)
        self.y_dates = self.y_income_stmt.index.intersection(self.y_balance_sheet.index).intersection(self.y_cashflow_stmt.index)
        self.qratios = pd.DataFrame(index=self.q_dates)
        self.qfinancials = pd.DataFrame(index=self.q_dates)
        self.qratios['Quarter'] = self.q_dates.to_series().apply(lambda x:((x.month - 1) // 3) + 1)
        self.qratios['Year'] = self.q_dates.to_series().apply(lambda x:x.year)
        self.qfinancials['Quarter'] = self.q_dates.to_series().apply(lambda x:((x.month - 1) // 3) + 1)
        self.qfinancials['Year'] = self.q_dates.to_series().apply(lambda x:x.year)
        self.yratios = pd.DataFrame(index=self.y_dates)
        self.yfinancials = pd.DataFrame(index=self.y_dates)
        self.yfinancials['Year'] = self.y_dates.to_series().apply(lambda x: x.year)
        self.yratios['Year'] = self.y_dates.to_series().apply(lambda x: x.year)
        
        self.latest_quarter = self.q_dates[-1]
        self.latest_year = self.y_dates[-1]
    
    def get_safe_value(self, df, key, date, default=np.nan):
        series = df.get(key)
        if series is None:
            self.errors.append(f"Warning: Data column '{key}' not found for {self.ticker}.")
            return default
        return series.get(date, default)

    def calculate_quarterly_ratios(self):
        if self.q_dates.empty:
            self.errors.append(f"No quarterly data available for {self.ticker} to calculate ratios.")
            return
        
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
                lt_debt = self.get_safe_value(self.q_balance_sheet, "Long Term Debt", date, default=0)
                st_debt = self.get_safe_value(self.q_balance_sheet, "Short Term Debt", date, default=0)
                total_debt = lt_debt + st_debt
                market_cap = self.info.get("marketCap")
                ev = market_cap + total_debt - cash if pd.notnull(market_cap) else np.nan

                op_cashflow = self.q_cashflow_stmt.loc[date, "Operating Cash Flow"]
                op_cashflow = self.get_safe_value(self.q_cashflow_stmt, "Operating Cash Flow", date, default=0)
                capex = self.get_safe_value(self.q_cashflow_stmt, "Capital Expenditure", date, default=0)
                free_cash_flow = op_cashflow - capex if pd.notnull(op_cashflow) else np.nan
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

                self.qfinancials.loc[date, "Operating Cash Flow"] = op_cashflow
                self.qfinancials.loc[date, "Capital Expenditure"] = capex
                self.qfinancials.loc[date, "Free Cash Flow"] = free_cash_flow
                self.qfinancials.loc[date, "Working Capital"] = working_capital

                # Calculating and storing Financials
                self.qratios.loc[date, "Net Profit Margin"] =( net_income / revenue) * 100 if revenue else np.nan
                self.qratios.loc[date, "Gross Margin"] = (gross_profit / revenue) * 100 if revenue else np.nan
                self.qratios.loc[date, "Operating Margin"] = (operating_income / revenue) * 100 if revenue else np.nan
                self.qratios.loc[date, "ROA"] = (net_income / total_assets) * 100 if total_assets else np.nan
                self.qratios.loc[date, "ROE"] = (net_income / equity) * 100 if equity else np.nan
                self.qratios.loc[date, "Current Ratio"] = current_assets / current_liabilities if current_liabilities else np.nan
                self.qratios.loc[date, "Quick Ratio"] = (current_assets - inventory) / current_liabilities if current_liabilities else np.nan
                self.qratios.loc[date, "Cash Ratio"] = cash / current_liabilities if current_liabilities else np.nan
                self.qratios.loc[date, "Debt-to-Equity"] = total_liabilities / equity if equity else np.nan
                self.qratios.loc[date, "Debt Ratio"] = total_liabilities / total_assets if total_assets else np.nan
                self.qratios.loc[date, "Cash Flow Margin"] = (op_cashflow / revenue) * 100 if revenue else np.nan
                self.qratios.loc[date, "Inventory Turnover"] = revenue / inventory if inventory else np.nan
                self.qratios.loc[date, "Asset Turnover"] = revenue / total_assets if total_assets else np.nan
                self.qratios.loc[date, "Receivables Turnover"] = revenue / receivables if receivables else np.nan
                self.qratios.loc[date, "CapEx Intensity"] = (capex / revenue) * 100 if revenue else np.nan
                self.qratios.loc[date, "ROCE"] = (operating_income / invested_capital) * 100 if invested_capital else np.nan
                self.qratios.loc[date, "FCF Conversion"] = (free_cash_flow / net_income) * 100 if net_income else np.nan
                self.qratios.loc[date, 'Financial Leverage'] = total_assets / equity if equity else np.nan

                # Altman-Z Score
                if all(pd.notnull([working_capital, total_assets, retained_earnings, ebit, market_cap, total_liabilities, revenue])):
                    A = working_capital / total_assets if total_assets else 0
                    B = retained_earnings / total_assets if total_assets else 0
                    C = ebit / total_assets if total_assets else 0
                    D = market_cap / total_liabilities if total_liabilities else 0
                    E = revenue / total_assets if total_assets else 0
                    z_score = 1.2 * A + 1.4 * B + 3.3 * C + 0.6 * D + 1.0 * E
                    self.qratios.loc[date, "Altman Z-Score"] = z_score
                else:
                    self.qratios.loc[date, "Altman Z-Score"] = np.nan

            except Exception as e:
                self.errors.append(f"Could not calculate quarterly ratios for {self.ticker} on {date}. Reason: {e}")

        if self.latest_quarter:
            trailing_pe = self.info.get("trailingPE")
            eps_growth = self.info.get("earningsGrowth")
            self.peg_ratio = trailing_pe / (eps_growth * 100) if trailing_pe and eps_growth and eps_growth > 0 else "N/A"

            current_price = self.info.get("currentPrice")
            book_value = self.info.get("bookValue")
            self.pb_ratio = current_price / book_value if current_price and book_value else "N/A"
            
            dividend_rate = self.info.get("dividendRate", np.nan)
            shares = self.info.get("sharesOutstanding", np.nan)
            self.ev_ebit = ev / ebit if ebit else np.nan
            self.dividend_payout_ratio = ((dividend_rate * shares) / net_income) * 100 if dividend_rate and shares and net_income else np.nan
            self.ev_fcf = ev / free_cash_flow if ev and free_cash_flow else np.nan
            self.fcf_yield = (free_cash_flow / market_cap) * 100 if free_cash_flow and market_cap else np.nan



        growth_cols = [ "Revenue", "Net Income", "Gross Profit", "Operating Income", "Operating Cash Flow", "Free Cash Flow", "EBIT" ]

        for col in growth_cols:
            if col in self.qfinancials.columns:
                self.qfinancials[f"{col} QoQ"] = self.qfinancials[col].pct_change(fill_method=None).round(4) * 100

        self.format_ratios(type='q')
        self.qfinancials.dropna(inplace = True)
        self.qratios.dropna(inplace = True)

    def calculate_yearly_ratios(self):
        if self.y_dates.empty:
            self.errors.append(f"No yearly data available for {self.ticker} to calculate ratios.")
            return
        
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
                self.yratios.loc[date, "Net Profit Margin"] = (net_income / revenue) * 100 if revenue else np.nan
                self.yratios.loc[date, "Gross Margin"] = (gross_profit / revenue) * 100 if revenue else np.nan
                self.yratios.loc[date, "Operating Margin"] = (operating_income / revenue) * 100 if revenue else np.nan
                self.yratios.loc[date, "ROA"] =( net_income / total_assets) * 100 if total_assets else np.nan
                self.yratios.loc[date, "ROE"] = (net_income / equity) * 100 if equity else np.nan
                self.yratios.loc[date, "Current Ratio"] = current_assets / current_liabilities if current_liabilities else np.nan
                self.yratios.loc[date, "Quick Ratio"] = (current_assets - inventory) / current_liabilities if current_liabilities else np.nan
                self.yratios.loc[date, "Cash Ratio"] = cash / current_liabilities if current_liabilities else np.nan
                self.yratios.loc[date, "Debt-to-Equity"] = total_liabilities / equity if equity else np.nan
                self.yratios.loc[date, "Debt Ratio"] = total_liabilities / total_assets if total_assets else np.nan
                self.yratios.loc[date, "Cash Flow Margin"] = (op_cash_flow / revenue) * 100 if revenue else np.nan
                self.yratios.loc[date, "Inventory Turnover"] = revenue / inventory if inventory else np.nan
                self.yratios.loc[date, "Asset Turnover"] = revenue / total_assets if total_assets else np.nan
                self.yratios.loc[date, "Receivables Turnover"] = revenue / receivables if receivables else np.nan
                self.yratios.loc[date, "CapEx Intensity"] = (capex / revenue) * 100 if revenue else np.nan
                self.yratios.loc[date, "ROCE"] = (operating_income / invested_capital) * 100 if invested_capital else np.nan
                self.yratios.loc[date, "FCF Conversion"] = (free_cash_flow / net_income) * 100 if net_income else np.nan
                self.yratios.loc[date, 'Financial Leverage'] = total_assets / equity if equity else np.nan

            except Exception as e:
                self.errors.append(f"Could not calculate yearly ratios for {self.ticker} on {date}. Reason: {e}")

       
        growth_cols = [ "Revenue", "Net Income", "Gross Profit", "Operating Income", "Operating Cash Flow", "Free Cash Flow", "EBIT" ]

        for col in growth_cols:
            if col in self.yfinancials.columns:
                self.yfinancials[f"{col} YoY"] = self.yfinancials[col].pct_change(fill_method=None).round(4) * 100

        self.format_ratios(type='y')
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
            df = self.qratios
        elif type == 'y':
            df = self.yratios
        else:
            return

        for col in percent_columns:
            if col in df.columns:
                df[col] = df[col].round(5)

        for col in ratio_columns:
            if col in df.columns:
                df[col] = df[col].round(4)