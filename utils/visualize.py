import seaborn as sns
import matplotlib.pyplot as plt
from prep_data import PrepareData


class Visualize:
    def __init__(self):
        pass 

    def Daywise_plot(self, data= None, row = None, col = None, color1='red', color2='blue', title='DC Power'):
        cols = data.columns # take all column
        gp = plt.figure(figsize=(20,40)) 
        gp.subplots_adjust(wspace=0.2, hspace=0.5)
        for i in range(1, len(cols)+1):
            ax = gp.add_subplot(row,col, i)
            data[cols[i-1]].plot(ax=ax, color=color1)
            ax.set_title('{} {}'.format(title, cols[i-1]),color=color2)
        # Adjust the size of the figure to remove top and bottom space
        plt.subplots_adjust(top=0.95, bottom=0.05)
        plt.savefig('result/'+title+'.png')
        # Close the plot
        plt.close()

    def weather_info_plot(self, df_solar):
        sns_plot = sns.displot(data=df_solar, x="AMBIENT_TEMPERATURE", 
        kde=True, bins = 100,color = "red", facecolor = "#3F7F7F",height = 5, aspect = 3.5)
        sns_plot.figure.savefig("result/Ambient_temperature_frequency.png")
        plt.close()

    def daily_yield_plot(self, df_solar):
        sns_plot = sns.lmplot(y="DC_POWER",x="DAILY_YIELD",hue="SOURCE_KEY",col="SOURCE_KEY",height=3,col_wrap=4,data=df_solar,fit_reg=True)
        sns_plot.figure.savefig("result/daily_yield")
        plt.close()

    def daily_plot(self, daily_solar, title='Daily DC Power', color='red'):
        # daily_dc = df_solar.groupby('DATE')['DC_POWER'].agg('sum')
        ax = daily_solar.sort_values(ascending=False).plot.bar(figsize=(15,5), legend=True,color=color)
        plt.title(title)
        # Set the font size of the x-axis tick labels
        plt.xticks(fontsize='x-small')
        plt.yticks(fontsize='x-small')
        # adjust the font size of the legend
        ax.legend(fontsize='small')
        # adjust the plot dimensions to accommodate the legend
        plt.tight_layout()
        plt.savefig('result/'+title+'.png')
        # Close the plot
        plt.close()

if __name__ == '__main__':
    #data preparetion
    generation_data_loc = 'data/Plant_2_Generation_Data.csv'
    weather_data_loc = 'data/Plant_2_Weather_Sensor_Data.csv'
    data = PrepareData(generation_data_loc, weather_data_loc)
    df_solar = data.merge_process()

    #visualization
    visua_func = Visualize()
    solar_dc = df_solar.pivot_table(values='DC_POWER', index='TIME', columns='DATE')
    solar_irradiation = df_solar.pivot_table(values='IRRADIATION', index='TIME', columns='DATE')
    solar_ambiant_temp = df_solar.pivot_table(values='AMBIENT_TEMPERATURE', index='TIME', columns='DATE')
    visua_func.Daywise_plot(data=solar_dc, row=12, col=3, color1='red', color2='blue')
    visua_func.Daywise_plot(data=solar_irradiation, row=12, col=3, color1='blue', color2='blue', title='Irradiation')
    visua_func.Daywise_plot(data=solar_ambiant_temp, row=12, col=3, color1='darkgreen', color2='blue', title='Ambient temperature')

    daily_dc = df_solar.groupby('DATE')['DC_POWER'].agg('sum')
    visua_func.daily_plot(daily_dc, title='Daily DC Power', color='red')

    daily_ambient_temp = df_solar.groupby('DATE')['AMBIENT_TEMPERATURE'].agg('sum')
    visua_func.daily_plot(daily_ambient_temp, title='Daily ambient temperature', color='darkgreen')

    daily_irradiation = df_solar.groupby('DATE')['IRRADIATION'].agg('sum')
    visua_func.daily_plot(daily_ambient_temp, title='Daily irradiation', color='blue')

    visua_func.weather_info_plot(df_solar)
    visua_func.daily_yield_plot(df_solar)



   