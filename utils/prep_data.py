import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

class PrepareData:
    def __init__(self, generation_data_loc, weather_data_loc):
        self.generation_data = self.read_csv(generation_data_loc)
        self.weather_data = self.read_csv(weather_data_loc)

        self.generation_data = self.change_time_fmt(self.generation_data, '%Y-%m-%d %H:%M')
        self.weather_data = self.change_time_fmt(self.weather_data, '%Y-%m-%d %H:%M:%S')

    def read_csv(self, file_name):
        return pd.read_csv(file_name)

    def change_time_fmt(self, pd_data, format):
        pd_data['DATE_TIME'] = pd.to_datetime(pd_data['DATE_TIME'],
                                            format = format)
        return pd_data
    
    def merge_process(self):
        df_solar = pd.merge(self.generation_data.drop(columns = ['PLANT_ID']), 
                        self.weather_data.drop(columns = ['PLANT_ID', 'SOURCE_KEY']), 
                        on='DATE_TIME')
        # adding separate time and date columns
        df_solar["DATE"] = pd.to_datetime(df_solar["DATE_TIME"]).dt.date
        df_solar["TIME"] = pd.to_datetime(df_solar["DATE_TIME"]).dt.time
        df_solar['DAY'] = pd.to_datetime(df_solar['DATE_TIME']).dt.day
        df_solar['MONTH'] = pd.to_datetime(df_solar['DATE_TIME']).dt.month
        df_solar['WEEK'] = pd.to_datetime(df_solar['DATE_TIME']).dt.week

        # add hours and minutes for ml models
        df_solar['HOURS'] = pd.to_datetime(df_solar['TIME'],format='%H:%M:%S').dt.hour
        df_solar['MINUTES'] = pd.to_datetime(df_solar['TIME'],format='%H:%M:%S').dt.minute
        df_solar['TOTAL MINUTES PASS'] = df_solar['MINUTES'] + df_solar['HOURS']*60

        # add date as string column
        df_solar["DATE_STRING"] = df_solar["DATE"].astype(str) # add column with date as string
        df_solar["HOURS"] = df_solar["HOURS"].astype(str)
        df_solar["TIME"] = df_solar["TIME"].astype(str)

        encoder = LabelEncoder()
        df_solar['SOURCE_KEY_NUMBER'] = encoder.fit_transform(df_solar['SOURCE_KEY'])
        
        return df_solar

    def get_input(self, df_solar):
        X = df_solar[['DAILY_YIELD','TOTAL_YIELD','AMBIENT_TEMPERATURE','MODULE_TEMPERATURE','IRRADIATION','DC_POWER']]
        y = df_solar['AC_POWER']
        return X,y
    

if __name__ == '__main__':
    generation_data_loc = 'data/Plant_2_Generation_Data.csv'
    weather_data_loc = 'data/Plant_2_Weather_Sensor_Data.csv'
    data = PrepareData(generation_data_loc, weather_data_loc)
    df_solar = data.merge_process()
    print(df_solar.head(2))
    print(df_solar.info())