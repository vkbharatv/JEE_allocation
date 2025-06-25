import pandas as pf
from data_func import *
data_raw = pd.read_excel("MasterData.xlsx")

cleaned_data = prepare_merit(data_raw)
# Initializing the waiting list
cleaned_data["CSE"] = 0
cleaned_data["CSE(D)"] = 0
cleaned_data["CCE"] = 0
cleaned_data["ECE"] = 0
cleaned_data["ECE(D)"] = 0
cleaned_data["ME"] = 0
cleaned_data["LICAI(AI)"] = 0
cleaned_data["LICAI(DS)"] = 0
# Target allocation Counts
allocation_targets = {
    "CSE": 500,
    "CSE(D)": 100,
    "CCE": 400,
    "ECE": 800,
    "ECE(D)": 100,
    "ME": 600,
    "LICAI(AI)": 30,
    "LICAI(DS)": 30,
}
allocation_save = allocation_targets.copy()
allocation_data = allocate_branches(cleaned_data, allocation_targets)
print("Total applicants =", len(allocation_data))
print(
    "Total allocation = ",
    len(allocation_data[allocation_data["ALLOCATED"].notna()]),
)
print(
    "Total Remaining = ",
    len(allocation_data[allocation_data["ALLOCATED"].isna()]),
    "\n",
)

save_data(allocation_data, data_raw, allocation_save)  # type: ignore