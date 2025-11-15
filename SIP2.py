import streamlit as st
import pandas as pd
import altair as alt
import math

st.set_page_config(page_title="Advanced SIP Calculator", page_icon="💹", layout="centered")

st.title("💹 Advanced SIP Calculator (No Matplotlib)")

st.write("""
This calculator includes:
- SIP future value (FV)
- Inflation-adjusted returns
- SIP vs Lumpsum comparison
- Month-by-month SIP table
- Interactive charts (Altair)
- CSV download
""")

# ----------------------------- INPUTS -----------------------------------
st.header("Enter Your Investment Details")

col1, col2 = st.columns(2)
with col1:
    monthly_sip = st.number_input("Monthly SIP Amount (₹)", min_value=100, value=5000, step=100)
    years = st.number_input("Investment Duration (Years)", min_value=1, value=10)

with col2:
    annual_return = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)
    inflation_rate = st.number_input("Inflation Rate (%)", min_value=0.0, value=6.0)

# ----------------------------- FUNCTIONS --------------------------------
def sip_future_value(P, r, yrs):
    monthly_rate = r / 12
    months = yrs * 12
    fv = P * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    return fv

def inflation_adjust(amount, inflation, yrs):
    return amount / ((1 + inflation)**yrs)

def sip_schedule(P, r, yrs):
    monthly_rate = r / 12
    months = yrs * 12
    data = []
    balance = 0
    invested = 0

    for month in range(1, months + 1):
        invested += P
        balance = (balance + P) * (1 + monthly_rate)
        data.append([month, invested, balance])

    df = pd.DataFrame(data, columns=["Month", "Total Invested", "Future Value"])
    return df

# ----------------------------- CALCULATE --------------------------------
if st.button("Calculate"):

    total_invested = monthly_sip * years * 12
    fv = sip_future_value(monthly_sip, annual_return/100, years)
    fv_infl_adj = inflation_adjust(fv, inflation_rate/100, years)

    df = sip_schedule(monthly_sip, annual_return/100, years)

    lumpsum = total_invested * (1 + annual_return/100)**years

    # --------------------------- RESULTS -------------------------------
    st.header("📘 Results Summary")

    st.write(f"**Total Invested:** ₹{total_invested:,.2f}")
    st.write(f"**Future Value (Without Inflation):** ₹{fv:,.2f}")
    st.write(f"**Future Value (Inflation Adjusted):** ₹{fv_infl_adj:,.2f}")

    st.write(f"**Lumpsum Value (If invested upfront):** ₹{lumpsum:,.2f}")

    st.markdown("---")

    # --------------------------- CHART 1 --------------------------------
    st.subheader("📈 SIP Growth Over Time (Interactive Chart)")

    chart1 = alt.Chart(df).mark_line().encode(
        x="Month",
        y="Future Value",
        tooltip=["Month", "Future Value"]
    ).interactive()

    st.altair_chart(chart1, use_container_width=True)

    # --------------------------- CHART 2 --------------------------------
    st.subheader("📉 Inflation Impact")

    df_inf = pd.DataFrame({
        "Category": ["Future Value", "Inflation Adjusted Value"],
        "Amount": [fv, fv_infl_adj]
    })

    chart2 = alt.Chart(df_inf).mark_bar().encode(
        x="Category",
        y="Amount",
        color="Category",
        tooltip=["Category", "Amount"]
    )

    st.altair_chart(chart2, use_container_width=True)

    # --------------------------- TABLE --------------------------------
    st.subheader("📄 Month-by-Month SIP Table")

    st.dataframe(df)

    # --------------------------- DOWNLOAD CSV --------------------------
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download SIP Schedule as CSV", csv, "sip_schedule.csv", "text/csv")

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit + Altair (No Matplotlib)")

