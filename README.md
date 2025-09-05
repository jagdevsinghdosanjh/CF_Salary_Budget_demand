# 📊 CF Salary Budget Demand Generator

A Streamlit-based web app for ICT Coordinators to generate monthly salary budget demands for Computer Faculties (CFs), with increment logic based on joining date and detailed salary slip generation.

---

## 🚀 Features

- ✅ Upload CF salary data via Excel
- 📈 Auto-calculate incremented basic salary based on Date of Joining
- 🏫 Generate school-wise monthly budget demand
- 👨‍🏫 View CF-wise salary breakdown per school
- 🧾 Generate detailed salary slips for each CF
- 📤 Download CSV summaries for school budgets, CF breakdowns, and salary slips

---

## 📁 Project Structure

```plaintext
cf_salary_budget/
├── app.py                      # Streamlit entry point
├── cf_app.py                   # Alternate app layout with salary slips
├── data/                       # Excel uploads
├── modules/                   # Modular logic
│   ├── data_loader.py
│   ├── salary_calculator.py
│   ├── salary_slip_calculator.py
│   └── utils.py
├── assets/                     # CSS and static assets
├── templates/                  # Optional HTML templates
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git exclusions

📦 Installation
    # Create virtual environment
    python -m venv venv
    source venv/Scripts/activate  # On Windows

# Install dependencies
    pip install -r requirements.txt

# Run the app
    streamlit run cf_app.py

📊 Excel Format Requirements
Your uploaded .xlsx file must include the following columns:

Name of CF

Name of School

Bank Account No, (State Bank Of India only)

Date of Joining in the ICT

Basic Salary

DA @ 181 %

HRA @ 10%

RA @ 6%

CCA

Border Allowance

Handicap Allowance

Medical Allowance

Mobile Allowance

⚠️ Column names must match exactly for correct parsing.

🧠 Increment Logic
Each CF’s basic salary is incremented annually by a fixed rate (default: 3%) based on their joining date in ICT. This incremented basic is then combined with allowances to compute total salary.

🛠️ Future Enhancements
📄 PDF export of salary slips

📊 Charts for budget trends

🔐 Role-based login for ICT/Admin

🗂️ Historical budget tracking

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.

📜 License
This project is open-source and available under the MIT License.

🙌 Built by
Jagdev Singh Dosanjh Geometry educator & modular app designer Empowering educators through clarity, automation, and scalable tools.


---

Let me know if you'd like to include screenshots, badges, or a demo link. We can make this README shine like a product page.


