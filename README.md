# BIG PROJECT: COVID Statistics 

Course: Data Representation 2023
Author: Roberto Vergano

## Project description

The aim of this project was to create and consume RESTful APIs while using a Flask server, AJAX and a SQL database. 

For the project, I wanted to study the COVID statistics in Dublin, Galway, Cork and Limerick. I created an app able to retrieve data from the cso website (1). Particularly, data from 3 different APIs: covid rates, death cases related to COVID, and vaccination rates. After formatting the json files, the data is uploaded to the “covid” SQL database (also created by the app). Through AJAX, the flask server is able to interact with the SQL database to perform CRUD operations.

## Getting started

Download the folder "Big_Project". This folder contains a python environment with all the packages and programs to run the app.

## Prerequisites

1. Python.
2. Please see requirements.txt in Big_Project folder for packages needed. 
3. Activate MySQL server, Wampserver64 was used for this project. Username: root. No password needed.
4. Activate python environment - **.\venv\Scripts\Activate.bat**
5. Internet browser.

## How does the app work?

1. Open your python environment.

2. Execute **python Myapp.py** - This program should execute all other programs in order to 
    - create the APIs, 
    - retrieve the data from cso webpage, 
    - connect to the SQL database, 
    - create the SQL database, 
    - upload the data to the SQL database, 
    - retrieve data from the SQL database, 
    - create plots and tables to display in the webpage,
    - create a flask server, 
    - send the data to the webpage, 
    - provide the web interface to perform CRUD operations with the SQL database
    
    **No other programs need to be executed**

3. The app should be running on **"http://127.0.0.1:5000"**

4. Webpage Login details
    - Username: data
    - Password: data

