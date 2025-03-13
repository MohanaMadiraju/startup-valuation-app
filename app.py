import streamlit as st

def calculate_valuation(revenue, growth_rate, operating_margin, depreciation, interest, tax_rate, capex, working_capital, discount_rate, terminal_growth, investment, pre_money_shares):
    projected_revenue = revenue * (1 + growth_rate)
    operating_profit = projected_revenue * operating_margin
    ebit = operating_profit - depreciation
    ebt = ebit - interest
    net_income = ebt * (1 - tax_rate)
    fcf = net_income + depreciation - capex - working_capital
    
    terminal_value = fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
    enterprise_value = terminal_value
    equity_value = enterprise_value
    pre_money_valuation = equity_value
    post_money_valuation = pre_money_valuation + investment
    dilution = investment / post_money_valuation
    investor_stake = dilution * 100
    founder_stake = 100 - investor_stake
    
    return pre_money_valuation, post_money_valuation, investor_stake, founder_stake

st.title("🚀 Startup Valuation Calculator")

# User inputs
revenue = st.number_input("Revenue (Current Year)", value=1000000.0, format="%.2f")
growth_rate = st.number_input("Revenue Growth Rate (%)", value=10.0, format="%.2f") / 100
operating_margin = st.number_input("Operating Margin (%)", value=15.0, format="%.2f") / 100
depreciation = st.number_input("Depreciation & Amortization", value=10000.0, format="%.2f")
interest = st.number_input("Interest Expense", value=5000.0, format="%.2f")
tax_rate = st.number_input("Tax Rate (%)", value=25.0, format="%.2f") / 100
capex = st.number_input("Capital Expenditure (CapEx)", value=20000.0, format="%.2f")
working_capital = st.number_input("Working Capital Changes", value=5000.0, format="%.2f")
discount_rate = st.number_input("Discount Rate (%)", value=12.0, format="%.2f") / 100
terminal_growth = st.number_input("Terminal Growth Rate (%)", value=3.0, format="%.2f") / 100
investment = st.number_input("Investment Amount", value=500000.0, format="%.2f")
pre_money_shares = st.number_input("Pre-Money Shares Outstanding", value=1000000.0, format="%.2f")

if st.button("Calculate Valuation"):
    pre_money, post_money, investor_stake, founder_stake = calculate_valuation(
        revenue, growth_rate, operating_margin, depreciation, interest, tax_rate,
        capex, working_capital, discount_rate, terminal_growth, investment, pre_money_shares
    )
    
    st.subheader("📊 Valuation Results")
    st.write(f"**Pre-Money Valuation:** ₹{pre_money:,.2f}")
    st.write(f"**Post-Money Valuation:** ₹{post_money:,.2f}")
    st.write(f"**Investor Stake:** {investor_stake:.2f}%")
    st.write(f"**Founder Stake:** {founder_stake:.2f}%")

st.caption("Created with ❤️ by a CA passionate about valuations!")
