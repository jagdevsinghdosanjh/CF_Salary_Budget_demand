import pandas as pd
from .utils import calculate_incremented_salary
import pandas as pd
from .utils import calculate_incremented_salary

def compute_cf_wise_budgets(df):
    df["Incremented Basic"] = df.apply(
        lambda row: calculate_incremented_salary(row["Date of Joining in the ICT"], row["Basic Salary"]), axis=1
    )

    allowance_cols = [
        "DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
        "Border Allowance", "Handicap Allowance",
        "Medical Allowance", "Mobile Allowance"
    ]
    valid_allowances = [col for col in allowance_cols if col in df.columns]

    df["Total Salary"] = df["Incremented Basic"] + df[valid_allowances].sum(axis=1)

    cf_budgets = df[[
        "Name of School",
        "Bank Account No, (State Bank Of India only)",
        "Name of CF",
        "Total Salary"
    ]].copy()

    cf_budgets.rename(columns={"Total Salary": "Monthly Budget Demand"}, inplace=True)
    return cf_budgets


def compute_school_budgets(df):
    df["Incremented Basic"] = df.apply(
        lambda row: calculate_incremented_salary(row["Date of Joining in the ICT"], row["Basic Salary"]), axis=1
    )

    expected_allowances = [
        "DA @ 181 %", "HRA @ 10%", "RA @ 6%", "CCA",
        "Border Allowance", "Handicap Allowance",
        "Medical Allowance", "Mobile Allowance"
    ]

    # Filter only columns that exist
    valid_allowances = [col for col in expected_allowances if col in df.columns]

    df["Total Salary"] = df["Incremented Basic"] + df[valid_allowances].sum(axis=1)

    school_budgets = df.groupby(
        ["Name of School", "Bank Account No, (State Bank Of India only)"]
    )["Total Salary"].sum().reset_index()

    school_budgets.rename(columns={"Total Salary": "Monthly Budget Demand"}, inplace=True)
    return school_budgets


# def compute_school_budgets(df):
#     df["Incremented Basic"] = df.apply(
#         lambda row: calculate_incremented_salary(row["Date of Joining in the ICT"], row["Basic Salary"]), axis=1
#     )

#     allowance_cols = [
#         "DA@181%", "HRA@10%", "RA@6%", "CCA",
#         "Border Allowance", "Handicap Allowance",
#         "Medical Allowance", "Mobile Allowance"
#     ]

#     df["Total Salary"] = df["Incremented Basic"] + df[allowance_cols].sum(axis=1)

#     school_budgets = df.groupby(
#         ["Name of School", "Bank Account No, (State Bank Of India only)"]
#     )["Total Salary"].sum().reset_index()

#     school_budgets.rename(columns={"Total Salary": "Monthly Budget Demand"}, inplace=True)
#     return school_budgets
