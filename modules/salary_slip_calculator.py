from .utils import calculate_incremented_salary

def generate_salary_slips(df):
    from .utils import calculate_incremented_salary

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

    ordered_cols = [
        "Name of CF", "Name of School", "Bank Account No, (State Bank Of India only)",
        "Date of Joining in the ICT", "Basic Salary", "Incremented Basic"
    ] + valid_allowances + ["Total Salary"]

    slips_df = df[ordered_cols].copy()

    # Rename for clarity
    slips_df.rename(columns={
        "Name of CF": "Faculty Name",
        "Name of School": "School",
        "Bank Account No, (State Bank Of India only)": "SBI Account No",
        "Date of Joining in the ICT": "Joining Date",
        "Basic Salary": "Basic",
        "Incremented Basic": "Incremented Basic",
        "Total Salary": "Total"
    }, inplace=True)

    return slips_df
