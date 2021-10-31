#Importing libraries
import pandas as pd

#Define clean_and_merge_zomato() method
def clean_and_merge_zomato(zomato_file_path, country_codes_file_path):
    """
    Loads, cleans, processes, and wrangles zomato.csv and Country-Code.xlsx
    
    Arguments:
    zomato_file_path - (str) the file path for the zomato.csv
    
    country_codes_file_path - (str) the file path for the Country-Code.xlsx
    """
    
    #Method chain 1 - load in/clean zomato.csv
    zomato_df = (
     pd.DataFrame(pd.read_csv("..\\data\\raw\\zomato.csv" , encoding = "maclatin2"))
     .drop(["Address","Rating color","Locality","Locality Verbose","Switch to order menu","Restaurant ID"],axis = 'columns')
     .dropna()
     .rename(columns={"Average Cost for two": "Average Cost for Two", 
                      "Has Table booking": "Has Table Booking",
                      "Has Online delivery": "Has Online Delivery",
                      "Rating text": "Rating Text",
                      "Is delivering now": "Is Delivering Now",
                      "Price range": "Price Range",
                      "Aggregate rating": "Aggregate Rating",})
    )

    #Method chain 2 - load in Country-Code.xlsx
    country_df = (
        pd.DataFrame(pd.read_excel("..\\data\\raw\\Country-Code.xlsx"))
    )

    #Method chain 3 - process/wrangle/merge country_df and zomato_df
    zomato_cleaned = (
     pd.merge(zomato_df,country_df, how = "inner",on = "Country Code")
     .query('Country=="India"')
     .assign(x = zomato_df["Aggregate Rating"]/zomato_df["Average Cost for Two"])
     .rename(columns={"x": "Aggregate Rating/Average Cost for Two"})
     .drop(['Country Code', 'Country'], axis = 'columns')
    )
    
    return zomato_cleaned