import streamlit as st
import pandas as pd
from io import BytesIO

def calculate_valuation(revenue, growth_rate, margin, depreciation, interest, tax_rate, capex, working_capital,
                         discount_rate, terminal_growth, investment, pre_money_shares, esop_percent, new_shares):
    projected_revenue = revenue * (1 + growth_rate)
    operating_profit = projected_revenue * margin
    ebit = operating_profit - depreciation
    ebt = ebit - interest
    net_income = ebt * (1 - tax_rate)
    fcf = net_income + depreciation - capex - working_capital
    
    terminal_value = (fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    enterprise_value = fcf + terminal_value
    equity_value = enterprise_value  # Assuming no net debt
    pre_money_valuation = equity_value
    post_money_valuation = pre_money_valuation + investment
    
    total_shares_after_funding = pre_money_shares + new_shares
    investor_ownership_before_esop = investment / post_money_valuation
    founder_esop_dilution = new_shares / total_shares_after_funding
    investor_final_ownership = investor_ownership_before_esop / (1 - founder_esop_dilution)
    
    return {
        "Pre-Money Valuation (₹)": pre_money_valuation,
        "Post-Money Valuation (₹)": post_money_valuation,
        "Investor Ownership Before ESOPs (%)": round(investor_ownership_before_esop * 100, 2),
        "Founder & ESOP Dilution (%)": round(founder_esop_dilution * 100, 2),
        "Investor Final Ownership (Anti-Dilution Applied) (%)": round(investor_final_ownership * 100, 2)
    }

def generate_report(data):
    df = pd.DataFrame(data.items(), columns=["Metric", "Value"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Valuation Report", index=False)
    output.seek(0)
    return output

# Streamlit UI
st.set_page_config(page_title="Startup Valuation Calculator", layout="wide")
st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=80)
st.title("Startup Valuation Calculator")
st.markdown("### Enter your startup details below to calculate valuation")

# Layout for input fields
col1, col2 = st.columns(2)
with col1:
    revenue = st.number_input("Revenue (₹)", value=1000000.0, format="%f")
    growth_rate = st.number_input("Revenue Growth Rate (%)", value=10.0, format="%f") / 100
    margin = st.number_input("Operating Margin (%)", value=15.0, format="%f") / 100
    depreciation = st.number_input("Depreciation & Amortization (₹)", value=50000.0, format="%f")
    interest = st.number_input("Interest Expense (₹)", value=20000.0, format="%f")
    tax_rate = st.number_input("Tax Rate (%)", value=25.0, format="%f") / 100

with col2:
    capex = st.number_input("Capital Expenditure (CapEx) (₹)", value=30000.0, format="%f")
    working_capital = st.number_input("Working Capital Changes (₹)", value=20000.0, format="%f")
    discount_rate = st.number_input("Discount Rate (%)", value=12.0, format="%f") / 100
    terminal_growth = st.number_input("Terminal Growth Rate (%)", value=3.0, format="%f") / 100
    investment = st.number_input("Investment Amount (₹)", value=500000.0, format="%f")
    pre_money_shares = st.number_input("Pre-Money Shares Outstanding", value=1000000, format="%d")

esop_percent = st.number_input("ESOP Pool % (before investment)", value=10.0, format="%f") / 100
new_shares = st.number_input("New Shares Issued (ESOPs / Future Rounds)", value=100000, format="%d")

if st.button("💰 Calculate Valuation"):
    results = calculate_valuation(revenue, growth_rate, margin, depreciation, interest, tax_rate, capex, working_capital,
                                  discount_rate, terminal_growth, investment, pre_money_shares, esop_percent, new_shares)
    
    st.markdown("### 📊 Valuation Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Pre-Money Valuation (₹)", f"{results['Pre-Money Valuation (₹)']:,}")
    col2.metric("Post-Money Valuation (₹)", f"{results['Post-Money Valuation (₹)']:,}")
    col3.metric("Investor Final Ownership (%)", f"{results['Investor Final Ownership (Anti-Dilution Applied) (%)']}%")
    
    report = generate_report(results)
    st.download_button(label="📥 Download Valuation Report", data=report, file_name="Startup_Valuation_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("This tool ensures investors maintain their stake, factoring in ESOP dilution protection.")


