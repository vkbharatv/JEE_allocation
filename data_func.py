import pandas as pd


def prepare_merit(data_r: pd.DataFrame):
    """Data Cleaning and Merit List Preparation"""

    clean_data = data_r[
        (data_r["HSC_PER"] >= 60)
        & (data_r["SSC_PER"] >= 60)
        & (data_r["HSC_PCM_PER"] >= 60)
        & (data_r["JEEE_SCORE"] >= 85)
    ]

    clean_data = clean_data.sort_values(
        by=[
            "JEEE_SCORE",
            "JEE_MATH",
            "JEE_PHYSICS",
            "JEE_CHEMISTRY",
            "HSC_PER",
            "HSC_PCM_PER",
            # "HSC_MAT",
            # "HSC_PHY",
            # "HSC_CHE",
            # "SSC_PER",
        ],
        ascending=False,
    )
    return clean_data.reset_index(drop=True).assign(ALLOCATED=None)


def save_data(data: pd.DataFrame, data_r: pd.DataFrame, allocations: pd.DataFrame):
    """Save Merit List"""

    opening_percentile = {
        "CSE": data[data["ALLOCATED"] == "CSE"]["JEEE_SCORE"].max(),
        "CSE(D)": data[data["ALLOCATED"] == "CSE(D)"]["JEEE_SCORE"].max(),
        "CCE": data[data["ALLOCATED"] == "CCE"]["JEEE_SCORE"].max(),
        "ECE": data[data["ALLOCATED"] == "ECE"]["JEEE_SCORE"].max(),
        "ECE(D)": data[data["ALLOCATED"] == "ECE(D)"]["JEEE_SCORE"].max(),
        "ME": data[data["ALLOCATED"] == "ME"]["JEEE_SCORE"].max(),
        "LICAI(AI)": data[data["ALLOCATED"] == "LICAI(AI)"]["JEEE_SCORE"].max(),
        "LICAI(DS)": data[data["ALLOCATED"] == "LICAI(DS)"]["JEEE_SCORE"].max(),
    }

    closing_percentile = {
        "CSE": data[data["ALLOCATED"] == "CSE"]["JEEE_SCORE"].min(),
        "CSE(D)": data[data["ALLOCATED"] == "CSE(D)"]["JEEE_SCORE"].min(),
        "CCE": data[data["ALLOCATED"] == "CCE"]["JEEE_SCORE"].min(),
        "ECE": data[data["ALLOCATED"] == "ECE"]["JEEE_SCORE"].min(),
        "ECE(D)": data[data["ALLOCATED"] == "ECE(D)"]["JEEE_SCORE"].min(),
        "ME": data[data["ALLOCATED"] == "ME"]["JEEE_SCORE"].min(),
        "LICAI(AI)": data[data["ALLOCATED"] == "LICAI(AI)"]["JEEE_SCORE"].min(),
        "LICAI(DS)": data[data["ALLOCATED"] == "LICAI(DS)"]["JEEE_SCORE"].min(),
    }

    branch_seats = {
        "CSE": data[data["ALLOCATED"] == "CSE"]["JEEE_SCORE"].count(),
        "CSE(D)": data[data["ALLOCATED"] == "CSE(D)"]["JEEE_SCORE"].count(),
        "CCE": data[data["ALLOCATED"] == "CCE"]["JEEE_SCORE"].count(),
        "ECE": data[data["ALLOCATED"] == "ECE"]["JEEE_SCORE"].count(),
        "ECE(D)": data[data["ALLOCATED"] == "ECE(D)"]["JEEE_SCORE"].count(),
        "ME": data[data["ALLOCATED"] == "ME"]["JEEE_SCORE"].count(),
        "LICAI(AI)": data[data["ALLOCATED"] == "LICAI(AI)"]["JEEE_SCORE"].count(),
        "LICAI(DS)": data[data["ALLOCATED"] == "LICAI(DS)"]["JEEE_SCORE"].count(),
    }

    analysis_data = pd.DataFrame(
        {
            "BRANCH": [
                "CSE",
                "CSE(D)",
                "CCE",
                "ECE",
                "ECE(D)",
                "ME",
                "LICAI(AI)",
                "LICAI(DS)",
            ],
            "OPENING_PERCENTILE": [
                opening_percentile["CSE"],
                opening_percentile["CSE(D)"],
                opening_percentile["CCE"],
                opening_percentile["ECE"],
                opening_percentile["ECE(D)"],
                opening_percentile["ME"],
                opening_percentile["LICAI(AI)"],
                opening_percentile["LICAI(DS)"],
            ],
            "CLOSING_PERCENTILE": [
                closing_percentile["CSE"],
                closing_percentile["CSE(D)"],
                closing_percentile["CCE"],
                closing_percentile["ECE"],
                closing_percentile["ECE(D)"],
                closing_percentile["ME"],
                closing_percentile["LICAI(AI)"],
                closing_percentile["LICAI(DS)"],
            ],
            "Seat Before": [
                allocations["CSE"],
                allocations["CSE(D)"],
                allocations["CCE"],
                allocations["ECE"],
                allocations["ECE(D)"],
                allocations["ME"],
                allocations["LICAI(AI)"],
                allocations["LICAI(DS)"],
            ],
            "Seats": [
                branch_seats["CSE"],
                branch_seats["CSE(D)"],
                branch_seats["CCE"],
                branch_seats["ECE"],
                branch_seats["ECE(D)"],
                branch_seats["ME"],
                branch_seats["LICAI(AI)"],
                branch_seats["LICAI(DS)"],
            ],
        }
    )
    analysis_data.loc["Total/Median", "Seats"] = analysis_data["Seats"].sum()
    analysis_data.loc["Total/Median", "Seat Before"] = analysis_data[
        "Seat Before"
    ].sum()

    analysis_data.loc["Total/Median", "CLOSING_PERCENTILE"] = data[
        data["ALLOCATED"].notna()
    ]["JEEE_SCORE"].median()

    print(analysis_data)

    with pd.ExcelWriter("Final.xlsx") as writer:
        data.to_excel(writer, sheet_name="Compleate Allocation", index=False)
        data_r.to_excel(writer, sheet_name="OLD DATA", index=False)
        analysis_data.to_excel(writer, sheet_name="ANALYSIS", index=False)
        data.dropna(subset=["ALLOCATED"]).to_excel(
            writer, sheet_name="MERIT_Waitlist", index=False
        )
        data[data["ALLOCATED"].isna()].to_excel(
            writer, sheet_name="Pure_Waitlist", index=False
        )
        data[
            (data["CSE"] == 0)
            & (data["CCE"] == 0)
            & (data["ECE"] == 0)
            & (data["ME"] == 0)
            & (data["ECE(D)"] == 0)
            & (data["CSE(D)"] == 0)
            & (data["LICAI(AI)"] == 0)
            & (data["LICAI(DS)"] == 0)
        ].to_excel(writer, sheet_name="MERIT_confirmnd", index=False)

    return print("\nData Saved with Fina name 'Final.xlsx'\n")


