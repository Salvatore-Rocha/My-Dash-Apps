import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import plotly.express as px 
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import dash_player as dp

#Reading the local file 
stocks = pd.read_csv(r"Dash_apps\Stocks_reader\mystocks.csv")

app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.SOLAR],
                 )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
                html.H1("Stocks Dashboard - 2023",
                        style={'textAlign': 'center', 
                               'color': '#457B9D', 
                               #'font-family': 'Trebuchet MS, sans-serif'
                               }
                        ),
                width = 12)
            ]),
], 
fluid = True,
className="dbc"
)



if __name__=='__main__':
    app.run_server(debug=True, port=8000)