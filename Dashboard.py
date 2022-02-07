from Load_Data import winds_df, temp_rh_df, rain_df, grp
import plotly.express as px
import dash
from dash import html
from dash import dcc

#Figures
#Possible templates: template='plotly_white', template='plotly_dark'
temp_fig = px.line(temp_rh_df, x='Date_Time', y='Temp_Air', #title='Air Temperature (C)',
                   color_discrete_sequence=['darkgrey'], template='plotly_white')
temp_fig.update_layout(title=dict(text='Air Temperature (C)',
                                  font=dict(size=24)),
                       xaxis_title='Date and Time',
                       yaxis_title='Temperature (C)',
                       font=dict(size=18))

hum_fig = px.line(temp_rh_df, x='Date_Time', y='Rel_Hum',#, title='Relative Humidity (%)',
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
                       polar = dict(
                           radialaxis = dict(
                               showticklabels=False,
                               type='linear')
                            ))
#still need to change the degrees to direction in letters

rain_fig = px.bar(rain_df, x='Date_Time', y='Rain_Acc', title='Accumulated Rain (mm)', template='plotly_white')
rain_fig.update_layout(title=dict(text='Accumulated Rain (mm)',
                                  font=dict(size=24)),
                       xaxis_title='Date and Time',
                       yaxis_title='Acc Rain (mm)',
                       font=dict(size=18))

#Dashboard
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('Weather Station Dashboard', style={'textAlign': 'center',
                                                                    'color': '#503D36', 'font-size': 40}),
                                html.Div([dcc.Graph(figure=temp_fig)],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([dcc.Graph(figure=hum_fig)],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([dcc.Graph(figure=pres_fig)],
                                         style={'textAlign': 'center', 'color': '#F57241'}),
                                html.Div([
                                    html.Div(dcc.Graph(figure=wind_fig),
                                             style={'display': 'inline-block', 'width': 990, 'height': 1600}),
                                    html.Div(dcc.Graph(figure=rain_fig),
                                             style={'display': 'inline-block', 'width': 2800, 'height': 1600})],
                                    style={'textAlign': 'center', 'color': '#F57241'})
                      ])

# Run the application
if __name__ == '__main__':
    app.run_server()
