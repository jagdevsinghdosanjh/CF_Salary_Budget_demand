import streamlit as st
import pandas as pd
from fpdf import FPDF
from modules.data_loader import load_cf_data as ld
from modules.salary_calculator import compute_school_budgets
from modules.utils import get_available_salary_components, compute_total_salary

# 🔁 Constants
COLUMN_SCHOOL_NAME = "Name of School"
COLUMN_CF_NAME = "Name of CF"

# 📄 PDF Generator
def generate_pdf(cf_data, available_components, computed_total):
    pdf = FPDF()
    pdf.add_page()

    # Register Unicode font
    pdf.add_font("DejaVu", "", "assets/fonts/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "assets/fonts/DejaVuSans-Bold.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Title
    pdf.set_font("DejaVu", 'B', 14)
    pdf.cell(200, 10, txt="Salary Slip", ln=True, align='C')
    pdf.ln(10)

    # Faculty Info
    pdf.set_font("DejaVu", size=12)
    pdf.cell(200, 10, txt=f"Computer Faculty: {cf_data[COLUMN_CF_NAME]}", ln=True)
    pdf.cell(200, 10, txt=f"School: {cf_data[COLUMN_SCHOOL_NAME]}", ln=True)
    pdf.cell(200, 10, txt=f"Date of Joining: {cf_data['Date of Joining in the ICT']}", ln=True)
    pdf.cell(200, 10, txt=f"Bank Account No: {cf_data['Bank Account No, (State Bank Of India only)']}", ln=True)
    pdf.ln(10)

    # Salary Components
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(100, 10, txt="Component", border=1)
    pdf.cell(100, 10, txt="Amount", border=1, ln=True)

    pdf.set_font("DejaVu", size=12)
    for comp in available_components:
        amount = cf_data.get(comp, 0)
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            amount = 0.0
        pdf.cell(100, 10, txt=comp, border=1)
        pdf.cell(100, 10, txt=f"₹{amount:,.2f}", border=1, ln=True)

    # Total Salary
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(100, 10, txt="Total Salary", border=1)
    pdf.cell(100, 10, txt=f"₹{computed_total:,.2f}", border=1, ln=True)

    return bytes(pdf.output(dest='S'))

# 📊 Streamlit App
st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
st.title("📊 Computer Faculty Salary Budget Demand Generator")

uploaded_file = st.file_uploader("Upload CF Salary Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Sidebar Filters
    st.sidebar.header("🏫 Monthly Budget Demand by Name of School")
    Schools = sorted(df[COLUMN_SCHOOL_NAME].dropna().unique())
    School = st.sidebar.selectbox("Select Name of School to View CFs", Schools)

    st.sidebar.header("👨‍🏫 CF-Wise Monthly Budget Breakdown")
    cf_names = sorted(df[df[COLUMN_SCHOOL_NAME] == School][COLUMN_CF_NAME].dropna().unique())
    selected_cf = st.sidebar.selectbox("Select CF to View Salary Slip", cf_names)

    # Salary Slip View
    st.subheader("📄 Complete Salary Slips for All CFs")
    cf_slip = df[(df[COLUMN_SCHOOL_NAME] == School) & (df[COLUMN_CF_NAME] == selected_cf)]

    if not cf_slip.empty:
        cf_data = cf_slip.iloc[0]

        st.markdown(f"""
        **Name of CF:** {cf_data[COLUMN_CF_NAME]}  
        **Name of School:** {cf_data[COLUMN_SCHOOL_NAME]}  
        **Date of Joining in the ICT:** {cf_data['Date of Joining in the ICT']}  
        **Bank Account No, (State Bank Of India only):** {cf_data['Bank Account No, (State Bank Of India only)']}
        """)

        expected_components = [
            "Basic", "Incremented Basic", "DA @ 181%", "HRA @ 10%", "RA @ 6%",
            "CCA", "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance"
        ]
        available_components = get_available_salary_components(cf_slip, expected_components)
        computed_total = compute_total_salary(cf_data, expected_components)

        if available_components:
            salary_table = cf_slip[available_components].T.rename(columns={cf_slip.index[0]: "Amount"})

            # Highlight missing mandatory fields
            mandatory_fields = ["Basic", "DA @ 181%"]
            missing_fields = [field for field in mandatory_fields if field not in available_components]
            for field in missing_fields:
                salary_table.loc[field] = "⚠️ Missing"

            salary_table.loc["Total Salary"] = f"₹{computed_total:,.2f}"
            st.table(salary_table)
        else:
            st.warning("No salary components found for this CF.")

        # PDF Download
        pdf_bytes = generate_pdf(cf_data, available_components, computed_total)
        st.download_button(
            label="📥 Download Salary Slip PDF",
            data=pdf_bytes,
            file_name=f"{cf_data[COLUMN_CF_NAME].replace(' ', '_')}_Salary_Slip.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("No data found for selected CF.")
else:
    st.info("Please upload a valid Excel file to begin.")
