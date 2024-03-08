import pandas as pd

# Load data
state_total = pd.read_csv("csv/stateCase.csv")
nation_cum = pd.read_csv("csv/7dayAvg.csv")
state_vac = pd.read_csv("csv/vaccines.csv")
gender_tests = pd.read_csv("csv/labTests.csv")
gender_confirm = pd.read_csv("csv/genders.csv")
race_percent = pd.read_csv("csv/ethincity.csv")
symptoms = pd.read_csv("csv/symptoms.csv")

# Drop US territories; only want Continental US
if 53 in state_total.index:
    state_total.drop([53], inplace=True)

# Reformat calendar dates to ISO 8601
print(nation_cum.columns)
nation_cum["epi_date_V3"] = pd.to_datetime(nation_cum["epi_date_V3"]).dt.date
race_percent["MMWR Week"] = pd.to_datetime(race_percent["MMWR Week"], format='%d-%b-%y').dt.date
gender_tests["Week"] = pd.to_datetime(gender_tests["Week"]).dt.date



# Reindex
gender_tests.set_index("Week", inplace=True)

# Create new sum columns
gender_tests["Total_Tests"] = gender_tests["Total Male Tests"] + gender_tests["Total Female Tests"]

# Add NYC to NY's total vaccine count
state_vac.set_index("Reporting Jurisdictions", inplace=True)
nyc_total = state_vac.loc["New York City", "Total"]
state_vac.at["New York", "Total"] += nyc_total
state_vac.drop(index="New York City", inplace=True)
state_vac.reset_index(inplace=True)
