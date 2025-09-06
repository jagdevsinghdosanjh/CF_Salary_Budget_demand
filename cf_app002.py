import streamlit as st
import pandas as pd
from modules.data_loader import load_cf_data
from modules.salary_calculator import compute_school_budgets, compute_cf_wise_budgets
from modules.salary_slip_calculator import generate_salary_slips

# Utility for currency formatting
def format_currency(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"₹{x:,.2f}" if pd.notnull(x) else "")
    return df

st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
st.title("📊 Computer Faculty Salary Budget Demand Generator")

uploaded_file = st.file_uploader("Upload CF Salary Excel File", type=["xlsx"])
if uploaded_file:
    df = load_cf_data(uploaded_file)

    # School-wise summary
    budget_df = compute_school_budgets(df)
    st.subheader("🏫 Monthly Budget Demand by School")
    st.dataframe(budget_df)

    # CF-wise breakdown
    cf_budget_df = compute_cf_wise_budgets(df)
    st.subheader("👨‍🏫 CF-Wise Monthly Budget Breakdown")

    schools = cf_budget_df["Name of School"].unique()
    selected_school = st.selectbox("Select School to View CFs", options=schools)
    filtered_cf_df = cf_budget_df[cf_budget_df["Name of School"] == selected_school]
    st.dataframe(filtered_cf_df)

    # Salary Slips
    slips_df = generate_salary_slips(df)
    st.subheader("📄 Complete Salary Slips for All CFs")

    selected_cf = st.selectbox("Select CF to View Salary Slip", options=slips_df["Faculty Name"].unique())
    cf_slip = slips_df[slips_df["Faculty Name"] == selected_cf].copy()

    currency_cols = ["Basic", "Incremented Basic", "DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
                    "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance", "Total"]
    cf_slip = format_currency(cf_slip, currency_cols)

    # Display formatted HTML layout
    st.markdown(f"""
    <div style="font-family:Segoe UI; padding:1rem; border:1px solid #ccc; background:#f9f9f9">
    <h3 style="color:#2c3e50;">Salary Slip for {selected_cf}</h3>
    <p><strong>School:</strong> {cf_slip.iloc[0]['School']}</p>
    <p><strong>Joining Date:</strong> {cf_slip.iloc[0]['Joining Date']}</p>
    <p><strong>SBI Account No:</strong> {cf_slip.iloc[0]['SBI Account No']}</p>
    <hr>
    <table style="width:100%; border-collapse:collapse;">
        <tr><th style="text-align:left;">Component</th><th style="text-align:right;">Amount</th></tr>
        <tr><td>Basic</td><td>{cf_slip.iloc[0]['Basic']}</td></tr>
        <tr><td>Incremented Basic</td><td>{cf_slip.iloc[0]['Incremented Basic']}</td></tr>
        <tr><td>DA @ 181%</td><td>{cf_slip.iloc[0]['DA @ 181 %']}</td></tr>
        <tr><td>HRA @ 10%</td><td>{cf_slip.iloc[0]['HRA @ 10%']}</td></tr>
        <tr><td>RA @ 6%</td><td>{cf_slip.iloc[0]['RA @ 6%']}</td></tr>
        <tr><td>CCA</td><td>{cf_slip.iloc[0]['CCA']}</td></tr>
        <tr><td>Border Allowance</td><td>{cf_slip.iloc[0]['Border Allowance']}</td></tr>
        <tr><td>Handicap Allowance</td><td>{cf_slip.iloc[0]['Handicap Allowance']}</td></tr>
        <tr><td>Medical Allowance</td><td>{cf_slip.iloc[0]['Medical Allowance']}</td></tr>
        <tr><td>Mobile Allowance</td><td>{cf_slip.iloc[0]['Mobile Allowance']}</td></tr>
        <tr><td><strong>Total Salary</strong></td><td><strong>{cf_slip.iloc[0]['Total']}</strong></td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # Download options
    st.download_button("📥 Download School-Wise Budget", budget_df.to_csv(index=False), "school_budget.csv")
    st.download_button("📥 Download CF-Wise Budget", cf_budget_df.to_csv(index=False), "cf_wise_budget.csv")
    st.download_button("📥 Download All Salary Slips", slips_df.to_csv(index=False), "cf_salary_slips.csv")
else:
    st.info("Please upload the salary details Excel file to proceed.")
