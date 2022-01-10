import pandas as pd
from tkinter import filedialog
from datetime import datetime

filepath = filedialog.askopenfilename() #opens a dialog for choosing the file to work with. Only takes the filepath name
weather_df = pd.read_csv(filepath) #uses the retrieved file path name to load the file
weather_df.columns = ['Date_Time', 'Code', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5', 'Col_6'] #Assigns names to the columns
pd.to_datetime(weather_df['Date_Time'], format="%m/%d/%Y %H:%M:%S %p")

#Simple way to break up the database depending on the data retrieval code
winds_df = weather_df[weather_df['Code']=='0R1'] #Assigns the data to a different dataframe depending on the retrieval code
temp_rh_df = weather_df[weather_df['Code']=='0R2']
rain_df = weather_df[weather_df['Code']=='0R3']

#Let's start with the winds dataframe. These have a five seconds resolution
#WD = Wind Direction in degrees
winds_df['WD_min_dummy'] = winds_df['Col_1'].str.split('=').str[1]
winds_df['WD_min'] = winds_df['WD_min_dummy'].str.split('D').str[0]
winds_df['WD_avg_dummy'] = winds_df['Col_2'].str.split('=').str[1]
winds_df['WD_avg'] = winds_df['WD_avg_dummy'].str.split('D').str[0]
winds_df['WD_max_dummy'] = winds_df['Col_3'].str.split('=').str[1]
winds_df['WD_max'] = winds_df['WD_max_dummy'].str.split('D').str[0]
winds_df.drop(columns=['WD_min_dummy', 'WD_avg_dummy', 'WD_max_dummy'], inplace=True)
#WS = Wind speed in m/s
winds_df['WS_min_dummy'] = winds_df['Col_4'].str.split('=').str[1]
winds_df['WS_min'] = winds_df['WS_min_dummy'].str.split('M').str[0]
winds_df['WS_avg_dummy'] = winds_df['Col_5'].str.split('=').str[1]
winds_df['WS_avg'] = winds_df['WS_avg_dummy'].str.split('M').str[0]
winds_df['WS_max_dummy'] = winds_df['Col_6'].str.split('=').str[1]
winds_df['WS_max'] = winds_df['WS_max_dummy'].str.split('M').str[0]
winds_df.drop(columns=['WS_min_dummy', 'WS_avg_dummy', 'WS_max_dummy'], inplace=True)

#Now for Temperature, Relative Humidity and Pressure
#These have a one minute resolution
temp_rh_df['Temp_Air_dummy'] = temp_rh_df['Col_1'].str.split('=').str[1]
temp_rh_df['Temp_Air'] = temp_rh_df['Temp_Air_dummy'].str.split('C').str[0]
temp_rh_df['Rel_Hum_dummy'] = temp_rh_df['Col_2'].str.split('=').str[1]
temp_rh_df['Rel_Hum'] = temp_rh_df['Rel_Hum_dummy'].str.split('P').str[0]
temp_rh_df['Pres_Air_dummy'] = temp_rh_df['Col_3'].str.split('=').str[1]
temp_rh_df['Pres_Air'] = temp_rh_df['Pres_Air_dummy'].str.split('H').str[0]
temp_rh_df.drop(columns=['Temp_Air_dummy', 'Rel_Hum_dummy', 'Pres_Air_dummy'], inplace=True)

#Lastly for rain
rain_df['Rain_Acc_dummy'] = rain_df['Col_1'].str.split('=').str[1]
rain_df['Rain_Acc'] = rain_df['Rain_Acc_dummy'].str.split('M').str[0]
rain_df['Rain_Dur_dummy'] = rain_df['Col_2'].str.split('=').str[1]
rain_df['Rain_Dur'] = rain_df['Rain_Dur_dummy'].str.split('s').str[0]
rain_df['Rain_Int_dummy'] = rain_df['Col_3'].str.split('=').str[1]
rain_df['Rain_Int'] = rain_df['Rain_Int_dummy'].str.split('M').str[0]
rain_df.drop(columns=['Rain_Acc_dummy', 'Rain_Dur_dummy', 'Rain_Int_dummy'], inplace=True)

#All columns have to be changed to numbers for the visualizations
winds_df[['WD_min', 'WD_avg', 'WD_max']] = winds_df[['WD_min', 'WD_avg', 'WD_max']].astype(float)
winds_df[['WS_min', 'WS_avg', 'WS_max']] = winds_df[['WS_min', 'WS_avg', 'WS_max']].astype(float)
temp_rh_df[['Temp_Air', 'Rel_Hum', 'Pres_Air']] \
    = temp_rh_df[['Temp_Air', 'Rel_Hum', 'Pres_Air']].astype(float)
rain_df[['Rain_Acc', 'Rain_Dur', 'Rain_Int']] = rain_df[['Rain_Acc', 'Rain_Dur', 'Rain_Int']].astype(float)

#Necesary column for the wind rose
grp = winds_df.groupby(['WD_avg', 'WS_avg']).size().reset_index(name='frequency')




