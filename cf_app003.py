import streamlit as st
import pandas as pd
from fpdf import FPDF
from modules.data_loader import load_cf_data
from modules.salary_calculator import compute_school_budgets, compute_cf_wise_budgets
from modules.salary_slip_calculator import generate_salary_slips

# 💰 Format currency columns
def format_currency(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"₹{x:,.2f}" if pd.notnull(x) else "—")
    return df

# 📄 Generate PDF salary slip
def generate_pdf(slip_row):
    pdf = FPDF()
    pdf.add_page()

    # Load Unicode fonts
    pdf.add_font("DejaVu", "", "assets/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "assets/DejaVuSans-Bold.ttf", uni=True)

    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(200, 10, txt="Salary Slip", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("DejaVu", "", 11)
    pdf.cell(100, 10, txt=f"Faculty Name: {slip_row['Faculty Name']}", ln=True)
    pdf.cell(100, 10, txt=f"School: {slip_row['School']}", ln=True)
    pdf.cell(100, 10, txt=f"Joining Date: {slip_row['Joining Date']}", ln=True)
    pdf.cell(100, 10, txt=f"SBI Account No: {slip_row['SBI Account No']}", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(100, 10, txt="Component", border=1)
    pdf.cell(50, 10, txt="Amount", border=1, ln=True)

    pdf.set_font("DejaVu", "", 11)
    for col in ["Basic", "Incremented Basic", "DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
                "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance", "Total"]:
        value = slip_row.get(col, "—")
        pdf.cell(100, 10, txt=col, border=1)
        pdf.cell(50, 10, txt=str(value), border=1, ln=True)

    return pdf.output(dest='S').encode('latin-1')

# 🚀 Streamlit App
st.set_page_config(page_title="CF Salary Budget Demand", layout="wide")
st.title("📊 Computer Faculty Salary Budget Demand Generator")

uploaded_file = st.file_uploader("Upload CF Salary Excel File", type=["xlsx"])
if uploaded_file:
    df = load_cf_data(uploaded_file)

    # 🏫 School-wise Budget
    budget_df = compute_school_budgets(df)
    st.subheader("🏫 Monthly Budget Demand by School")
    st.dataframe(budget_df)

    # 👨‍🏫 CF-wise Breakdown
    cf_budget_df = compute_cf_wise_budgets(df)
    st.subheader("👨‍🏫 CF-Wise Monthly Budget Breakdown")

    schools = cf_budget_df["Name of School"].unique()
    selected_school = st.selectbox("Select School to View CFs", options=schools)
    filtered_cf_df = cf_budget_df[cf_budget_df["Name of School"] == selected_school]
    st.dataframe(filtered_cf_df)

    # 📄 Salary Slips
    slips_df = generate_salary_slips(df)
    st.subheader("📄 Complete Salary Slips for All CFs")

    selected_cf = st.selectbox("Select CF to View Salary Slip", options=slips_df["Faculty Name"].unique())
    cf_slip = slips_df[slips_df["Faculty Name"] == selected_cf].copy()
    cf_slip = format_currency(cf_slip, ["Basic", "Incremented Basic", "DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
                                        "Border Allowance", "Handicap Allowance", "Medical Allowance", "Mobile Allowance", "Total"])

    if not cf_slip.empty:
        st.markdown(f"""
        <div style="font-family:Segoe UI; padding:1.5rem; border:2px solid #2c3e50; background:#ffffff; max-width:800px; margin:auto;">
          <h2 style="text-align:center; color:#2c3e50;">Salary Slip</h2>
          <hr>
          <p><strong>Faculty Name:</strong> {cf_slip.iloc[0]['Faculty Name']}</p>
          <p><strong>School:</strong> {cf_slip.iloc[0]['School']}</p>
          <p><strong>Joining Date:</strong> {cf_slip.iloc[0]['Joining Date']}</p>
          <p><strong>SBI Account No:</strong> {cf_slip.iloc[0]['SBI Account No']}</p>
          <hr>
          <table style="width:100%; border-collapse:collapse;">
            <thead>
              <tr style="background:#f0f0f0;">
                <th style="text-align:left; padding:8px;">Component</th>
                <th style="text-align:right; padding:8px;">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr><td style="padding:8px;">Basic</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Basic']}</td></tr>
              <tr><td style="padding:8px;">Incremented Basic</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Incremented Basic']}</td></tr>
              <tr><td style="padding:8px;">DA @ 181%</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['DA @ 181 %']}</td></tr>
              <tr><td style="padding:8px;">HRA @ 10%</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['HRA @ 10%']}</td></tr>
              <tr><td style="padding:8px;">RA @ 6%</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['RA @ 6%']}</td></tr>
              <tr><td style="padding:8px;">CCA</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['CCA']}</td></tr>
              <tr><td style="padding:8px;">Border Allowance</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Border Allowance']}</td></tr>
              <tr><td style="padding:8px;">Handicap Allowance</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Handicap Allowance']}</td></tr>
              <tr><td style="padding:8px;">Medical Allowance</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Medical Allowance']}</td></tr>
              <tr><td style="padding:8px;">Mobile Allowance</td><td style="text-align:right; padding:8px;">{cf_slip.iloc[0]['Mobile Allowance']}</td></tr>
              <tr style="background:#e8f4ff;"><td style="padding:8px;"><strong>Total Salary</strong></td><td style="text-align:right; padding:8px;"><strong>{cf_slip.iloc[0]['Total']}</strong></td></tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        # 📤 PDF Export
        pdf_bytes = generate_pdf(cf_slip.iloc[0])
        st.download_button(
            label="📄 Download Salary Slip as PDF",
            data=pdf_bytes,
            file_name=f"{selected_cf}_salary_slip.pdf",
            mime="application/pdf"
        )

    # 📥 CSV Downloads
    st.download_button("📥 Download School-Wise Budget", budget_df.to_csv(index=False), "school_budget.csv")
    st.download_button("📥 Download CF-Wise Budget", cf_budget_df.to_csv(index=False), "cf_wise_budget.csv")
    st.download_button("📥 Download All Salary Slips", slips_df.to_csv(index=False), "all_salary_slips.csv")
    st.success("Data processed successfully!")
# --- IGNORE ---