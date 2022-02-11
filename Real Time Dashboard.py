import plotly.express as px
import pandas as pd
import dash
from tkinter import filedialog
from datetime import datetime
from dash import html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

#Gets filepath
filepath = filedialog.askopenfilename() #opens a dialog for choosing the file to work with. Only takes the filepath name

#Starts the Dashboard
app = dash.Dash(__name__)

#------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True, the counter will no longer update
                interval=3*1000,    #increment the counter n_intervals every interval milliseconds
                n_intervals=0,      #number of times the interval has passed
    ),
    html.Div(children=[html.H1(id='output_data', style={'textAlign': 'center',
                                                    'color': '#503D36', 'font-size': 40}),
                                html.Div([dcc.Graph(id='temp_fig')],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([dcc.Graph(id='hum_fig')],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([dcc.Graph(id='pres_fig')],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([
                                    html.Div(dcc.Graph(id='wind_fig'),
                                             style={'display': 'inline-block', 'width': '35vw', 'height': 1800}),
                                    html.Div(dcc.Graph(id='rain_fig'),
                                             style={'display': 'inline-block', 'width': '60vw', 'height': 1800})],
                                    style={'textAlign': 'center', 'color': '#F57241'})
                      ])
])

#------------------------------------------------------------------------
@app.callback(
    [Output('output_data', 'children'),
     Output('temp_fig', 'figure'),
     Output('hum_fig', 'figure'),
     Output('pres_fig', 'figure'),
     Output('wind_fig', 'figure'),
     Output('rain_fig', 'figure')],
    [Input('my_interval', 'n_intervals')]
)
def update_graph(num):
    """update every 3 seconds"""
    if num==0:
        raise PreventUpdate
    else:
        # Data Prep
        weather_df = pd.read_csv(filepath)  # uses the retrieved file path name to load the file
        weather_df.columns = ['Date_Time', 'Code', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5',
                              'Col_6']  # Assigns names to the columns
        pd.to_datetime(weather_df['Date_Time'], format="%m/%d/%Y %H:%M:%S %p")

        # Simple way to break up the database depending on the data retrieval code
        winds_df = weather_df[
            weather_df['Code'] == '0R1']  # Assigns the data to a different dataframe depending on the retrieval code
        temp_rh_df = weather_df[weather_df['Code'] == '0R2']
        rain_df = weather_df[weather_df['Code'] == '0R3']

        # Let's start with the winds dataframe. These have a five seconds resolution
        # WD = Wind Direction in degrees
        winds_df['WD_min_dummy'] = winds_df['Col_1'].str.split('=').str[1]
        winds_df['WD_min'] = winds_df['WD_min_dummy'].str.split('D').str[0]
        winds_df['WD_avg_dummy'] = winds_df['Col_2'].str.split('=').str[1]
        winds_df['WD_avg'] = winds_df['WD_avg_dummy'].str.split('D').str[0]
        winds_df['WD_max_dummy'] = winds_df['Col_3'].str.split('=').str[1]
        winds_df['WD_max'] = winds_df['WD_max_dummy'].str.split('D').str[0]
        winds_df.drop(columns=['WD_min_dummy', 'WD_avg_dummy', 'WD_max_dummy'], inplace=True)
        # WS = Wind speed in m/s
        winds_df['WS_min_dummy'] = winds_df['Col_4'].str.split('=').str[1]
        winds_df['WS_min'] = winds_df['WS_min_dummy'].str.split('M').str[0]
        winds_df['WS_avg_dummy'] = winds_df['Col_5'].str.split('=').str[1]
        winds_df['WS_avg'] = winds_df['WS_avg_dummy'].str.split('M').str[0]
        winds_df['WS_max_dummy'] = winds_df['Col_6'].str.split('=').str[1]
        winds_df['WS_max'] = winds_df['WS_max_dummy'].str.split('M').str[0]
        winds_df.drop(columns=['WS_min_dummy', 'WS_avg_dummy', 'WS_max_dummy'], inplace=True)

        # Now for Temperature, Relative Humidity and Pressure
        # These have a one minute resolution
        temp_rh_df['Temp_Air_dummy'] = temp_rh_df['Col_1'].str.split('=').str[1]
        temp_rh_df['Temp_Air'] = temp_rh_df['Temp_Air_dummy'].str.split('C').str[0]
        temp_rh_df['Rel_Hum_dummy'] = temp_rh_df['Col_2'].str.split('=').str[1]
        temp_rh_df['Rel_Hum'] = temp_rh_df['Rel_Hum_dummy'].str.split('P').str[0]
        temp_rh_df['Pres_Air_dummy'] = temp_rh_df['Col_3'].str.split('=').str[1]
        temp_rh_df['Pres_Air'] = temp_rh_df['Pres_Air_dummy'].str.split('H').str[0]
        temp_rh_df.drop(columns=['Temp_Air_dummy', 'Rel_Hum_dummy', 'Pres_Air_dummy'], inplace=True)

        # Lastly for rain
        rain_df['Rain_Acc_dummy'] = rain_df['Col_1'].str.split('=').str[1]
        rain_df['Rain_Acc'] = rain_df['Rain_Acc_dummy'].str.split('M').str[0]
        rain_df['Rain_Dur_dummy'] = rain_df['Col_2'].str.split('=').str[1]
        rain_df['Rain_Dur'] = rain_df['Rain_Dur_dummy'].str.split('s').str[0]
        rain_df['Rain_Int_dummy'] = rain_df['Col_3'].str.split('=').str[1]
        rain_df['Rain_Int'] = rain_df['Rain_Int_dummy'].str.split('M').str[0]
        rain_df.drop(columns=['Rain_Acc_dummy', 'Rain_Dur_dummy', 'Rain_Int_dummy'], inplace=True)

        # All columns have to be changed to numbers for the visualizations
        winds_df[['WD_min', 'WD_avg', 'WD_max']] = winds_df[['WD_min', 'WD_avg', 'WD_max']].astype(float)
        winds_df[['WS_min', 'WS_avg', 'WS_max']] = winds_df[['WS_min', 'WS_avg', 'WS_max']].astype(float)
        temp_rh_df[['Temp_Air', 'Rel_Hum', 'Pres_Air']] \
            = temp_rh_df[['Temp_Air', 'Rel_Hum', 'Pres_Air']].astype(float)
        rain_df[['Rain_Acc', 'Rain_Dur', 'Rain_Int']] = rain_df[['Rain_Acc', 'Rain_Dur', 'Rain_Int']].astype(float)

        # Necesary column for the wind rose
        grp = winds_df.groupby(['WD_avg', 'WS_avg']).size().reset_index(name='frequency')

        y_data='Weather Station Dashboard'

        #Dashboard figures
        temp_fig = px.line(temp_rh_df, x='Date_Time', y='Temp_Air',  # title='Air Temperature (C)',
                           color_discrete_sequence=['darkgrey'], template='plotly_white')
        temp_fig.update_layout(title=dict(text='Air Temperature (C)',
                                          font=dict(size=24)),
                               xaxis_title='Date and Time',
                               yaxis_title='Temperature (C)',
                               font=dict(size=18))

        hum_fig = px.line(temp_rh_df, x='Date_Time', y='Rel_Hum',  # , title='Relative Humidity (%)',
                          color_discrete_sequence=['darkgoldenrod'], template='plotly_white')
        hum_fig.update_layout(title=dict(text='Relative Humidity (%)',
                                         font=dict(size=24)),
                              xaxis_title='Date and Time',
                              yaxis_title='Rel Humidity (%)',
                              font=dict(size=18))

        pres_fig = px.line(temp_rh_df, x='Date_Time', y='Pres_Air', title='Air Pressure (mbar)',
                           color_discrete_sequence=['green'], template='plotly_white')
        pres_fig.update_layout(title=dict(text='Atmospheric Pressure (mbar)',
                                          font=dict(size=24)),
                               xaxis_title='Date and Time',
                               yaxis_title='Pressure (mbar)',
                               font=dict(size=18))

        wind_fig = fig = px.bar_polar(grp, theta="WD_avg", r='frequency', color="WS_avg")
        wind_fig.update_layout(template='plotly_white', font=dict(size=16),
                               title=dict(
                                   text='Wind Direction and Speed',
                                   font=dict(size=24)),
                               polar=dict(
                                   radialaxis=dict(
                                       showticklabels=False,
                                       type='linear')
                               ))
        # still need to change the degrees to direction in letters

        rain_fig = px.bar(rain_df, x='Date_Time', y='Rain_Acc', title='Accumulated Rain (mm)', template='plotly_white')
        rain_fig.update_layout(title=dict(text='Accumulated Rain (mm)',
                                          font=dict(size=24)),
                               xaxis_title='Date and Time',
                               yaxis_title='Acc Rain (mm)',
                               font=dict(size=18))

    return (y_data,temp_fig, hum_fig, pres_fig, wind_fig, rain_fig)
#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)