import mysql.connector
from mysql.connector import Error
import sql_queries as sq
import retrieve_data as rd
import pandas as pd
import numpy as np

#Function to create the database:
def create_database():
    database_query = sq.coviddb
    try:
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )

        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        if 'covid' not in [db[0] for db in cursor]:
            cursor.execute(database_query)        
            print("Connection to MySQL DB successful")
            print("Covid Database created successfully")
        else:
            print("Covid database already exists")

        cursor.close()

    except Error as e:
        print(f"The error '{e}' occurred")
    
# Function to create a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to create a table in the database
def create_table(connection, create_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print(f"Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Funtion to avoid duplicate data in tables:
def avoid_duplicates(connection, duplicate_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(duplicate_table_query)
        print("No duplicates found")
    except Error as e:
        print(f"The error '{e}' occurred")

# Functions to insert the dataframes into the sql database
def insert_covid_rates(connection):
    cursor = connection.cursor()
    covid_data = """
    INSERT IGNORE INTO covid_rates (City, Date, CasesPer100k) values (%s,%s,%s)
    ;
    """
    # Correcting the date format
    rd.weekly_covid_rates['Date'] = rd.weekly_covid_rates['Date'].str.replace(r'(\d{4} [a-zA-Z]+)(\d{2})', r'\1 \2', regex=True)
    rd.weekly_covid_rates['Date'] = pd.to_datetime(rd.weekly_covid_rates['Date']).dt.date

    # Ensure all NaN values are converted to None
    rd.weekly_covid_rates = rd.weekly_covid_rates.replace({np.nan: None})

    # Iterate over DataFrame rows
    for index, row in rd.weekly_covid_rates.iterrows():
        values = (row['City'], row['Date'], row['CasesPer100k'])
        cursor.execute(covid_data, values)

    # Committing the transaction
    connection.commit()

    # Closing cursor and connection
    cursor.close()
    print("Data inserted successfully into the 'covid_rates' table.")

def insert_death_rates(connection):
    cursor = connection.cursor()
    death_data = """
    INSERT IGNORE INTO death_rates (County, Date, Deaths) values (%s,%s,%s)
    ;
    """
    rd.weekly_death_rates['Date'] = rd.weekly_death_rates['Date'].str.replace(r'(\d{4} [a-zA-Z]+)(\d{2})', r'\1 \2', regex=True)
    rd.weekly_death_rates['Date'] = pd.to_datetime(rd.weekly_death_rates['Date'])
    rd.weekly_death_rates = rd.weekly_death_rates.replace({np.nan: None})
    for index, row in rd.weekly_death_rates.iterrows():
        values = (row['County'], row['Date'], row['Deaths'])
        cursor.execute(death_data, values)
    connection.commit()
    cursor.close()
    print("Data inserted successfully into the 'death_rates' table.")

def insert_vaccination_rates(connection):

    cursor = connection.cursor()
    vaccination_data = """
    INSERT IGNORE INTO vaccination_data (City, Area, Date, VaccinationRate) VALUES (%s, %s, %s, %s);
    """
    date_format = "%Y %B"  # Adjust this as per your actual date format in rd.weekly_vaccination_rates
    rd.weekly_vaccination_rates['Date'] = pd.to_datetime(rd.weekly_vaccination_rates['Date'], format=date_format, errors='coerce')
    rd.weekly_vaccination_rates['Date'] = rd.weekly_vaccination_rates['Date'].dt.strftime('%Y-%m-%d')
    rd.weekly_vaccination_rates = rd.weekly_vaccination_rates.replace({np.nan: None})

    for index, row in rd.weekly_vaccination_rates.iterrows():
        values = (row['City'], row['Area'], row['Date'], row['VaccinationRate'])
        cursor.execute(vaccination_data, values)

    connection.commit()
    cursor.close()
    print("Data inserted successfully into the 'vaccination_data' table.")

def create_and_insert():
    
    # Connect to the MySQL database
    host_name = 'localhost'
    db_name = 'covid'
    user_name = 'root'
    user_password = ''
    connection = create_connection(host_name, user_name, user_password, db_name)

    create_table(connection, sq.covid_table)
    create_table(connection, sq.deaths_table)
    create_table(connection, sq.vaccination_table)
    avoid_duplicates(connection, sq.covid_dup)
    avoid_duplicates(connection, sq.death_dup)
    avoid_duplicates(connection, sq.vacc_dup)
    insert_covid_rates(connection)
    insert_death_rates(connection)
    insert_vaccination_rates(connection)
    
    connection.close()

def sql_database_set_up():
    
    create_database()
    create_and_insert()

#if __name__ == "__main__":
    #sql_database_set_up()