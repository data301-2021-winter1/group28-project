#Import Libraries
import numpy as np
import pandas as pd

def clean_and_merge_zomato(zomato_file_path, country_codes_file_path):
    """
    Loads, cleans, processes, and wrangles zomato.csv and Country-Code.xlsx
    
    Arguments:
    zomato_file_path - (str) the file path for the zomato.csv
    
    country_codes_file_path - (str) the file path for the Country-Code.xlsx
    """
    
    #Method chain 1 - load in/clean zomato.csv
    zomato_df = (
     pd.DataFrame(pd.read_csv(zomato_file_path, encoding = "maclatin2"))
     .drop(["Address","Rating color","Locality","Locality Verbose","Switch to order menu","Restaurant ID"],axis = 'columns')
     .dropna()
    )

    #Method chain 2 - load in Country-Code.xlsx
    country_df = (
        pd.DataFrame(pd.read_excel(country_codes_file_path))
    )

    #Method chain 3 - process/wrangle/merge country_df and zomato_df
    zomato_cleaned = (
     pd.merge(zomato_df,country_df, how = "inner",on = "Country Code")
     #zomato_df = zomato_df[(zomato_df['Aggregate rating'].isin([0.0])) == False]
     .set_index(['Country','City']) 
     .drop(['Country Code'], axis = 'columns')
    .query('Country=="India"')
    )
    
    return zomato_cleaned