from Load_Data import winds_df, temp_rh_df, rain_df, grp
import plotly.express as px
import dash
from dash import html
from dash import dcc

#Figures
temp_fig = px.line(temp_rh_df, x='Date_Time', y='Temp_Air', title='Air Temperature (C)',
                   color_discrete_sequence=['red'], template="plotly_dark")
hum_fig = px.line(temp_rh_df, x='Date_Time', y='Rel_Hum', title='Relative Humidity (%)')
pres_fig = px.line(temp_rh_df, x='Date_Time', y='Pres_Air', title='Air Pressure (mbar)',
                   color_discrete_sequence=['green'])
wind_fig = fig = px.bar_polar(grp, theta="WD_avg", color="WS_avg", r='frequency',
                   color_discrete_sequence= px.colors.sequential.Plasma_r,
                   title="Wind Direction and Speed")
wind_fig.update_layout(template=None,
                       polar = dict(
                           radialaxis = dict(
                               showticklabels=False),
                           angularaxis = dict(
                               type='linear')
                            ))
#still need to change the degrees to direction in letters
#https://stackoverflow.com/questions/69106173/plotly-polar-bar-plot-setting-custom-theta-unit
rain_fig = px.bar(rain_df, x='Date_Time', y='Rain_Acc', title='Accumulated Rain (mm)')

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
                                    html.Div(dcc.Graph(figure=wind_fig), style={'display': 'inline-block'}),
                                    html.Div(dcc.Graph(figure=rain_fig), style={'display': 'inline-block'})],
                                    style={'textAlign': 'center', 'color': '#F57241'})
                      ])

# Run the application
if __name__ == '__main__':
    app.run_server()
