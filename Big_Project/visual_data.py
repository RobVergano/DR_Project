import retrieve_data as rd
import pandas as pd
import matplotlib.pyplot as plt

def dublin_rates():
    
    # Extracting Dublin-specific data from each DataFrame
    df1 = covid['Dublin City']  # Replace with the exact column name if different
    df2 = deaths['Co. Dublin']  # Replace with the exact column name if different
    df3 = vacc['Dublin']       # Replace with the exact column name if different

    # Concatenating columns into a new DataFrame
    # Ensure that all DataFrames have the same index (months in this case)
    df_dublin = pd.concat([df1, df2, df3], axis=1)

    # Renaming columns for clarity
    df_dublin.columns = ['Covid cases per 100,000 population', 'Total Deaths', 'Total Vaccinations']
    df_dublin.drop('2021-12', inplace = True) # delete the december row since there is no data
    return df_dublin

def cork_rates():    
    
    df1 = covid['Cork County']  
    df2 = deaths['Co. Cork']
    df3 = vacc['Cork']           
    df_cork = pd.concat([df1, df2, df3], axis=1)    
    df_cork.columns = ['Covid cases per 100,000 population', 'Total Deaths', 'Total Vaccinations']
    df_cork.drop('2021-12', inplace = True) # delete the december row since there is no data
    return df_cork

def galway_rates():

    df1 = covid['Galway County']  
    df2 = deaths['Co. Galway']
    df3 = vacc['Galway']           
    df_galway = pd.concat([df1, df2, df3], axis=1)    
    df_galway.columns = ['Covid cases per 100,000 population', 'Total Deaths', 'Total Vaccinations']
    df_galway.drop('2021-12', inplace = True) # delete the december row since there is no data
    return df_galway

def limerick_rates():
    
    df1 = covid['Limerick City and County']  
    df2 = deaths['Co. Limerick']
    df3 = vacc['Limerick']           
    df_limerick = pd.concat([df1, df2, df3], axis=1)    
    df_limerick.columns = ['Covid cases per 100,000 population', 'Total Deaths', 'Total Vaccinations']
    df_limerick.drop('2021-12', inplace = True) # delete the december row since there is no data
    return df_limerick

def get_bar_plot(county_data, county_name, file_path):

    # Creating a DataFrame from the provided data
    data = {
        "Date": county_data.index,
        "Covid cases per 100,000 population": county_data["Covid cases per 100,000 population"],
        "Total Deaths": county_data["Total Deaths"],
        "Total Vaccinations": county_data["Total Vaccinations"]
    }

    df = pd.DataFrame(data)
    df.set_index("Date", inplace=True)

    # Plotting
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar', ax=plt.gca())
    plt.title(f'{county_name} - Covid Statistics Over Time')
    plt.ylabel('Values')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()  

def tables_and_bar_plot():
    
    d = get_bar_plot(dublin_rates(),"Dublin", "static\plots\dublin_plot.png")
    c = get_bar_plot(cork_rates(),"Cork", "static\plots\cork_plot.png")
    g = get_bar_plot(galway_rates(),"Galway", "static\plots\galway_plot.png")
    l = get_bar_plot(limerick_rates(),"Limerick", "static\plots\limerick_plot.png")
    print ("Monthly plots saved")
    return d,c,g,l


#Tables:
covid = rd.monthly_covid_rates_2021 
deaths = rd.monthly_death_rates_2021 
vacc = rd.monthly_vaccination_rates_2021 
dublin_stats = (round(dublin_rates().describe(),2).drop("count")).to_html()
cork_stats = (round(cork_rates().describe(),2).drop("count")).to_html()
lim_stats = (round(limerick_rates().describe(),2).drop("count")).to_html()
gal_stats = (round(galway_rates().describe(),2).drop("count")).to_html()

