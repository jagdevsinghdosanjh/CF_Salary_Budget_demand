import streamlit as st
import pandas as pd
from fpdf import FPDF

# -------------------------------
# 📄 PDF Generator
# -------------------------------
def generate_pdf(cf_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Salary Slip", ln=True, align='C')
    pdf.ln(10)

    # Faculty Info
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Faculty Name: {cf_data['Faculty Name']}", ln=True)
    pdf.cell(200, 10, txt=f"School: {cf_data['School']}", ln=True)
    pdf.cell(200, 10, txt=f"Joining Date: {cf_data['Joining Date']}", ln=True)
    pdf.cell(200, 10, txt=f"SBI Account No: {cf_data['SBI Account No']}", ln=True)
    pdf.ln(10)

    # Salary Components
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="Component", border=1)
    pdf.cell(100, 10, txt="Amount", border=1, ln=True)

    pdf.set_font("Arial", size=12)
    components = [
        "Basic", "Incremented Basic", "DA @ 181%", "HRA @ 10%", "RA @ 6%",
        "CCA", "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance"
    ]
    for comp in components:
        amount = cf_data.get(comp, "₹0.00")
        pdf.cell(100, 10, txt=comp, border=1)
        pdf.cell(100, 10, txt=str(amount), border=1, ln=True)

    # Total
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="Total Salary", border=1)
    pdf.cell(100, 10, txt=str(cf_data.get("Total Salary", "₹0.00")), border=1, ln=True)

    return bytes(pdf.output(dest='S'))

# -------------------------------
# 📊 Streamlit App
# -------------------------------
st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
st.title("📊 Computer Faculty Salary Budget Demand Generator")

# File Upload
uploaded_file = st.file_uploader("Upload CF Salary Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Sidebar Filters
    st.sidebar.header("🏫 Monthly Budget Demand by School")
    schools = sorted(df["School"].unique())
    selected_school = st.sidebar.selectbox("Select School to View CFs", schools)

    st.sidebar.header("👨‍🏫 CF-Wise Monthly Budget Breakdown")
    cf_names = sorted(df[df["School"] == selected_school]["Faculty Name"].unique())
    selected_cf = st.sidebar.selectbox("Select CF to View Salary Slip", cf_names)

    # Salary Slip View
    st.subheader("📄 Complete Salary Slips for All CFs")
    cf_slip = df[(df["School"] == selected_school) & (df["Faculty Name"] == selected_cf)]

    if not cf_slip.empty:
        cf_data = cf_slip.iloc[0]
        st.markdown(f"""
        **Faculty Name:** {cf_data['Faculty Name']}  
        **School:** {cf_data['School']}  
        **Joining Date:** {cf_data['Joining Date']}  
        **SBI Account No:** {cf_data['SBI Account No']}
        """)

        st.table(cf_slip[[
            "Basic", "Incremented Basic", "DA @ 181%", "HRA @ 10%", "RA @ 6%",
            "CCA", "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance", "Total Salary"
        ]].T.rename(columns={cf_slip.index[0]: "Amount"}))

        # PDF Download
        pdf_bytes = generate_pdf(cf_data)
        st.download_button(
            label="📥 Download Salary Slip PDF",
            data=pdf_bytes,
            file_name=f"{cf_data['Faculty Name'].replace(' ', '_')}_Salary_Slip.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("No data found for selected CF.")

else:
    st.info("Please upload a valid Excel file to begin.")
    