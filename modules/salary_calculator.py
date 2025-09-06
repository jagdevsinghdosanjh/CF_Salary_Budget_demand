from .utils import calculate_incremented_salary

def compute_school_budgets(df):
    df["Incremented Basic"] = df.apply(
        lambda row: calculate_incremented_salary(row["Date of Joining in the ICT"], row["Basic Salary"]), axis=1
    )
    df["Total Salary"] = df["Incremented Basic"] + df[["DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
                                                    "Border Allowance", "Handicap Allowance",
                                                    "Medical Allowance", "Mobile Allowance"]].sum(axis=1)
    school_budgets = df.groupby(["Name of School", "Bank Account No, (State Bank Of India only)"])["Total Salary"].sum().reset_index()
    #school_budgets.rename(columns={"Total Salary": "Monthly Budget Demand"}, inplace=True)
    return school_budgets
