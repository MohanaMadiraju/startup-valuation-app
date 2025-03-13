import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Set Page Config
st.set_page_config(page_title="Startup Valuation Calculator", page_icon="🚀", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stApp {background-color: #F5F7FA;}
    .css-18e3th9 {padding-top: 2rem;}
    .big-font {font-size:25px !important; font-weight: bold;}
    .stButton>button {background-color: #007BFF; color: white; border-radius: 5px; font-size: 18px;}
    </style>
    """, unsafe_allow_html=True)

# Title and Logo
col1, col2 = st.columns([0.15, 0.85])
col1.image("https://cdn-icons-png.flaticon.com/512/2016/2016046.png", width=100)
col2.markdown("<p class='big-font'>Startup Valuation Calculator</p>", unsafe_allow_html=True)

st.write("## Enter your startup details below to calculate valuation")

# User Inputs
revenue = st.number_input("Revenue (Current Year)", value=1000000.0, format="%.2f")
growth_rate = st.number_input("Revenue Growth Rate (%)", value=10.0, format="%.2f")
operating_margin = st.number_input("Operating Margin (%)", value=15.0, format="%.2f")
depreciation = st.number_input("Depreciation & Amortization", value=10000.0, format="%.2f")
interest_expense = st.number_input("Interest Expense", value=5000.0, format="%.2f")
tax_rate = st.number_input("Tax Rate (%)", value=25.0, format="%.2f")
capex = st.number_input("Capital Expenditure (CapEx)", value=20000.0, format="%.2f")
working_capital = st.number_input("Working Capital Changes", value=5000.0, format="%.2f")
discount_rate = st.number_input("Discount Rate (%)", value=12.0, format="%.2f")
terminal_growth = st.number_input("Terminal Growth Rate (%)", value=3.0, format="%.2f")
investment = st.number_input("Investment Amount", value=500000.0, format="%.2f")
pre_money_shares = st.number_input("Pre-Money Shares Outstanding", value=1000000.0, format="%.2f")
esop_pool = st.number_input("ESOP Pool (% of Equity)", value=10.0, format="%.2f")

# Calculate Valuation
def calculate_valuation():
    pre_money_valuation = revenue * (1 + (growth_rate / 100)) / (discount_rate / 100 - terminal_growth / 100)
    post_money_valuation = pre_money_valuation + investment
    investor_stake = (investment / post_money_valuation) * 100
    founder_stake = 100 - investor_stake - esop_pool
    return pre_money_valuation, post_money_valuation, investor_stake, founder_stake

if st.button("Calculate Valuation"):
    pre_money, post_money, investor_stake, founder_stake = calculate_valuation()
    
    st.success("✅ Valuation Calculated Successfully!")
    st.write("### Valuation Results")
    
    st.info(f"**Pre-Money Valuation:** ₹{pre_money:,.2f}")
    st.info(f"**Post-Money Valuation:** ₹{post_money:,.2f}")
    st.write(f"**Investor Stake:** {investor_stake:.2f}%")
    st.write(f"**Founder Stake (after ESOP):** {founder_stake:.2f}%")
    st.write(f"**ESOP Pool:** {esop_pool:.2f}%")
    
    # Chart
    labels = ['Investor Stake', 'Founder Stake', 'ESOP Pool']
    sizes = [investor_stake, founder_stake, esop_pool]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#FF9999', '#66B3FF', '#99FF99'])
    ax.axis('equal')
    st.pyplot(fig)
    
    # PDF Report
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Startup Valuation Report", ln=True, align='C')
        pdf.cell(200, 10, f"Pre-Money Valuation: ₹{pre_money:,.2f}", ln=True)
        pdf.cell(200, 10, f"Post-Money Valuation: ₹{post_money:,.2f}", ln=True)
        pdf.cell(200, 10, f"Investor Stake: {investor_stake:.2f}%", ln=True)
        pdf.cell(200, 10, f"Founder Stake (after ESOP): {founder_stake:.2f}%", ln=True)
        pdf.cell(200, 10, f"ESOP Pool: {esop_pool:.2f}%", ln=True)
        pdf.output("valuation_report.pdf")
    
    if st.button("Download Valuation Report as PDF"):
        generate_pdf()
        st.success("📥 Report Generated! Download it from your browser.")


