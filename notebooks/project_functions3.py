#Import packages
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import plotly.express as px

def load_and_process(relative_file_path_zCSV, relative_file_path_cCSV):
    """
    Loads, cleans, processes, and wrangles zomato.csv
    
    Arguments:
    relative_file_path_zCSV - (str) the file path for the zomato.csv
    relative_file_path_cCSV - (str) the file path for the forex.csv
    """
    
    zCSV = pd.read_csv(relative_file_path_zCSV , encoding = "maclatin2")
    cCSV = pd.read_csv(relative_file_path_cCSV)
    currencyexchange_df = pd.DataFrame({"Currency":["INR","USD","GBP","BRL","AED","ZAR","NZD","TRY","BWP","IDR","QAR","LKR"],
                                    "Average exchange rate":[cCSV[cCSV["slug"].isin(["USD/INR"])]["open"].mean(),1,
                                                            cCSV[cCSV["slug"].isin(["USD/GBP"])]["open"].mean(),cCSV[cCSV["slug"].isin(["USD/BRL"])]["open"].mean(),
                                                            cCSV[cCSV["slug"].isin(["USD/AED"])]["open"].mean(),cCSV[cCSV["slug"].isin(["USD/ZAR"])]["open"].mean(),
                                                            cCSV[cCSV["slug"].isin(["USD/NZD"])]["open"].mean(),cCSV[cCSV["slug"].isin(["USD/TRY"])]["open"].mean(),
                                                            cCSV[cCSV["slug"].isin(["USD/BWP"])]["open"].mean(),cCSV[cCSV["slug"].isin(["USD/IDR"])]["open"].mean(),
                                                            cCSV[cCSV["slug"].isin(["USD/QAR"])]["open"].mean(),cCSV[cCSV["slug"].isin(["USD/LKR"])]["open"].mean()]})
    c_df = zCSV['Cuisines'].value_counts()
    
    #Method Chain 1 - Loading and Cleaning Zomato database
    zCSV = (
        zCSV.drop(zCSV.loc[zCSV["Rating text"]=="Not rated"].index)
        .drop(['Restaurant ID', 'Restaurant Name', 'Country Code', 'City', 'Address','Locality', 'Locality Verbose', 'Longitude', 'Latitude', 'Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu', 'Rating color', 'Rating text', 'Votes'], axis = 1)
        .replace({"Indian Rupees(Rs.)":"INR","Dollar($)":"USD","Pounds(Ł)":"GBP","Brazilian Real(R$)":"BRL","Emirati Diram(AED)":"AED",
                                                          "Rand(R)":"ZAR","NewZealand($)":"NZD","Turkish Lira(TL)":"TRY","Botswana Pula(P)":"BWP","Indonesian Rupiah(IDR)":"IDR",
                                                          "Qatari Rial(QR)":"QAR","Sri Lankan Rupee(LKR)":"LKR","Indonesia":"IDR"})
    )

    #Method Chain 2 - assigning new values to the database
    cCSV = (
        cCSV.assign(date= lambda x: pd.to_datetime(x["date"]))
        .assign(year=lambda x: x["date"].dt.year)
    )

    #Method Chain 3 - drop the rows in zCSV that are not from 2019 to 2020
    cCSV = (
        cCSV.drop(cCSV.loc[cCSV["year"].isin(range(2019,2020))==False].index)
    )

    #Method Chain 4 - Merging the series, currency exchange and Zomato database
    zCSV = (
        pd.DataFrame({'Cuisines':c_df.index, '# of Occurences' : c_df.values})
        .merge(zCSV, how = "inner",on = "Cuisines")
        .merge(currencyexchange_df, how="inner", on="Currency")
        .assign(Average_Cost_for_Two_USD= lambda x: x["Average Cost for two"] / x["Average exchange rate"])
    )
    
    return zCSV