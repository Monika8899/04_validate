import pandas as pd

data_path = r'C:\Users\KAMINENI MONIKA\Desktop\Hwy26Crashes2019_S23.csv'
crashes = pd.read_csv(data_path)
print(crashes)


def verify_assertion(description, condition):
    try:
        assert condition, description
        print(f"Passed: {description}")
    except AssertionError as error:
        print(f"Failed: {error}")

def analyze_data(df):
    # Every crash Occurred on a Date
    all_dates_exist = (df['Crash Day']).notna().all()
    verify_assertion("Every crash occurred on a date", all_dates_exist)

    # Limit Assertion: Every crash occurred during year 2019
    verify_assertion("Every crash occurred during year 2019", ((df['Crash Year'] == 2019)).all())


    # Intra-record Assertion: If a crash record has a latitude coordinate then it should also have a longitude coordinate
    condition = (df['Latitude Degrees'].notnull() & df['Longitude Degrees'].notnull()) | (
                df['Latitude Degrees'].isnull() & df['Longitude Degrees'].isnull())
    verify_assertion("If a crash record has a latitude coordinate then,it should also have a longitude coordinate",
                     condition.all())

    # Inter-record Check Assertions
    vehicle_ids_valid = df['Vehicle ID'].isin(df['Crash ID']).all()
    verify_assertion("Every vehicle listed was part of a known crash", vehicle_ids_valid)

    # Summary Assertions
    crash_total = len(df)
    verify_assertion("Thousands of crashes happened but not millions", 1000 <= crash_total <= 999999)


    # distributed throughout the months of the year.”
    monthly_counts = df.groupby(['Crash Year', 'Crash Month']).size().unstack().fillna(0)
    monthly_distribution = monthly_counts.div(monthly_counts.sum(axis=1), axis=0)  # Normalize by year
    condition1 = monthly_distribution.std().mean() < 0.1  # Check if the mean standard deviation across years is low
    verify_assertion("Crashes are evenly distributed throughout the months of the year", condition1)

    # alcohol_involved_crash_check
    alcohol_involved_count = df[df['Alcohol-Involved Flag'] == 'Yes'].shape[0]
    total_crashes = len(df)
    assertion_description = "Number of crashes involving alcohol should not exceed the total number of crashes"
    alcohol_involved_check = alcohol_involved_count <= total_crashes
    verify_assertion(assertion_description, alcohol_involved_check)

    # Filter the crashses crossed more than 15 for Highway Number 26 and the year 2019
    highway_26_data = df[(df['Highway Number'] == 26) & (df['Crash Year'] == 2019)]
    total_accidents = len(highway_26_data)

    # Check if the total accidents on Highway Number 26 in 2019 is more than 15
    assertion_description = "Total accidents on Highway Number 26 in 2019 should be more than 15"
    total_accidents_check = total_accidents > 15
    verify_assertion(assertion_description, total_accidents_check)

    # atleast 10 crashes happened due to Road surface of type 99
    road_surface_condition_count = (df['Road Surface Condition'] == 99).sum()
    assertion_description = "At least 10 vehicles met Crash with Road surface type 99"
    road_surface_condition_check = road_surface_condition_count >= 10
    verify_assertion(assertion_description, road_surface_condition_check)

    # Filter the dataset for weekends (Saturday and Sunday) and 'Alcohol-Involved Flag'
    weekend_alcohol_accidents = df[(df['Week Day Code'].isin([6, 7])) & (df['Alcohol-Involved Flag'] == 'Yes')]

    # Verify if at least one accident occurred on weekends with alcohol involvement
    assertion_description = "At least one accident occurred on weekends with 'Alcohol-Involved Flag'"
    at_least_one_accident = not weekend_alcohol_accidents.empty
    verify_assertion(assertion_description, at_least_one_accident)

    # Filter the dataset for crashes without School Zone or Work Zone indicators (flags 0 or 1)
    without_indicators = df[(df['School Zone Indicator'].isin([0, 1])) & (df['Work Zone Indicator'].isin([0, 1]))]

    # Calculate the count of crashes without indicators
    without_indicators_count = len(without_indicators)

    # Calculate 1% of the total crashes
    total_crashes = len(df)
    one_percent_total_crashes = 0.1 * total_crashes
    # Verify if at least 1% of total crashes occurred without indicators
    assertion_description = "At least 10% of total crashes occurred without School Zone or Work Zone indicators"
    at_least_one_percent = without_indicators_count >= one_percent_total_crashes
    verify_assertion(assertion_description, at_least_one_percent)



analyze_data(crashes)
