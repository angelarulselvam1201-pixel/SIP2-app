import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced SIP Calculator", page_icon="📊", layout="centered")

st.title("📊 Advanced SIP Calculator (With Inflation & Charts)")

# Inputs
monthly_invest = st.number_input("Monthly SIP Amount (₹)", min_value=100, value=5000, step=100)
annual_rate = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)
years = st.number_input("Investment Duration (Years)", min_value=1, value=10)
inflation_rate = st.number_input("Expected Inflation Rate (%)", min_value=0.0, value=6.0)

# SIP future value formula
def sip_future_value(P, r, n):
    monthly_r = r / 12
    months = n * 12
    fv = P * (((1 + monthly_r) ** months - 1) / monthly_r) * (1 + monthly_r)
    return fv

# Inflation adjustment
def inflation_adjust(amount, inflation, years):
    real_rate = (1 + inflation) ** years
    return amount / real_rate

# Generate monthly breakdown
def sip_breakdown(P, annual_r, years):
    monthly_r = annual_r / 12
    months = years * 12
    data = []
    total = 0

    for m in range(1, months + 1):
        total = (total + P) * (1 + monthly_r)
        data.append([m, m // 12, m % 12, P * m, total])
    
    return pd.DataFrame(data, columns=["Month", "Years Completed", "Extra Months", "Total Invested", "Future Value"])

# Calculate button
if st.button("Calculate"):

    # Main calculations
    fv = sip_future_value(monthly_invest, annual_rate / 100, years)
    total_invested = monthly_invest * years * 12
    inflation_adj_returns = inflation_adjust(fv, inflation_rate / 100, years)

    growth = fv - total_invested
    real_growth = inflation_adj_returns - total_invested

    st.subheader("📘 Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invested", f"₹{total_invested:,.2f}")
    col2.metric("Future Value", f"₹{fv:,.2f}")
    col3.metric("Inflation Adjusted Value", f"₹{inflation_adj_returns:,.2f}")

    st.subheader("📈 Profit")
    col4, col5 = st.columns(2)
    col4.metric("Profit (Before Inflation)", f"₹{growth:,.2f}")
    col5.metric("Profit (After Inflation)", f"₹{real_growth:,.2f}")

    # Monthly breakdown table
    st.subheader("📅 Monthly Breakdown Table")
    df = sip_breakdown(monthly_invest, annual_rate / 100, years)
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Breakdown (CSV)", csv, "sip_breakdown.csv", "text/csv")

    # Chart 1: Future Value vs Total Invested
    st.subheader("📊 Investment Growth Chart")
    plt.figure(figsize=(10, 5))
    plt.plot(df["Month"], df["Total Invested"], label="Total Invested")
    plt.plot(df["Month"], df["Future Value"], label="Future Value")
    plt.xlabel("Months")
    plt.ylabel("Amount (₹)")
    plt.legend()
    st.pyplot(plt)

    # Chart 2: Inflation-adjusted returns
    st.subheader("📉 Inflation-Adjusted Value Over Time")
    df["Inflation Adjusted"] = df["Future Value"] / ((1 + inflation_rate/100) ** (df["Month"] / 12))

    plt.figure(figsize=(10, 5))
    plt.plot(df["Month"], df["Future Value"], label="Future Value")
    plt.plot(df["Month"], df["Inflation Adjusted"], label="Inflation Adjusted", linestyle="--")
    plt.xlabel("Months")
    plt.ylabel("Amount (₹)")
    plt.legend()
    st.pyplot(plt)

    st.markdown("---")
    st.caption("Advanced SIP calculator with inflation & graphical analysis.")
