import pandas as pd
import json

def get_monthly_covid_cases():
    df = pd.read_json("cso\covid_formatted.json")

    cities = ["Dublin City","Cork County","Galway County","Limerick City and County"]

    # Flatten the nested structure into a DataFrame
    flattened_data = df['Covid cases per 100,000 population'].apply(pd.Series)

    # Filter for the specified cities
    filtered_data = flattened_data[cities]

    # Convert the index to a DateTime index for resampling
    filtered_data.index = pd.to_datetime(filtered_data.index)

    # Selecting only the data for the year 2021
    filtered_data_2021 = filtered_data.loc['2021']

    # Dropping rows where all specified city data is None
    filtered_data_2021 = filtered_data_2021.dropna(how='all')

    # Resampling the data by month and calculating the mean for each city
    df_monthly_2021 = filtered_data_2021.resample('M').sum()  # You can change 'mean' to 'sum' or 'max' as needed

    # Formatting the index to show only year and month
    df_monthly_2021.index = df_monthly_2021.index.strftime('%Y-%m')

    return df_monthly_2021

def get_monthly_death_rates():
# Load the JSON file into a DataFrame
    df_deaths = pd.read_json('cso\death_formatted.json')
    counties = ["Co. Dublin", "Co. Cork", "Co. Galway", "Co. Limerick"]

    # Flatten the nested structure of the 'Total Deaths' column
    flattened_deaths = df_deaths['Total Deaths'].apply(pd.Series)

    # Filter for the specified counties
    filtered_deaths = flattened_deaths[counties]

    # Convert the index to a DateTime index for resampling
    filtered_deaths.index = pd.to_datetime(filtered_deaths.index)

    # Selecting only the data for the year 2021
    filtered_deaths_2021 = filtered_deaths.loc['2021']

    # Dropping rows where all specified county data is None
    filtered_deaths_2021 = filtered_deaths_2021.dropna(how='all')

    # Resampling the data by month and calculating the mean for each county
    df_monthly_deaths_2021 = filtered_deaths_2021.resample('M').sum()

    # Formatting the index to show only year and month
    df_monthly_deaths_2021.index = df_monthly_deaths_2021.index.strftime('%Y-%m')

    return df_monthly_deaths_2021

def get_monthly_vaccination_rates():
    """
    Extracts and aggregates monthly vaccination rate changes for 2021 for Dublin, Galway, Cork, and Limerick.

    Parameters:
    file_path (str): Path to the JSON file containing the vaccination data.

    Returns:
    pd.DataFrame: DataFrame containing the aggregated monthly vaccination rate changes for each city.
    """
    # Load the JSON file into a DataFrame
    df_vaccination = pd.read_json("cso\\vaccination_formatted.json")

    # Flatten the nested structure of the 'Monthly Percentage Point Change in Primary Course Completed' column
    flattened_vaccination = df_vaccination['Monthly Percentage Point Change in Primary Course Completed'].apply(pd.Series)

    # Identifying the keys for each city
    city_keys = {
        'Dublin': [key for key in flattened_vaccination.columns if 'Dublin' in key],
        'Galway': [key for key in flattened_vaccination.columns if 'Galway' in key],
        'Cork': [key for key in flattened_vaccination.columns if 'Cork' in key],
        'Limerick': [key for key in flattened_vaccination.columns if 'Limerick' in key]
    }

    # Convert the index to a DateTime index for resampling
    flattened_vaccination.index = pd.to_datetime(flattened_vaccination.index)

    # Selecting only the data for the year 2021
    flattened_vaccination_2021 = flattened_vaccination.loc['2021']

    # Creating a new DataFrame to hold the aggregated data
    df_monthly_vaccination_by_city = pd.DataFrame(index=flattened_vaccination_2021.index)

    # Aggregating the data for each city
    for city, keys in city_keys.items():
        df_monthly_vaccination_by_city[city] = flattened_vaccination_2021[keys].sum(axis=1)

    # Formatting the index to show only year and month
    df_monthly_vaccination_by_city.index = df_monthly_vaccination_by_city.index.strftime('%Y-%m')

    return df_monthly_vaccination_by_city

def get_weekly_covid_data():
    cities = ["Dublin City", "Cork County", "Galway County", "Limerick City and County"]
    with open('cso/covid_formatted.json', 'r') as file:
        data = json.load(file)

    # The data is nested under "Covid cases per 100,000 population"
    covid_data = data["Covid cases per 100,000 population"]

    # Extracting data
    all_cases = []
    for date, city_cases in covid_data.items():
        for city in cities:
            if city in city_cases:
                case_info = {'City': city, 'Date': date, 'CasesPer100k': city_cases[city]}
                all_cases.append(case_info)

    # Creating a DataFrame without index
    df = pd.DataFrame(all_cases)

    return df

def get_weekly_death_data():
    counties = ["Co. Dublin", "Co. Cork", "Co. Galway", "Co. Limerick"]
    
    # Load the JSON data
    with open('cso/death_formatted.json', 'r') as file:
        data = json.load(file)

    # Extract the data under "Total Deaths"
    death_data = data["Total Deaths"]

    # Create a list to store the data
    all_data = []

    # Iterate over the data and construct the list of dictionaries
    for date, county_deaths in death_data.items():
        for county in counties:
            if county in county_deaths and county_deaths[county] is not None:
                all_data.append({'County': county, 'Date': date, 'Deaths': county_deaths[county]})

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(all_data)

    return df

def get_weekly_vaccination_rates():
    city_keywords = ["Dublin", "Cork", "Galway", "Limerick"]
    with open('cso\\vaccination_formatted.json', 'r') as file:
        data = json.load(file)

    # The data is nested under various keys
    # We'll iterate through all keys to extract relevant data
    extracted_data = []
    for key in data.keys():
        for date, areas in data[key].items():
            for area, rate in areas.items():
                for city in city_keywords:
                    if city in area:
                        extracted_data.append({'City': city, 'Area': area, 'Date': date, 'VaccinationRate': rate})

    return pd.DataFrame(extracted_data)


monthly_covid_rates_2021 = get_monthly_covid_cases()
monthly_death_rates_2021 = get_monthly_death_rates()
monthly_vaccination_rates_2021 = get_monthly_vaccination_rates()
weekly_death_rates = get_weekly_death_data()
weekly_covid_rates = get_weekly_covid_data()
weekly_vaccination_rates = get_weekly_vaccination_rates()

