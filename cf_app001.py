import streamlit as st
from modules.data_loader import load_cf_data
from modules.salary_calculator import compute_school_budgets, compute_cf_wise_budgets
from modules.salary_slip_calculator import generate_salary_slips

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
    selected_cf = st.selectbox("Select CF to View Salary Slip", options=slips_df["Name of CF"].unique())
    cf_slip = slips_df[slips_df["Name of CF"] == selected_cf]
    st.dataframe(cf_slip)

    # Download options
    st.download_button("Download School-Wise Budget", budget_df.to_csv(index=False), "school_budget.csv")
    st.download_button("Download CF-Wise Budget", cf_budget_df.to_csv(index=False), "cf_wise_budget.csv")
    st.download_button("Download All Salary Slips", slips_df.to_csv(index=False), "cf_salary_slips.csv")
else:
    st.info("Please upload the salary details Excel file to proceed.")
