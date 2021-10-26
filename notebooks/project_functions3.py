#Import packages
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import plotly.express as px

def load_and_process(relative_file_path):
    """
    Loads, cleans, processes, and wrangles zomato.csv
    
    Arguments:
    relative_file_path - (str) the file path for the zomato.csv
    """
    #Method Chain 1 - Loading and Cleaning Zomato database
    z_df = (
        pd.read_csv(relative_file_path , encoding = "maclatin2")
        .drop(['Restaurant ID', 'Restaurant Name', 'Country Code', 'City', 'Address','Locality', 'Locality Verbose', 'Longitude', 'Latitude', 'Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu', 'Rating color', 'Rating text', 'Votes', 'Average Cost for two', 'Currency'], axis = 1)
    )
    
    #Method Chain 2 - Creating new series containing counts of each Cuisine
    c_df = (
        z_df['Cuisines'].value_counts()
    )
    
    #Method Chain 3 - Merging the series and Zomato database
    zomato_df = (
        pd.DataFrame({'Cuisines':c_df.index, '# of Occurences' : c_df.values})
        .merge(z_df, how = "inner",on = "Cuisines")
    )
    
    return zomato_df