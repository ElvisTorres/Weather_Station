from Load_Data import winds_df, temp_rh_df, rain_df
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib import ticker
from windrose import WindroseAxes
import seaborn as sns
from datetime import datetime


def Wind_Rose():
    wd = winds_df['WD_avg']
    ws = winds_df['WS_avg']
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    ax.set_xticklabels (['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'], fontsize=14)
    plt.title('Wind Direction and Speed (m/s)', fontsize=24)
    plt.show()

def Temp_and_RH():
    fig, ax = plt.subplots(figsize=(6, 3))  # sets the figure size
    ax = sns.lineplot(y='Temp_Air', x='Date_Time', data=temp_rh_df,
                      color='red')  # info for getting the line plot done
    plt.tight_layout()  # helps to not get the x tick labels cut off
    ax.set_title('Temperature and Relative Humidity', fontsize=20)
    ax2 = plt.twinx()  # creates the secondary axis
    sns.lineplot(y='Rel_Hum', x='Date_Time', data=temp_rh_df,
                 color='blue')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))  # sets the number of ticks in the x axis
    ax.tick_params(axis='x', rotation=35)  # rotates the x ticks for easier viewing
    ax.set_xlabel('Date and Time', fontsize=14)  # sets the x label
    ax.set_ylabel('Temperature ($C^o$)', fontsize=14)
    ax2.set_ylabel('Relative Humidity (%)', fontsize=14)  # sets the secondary axis label
    ax.yaxis.label.set_color('red')  # changes the axis label color
    ax2.yaxis.label.set_color('blue')
    plt.show()

def Rain():
    fig, ax = plt.subplots(figsize=(6, 3))  # sets the figure size
    ax = sns.barplot(y='Rain_Acc', x='Date_Time', data=rain_df,
                     color='lightblue')  # info for getting the line plot done
    plt.tight_layout()  # helps to not get the x tick labels cut off
    ax.set_title('Total Rain', fontsize=20)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))  # sets the number of ticks in the x axis
    ax.tick_params(axis='x', rotation=35)  # rotates the x ticks for easier viewing
    ax.set_xlabel('Date and Time', fontsize=14)  # sets the x label
    ax.set_ylabel('Total Rain (mm)', fontsize=14)
    plt.show()