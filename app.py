import streamlit as st
from modules.data_loader import load_cf_data
from modules.salary_calculator import compute_school_budgets

st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
st.title("📊 Computer Faculty Salary Budget Demand Generator")

uploaded_file = st.file_uploader("Upload CF Salary Excel File", type=["xlsx"])
if uploaded_file:
    df = load_cf_data(uploaded_file)
    budget_df = compute_school_budgets(df)

    st.subheader("📌 Monthly Budget Demand by School")
    st.dataframe(budget_df)

    st.download_button("Download Budget Summary", budget_df.to_csv(index=False), "cf_budget_summary.csv")
else:
    st.info("Please upload the salary details Excel file to proceed.")


# # Streamlit entry point
# import streamlit as st
# from modules.data_loader import load_cf_data
# from modules.salary_calculator import compute_school_budgets

# st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
# st.title("📊 Computer Faculty Salary Budget Demand Generator")

# df = load_cf_data("data/cf_salary_details.xlsx")
# budget_df = compute_school_budgets(df)

# st.dataframe(budget_df)

# if st.button("Download Budget Summary"):
#     st.download_button("Download CSV", budget_df.to_csv(index=False), "cf_budget_summary.csv")
