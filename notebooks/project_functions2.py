# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

def load_and_process(zomato_file_path, forex_file_path, countrycode_file_path):
    """
    This method takes the loads, processes, and formats the zomato.csv file to be returned as a dataframe.
    
    Arguments:
    zomato_file_path - (str) the file path for zomato.csv
    forex_file_path - (str) the file path for forex.csv
    countrycode_file_path - (str) the file path for Country-Code.xlsx
    """
        
    forex_df = (
        pd.read_csv(forex_file_path)
        .assign(date=lambda x: pd.to_datetime(x["date"]))
        .assign(year=lambda x: x["date"].dt.year)
    )
    forex_df = (
        forex_df
        .drop(forex_df.loc[forex_df["year"].isin(range(2014,2019))==False].index)
    )
    
    currencyexchange_df = pd.DataFrame({"Currency":["INR","USD","GBP","BRL","AED","ZAR","NZD","TRY","BWP","IDR","QAR","LKR"],
                                    "Average exchange rate":[forex_df[forex_df["slug"].isin(["USD/INR"])]["open"].mean(),1,
                                                            forex_df[forex_df["slug"].isin(["USD/GBP"])]["open"].mean(),forex_df[forex_df["slug"].isin(["USD/BRL"])]["open"].mean(),
                                                            forex_df[forex_df["slug"].isin(["USD/AED"])]["open"].mean(),forex_df[forex_df["slug"].isin(["USD/ZAR"])]["open"].mean(),
                                                            forex_df[forex_df["slug"].isin(["USD/NZD"])]["open"].mean(),forex_df[forex_df["slug"].isin(["USD/TRY"])]["open"].mean(),
                                                            forex_df[forex_df["slug"].isin(["USD/BWP"])]["open"].mean(),forex_df[forex_df["slug"].isin(["USD/IDR"])]["open"].mean(),
                                                            forex_df[forex_df["slug"].isin(["USD/QAR"])]["open"].mean(),forex_df[forex_df["slug"].isin(["USD/LKR"])]["open"].mean()]})
    
    countrycode_df = pd.read_excel(countrycode_file_path)
    
    df1 = (
          pd.read_csv(zomato_file_path, encoding="latin2")
          .drop(["Address", "Locality", "Locality Verbose", "Switch to order menu", "Rating color", "Rating text"], axis='columns')
          .dropna()
    )
    
    df2 = (
          df1.drop(df1.loc[df1["Aggregate rating"]==0.0].index)
          
          .merge(countrycode_df, how="inner", on="Country Code")
          .assign(Currency=lambda x: x["Currency"].replace({"Indian Rupees(Rs.)":"INR","Dollar($)":"USD","Pounds(Ł)":"GBP","Brazilian Real(R$)":"BRL","Emirati Diram(AED)":"AED",
                                                      "Rand(R)":"ZAR","NewZealand($)":"NZD","Turkish Lira(TL)":"TRY","Botswana Pula(P)":"BWP","Indonesian Rupiah(IDR)":"IDR",
                                                      "Qatari Rial(QR)":"QAR","Sri Lankan Rupee(LKR)":"LKR","Indonesia":"IDR"})
                            )
          .merge(currencyexchange_df, how="inner", on="Currency")
          .rename(columns={"Average Cost for two":"Average_Cost"})
          .assign(Average_Cost=lambda x: round((x["Average_Cost"] / x["Average exchange rate"]),2))
          .assign(Currency="USD")
          .assign(Country=lambda x: x["Country"].replace({"Phillipines":"Philippines"}))
          .drop(["Country Code","Average exchange rate","Price range"], axis='columns')
          .reindex(["Country", "City", "Restaurant ID", "Restaurant Name", "Aggregate rating", "Longitude", "Latitude", "Cuisines", "Average_Cost", "Currency",
                       "Has Table booking", "Has Online delivery", "Is delivering now", "Votes"], axis=1)
          
          .reset_index()
      )

    return df2