def allocate_branches(clean_data: pd.DataFrame, allocation_t: dict):
    """Branch Rules"""
    max_row = len(clean_data)
    pref = {}
    waitlist = {
        "CSE": 0,
        "CSE(D)": 0,
        "CCE": 0,
        "ECE": 0,
        "ECE(D)": 0,
        "ME": 0,
        "LICAI(AI)": 0,
        "LICAI(DS)": 0,
    }
    for row in range(0, max_row):
        pref.clear()
        pref = {
            "PREF1": clean_data.iloc[row]["PREF1"],
            "PREF2": clean_data.iloc[row]["PREF2"],
            "PREF3": clean_data.iloc[row]["PREF3"],
            "PREF4": clean_data.iloc[row]["PREF4"],
            "PREF5": clean_data.iloc[row]["PREF5"],
            "PREF6": clean_data.iloc[row]["PREF6"],
            "PREF7": clean_data.iloc[row]["PREF7"],
            "PREF8": clean_data.iloc[row]["PREF8"],
        }

        try:
            for _, value in pref.items():
                if (allocation_t[value]) > 0:
                    allocation_t[value] -= 1
                    clean_data.loc[row, "ALLOCATED"] = value
                    break

                waitlist[value] += 1
                # print(waitlist[value])
                clean_data.loc[row, value] = waitlist[value]

        except KeyError:
            pass

    allocations = clean_data

    return allocations
