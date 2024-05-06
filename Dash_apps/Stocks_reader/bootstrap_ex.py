import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import plotly.express as px 
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
#A functions from pandas that extract stock data from various Internet sources into a pandas DataFrame.
import datetime as dt
import dash_player as dp

#Define the data range of the data we are interested in
start  = dt.datetime(2023,1,1)
end    = dt.datetime(2023,12,31)
"""
#Define wich stocks we want, and from which web are we getting them from (Stooq)
stocks = web.DataReader(
    ["BABA","ETSY","SWK","APPN","W","SNAP"],
    "stooq",
    start=start,
    end=end)

#Reshape Dataframe
stocks = stocks.stack().reset_index()

#The print line is used just to have a look of the Df in the terminal
#print(stocks[:15])

#The next lines will download the Df as a CSV file to our local environment. 
#This approach prevents overloading the API with requests every time we run the script, which could potentially lead to getting banned from the API
stocks.to_csv("mystocks.csv", index=False)
"""
#Reading the local file 
stocks = pd.read_csv("mystocks.csv")

#The print line is used just to have a look of the Df in the terminal
#print(stocks[:15])
#"""

# "__name__" is used as  "flask" is used under the hood
#WARNING: dbc.Container will not work if dbc.theme is not declared
#meta_tags are used to ensure that the app is responsive on mobile devices
app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.COSMO],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                 )

card_one = dbc.Card(
    dbc.CardBody(
        [
            html.H4("1️⃣ Select a Date", className="card-title"),
            html.H6("Dates are only availables for the year 2023 and should not fall on a weekend", className="card-subtitle1"),
            html.H6("If a date is not selected the histogram will not be shown", className="card-subtitle2",
                    style={"text-decoration": "underline red", }),
            dcc.DatePickerSingle(id='histo-date',
                                min_date_allowed= start,
                                initial_visible_month=dt.date(2023, 8, 5),
                                max_date_allowed= end,
                                #date= dt.datetime(2023, 3, 2)
                        ),
        ]
    ),
   style={"width": "18rem"},
)

card_two = dbc.Card(
    dbc.CardBody(
        [
            html.H4("2️⃣ Select Stocks", className="card-title"),
            html.H6("Please choose the stocks for which you’d like to view the closing values in the histogram", className="card-subtitle"),
            html.Br(),
            dcc.Checklist(id        ='my-checklist', 
                        value     = stocks["Symbols"].unique()[0:3],
                        options   = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())],
                        inline    = True,
                        inputStyle={"margin-left":"6px", "margin-right": "2px"}
                        )
        ]
    ),
    style={"width": "26rem"},
)

# Layout section
# ************************************************************************
app.layout = dbc.Container([
    # First we define the number of Rows the app will have, in this case 3 rows are declared
    # If a Row have more than one column, open a list "[]" that will include all of them
    # btw, Width 12 is the "max" columns we can have in one row; if excceded, the elements will colapse bellow the preceding elements
    # For default "dbc.Container([...], Fluid = False)"; Fluid will remove padding from left and right (white space) if set to True
    # Also for default, dash will render the columns as are written in the code; if the order needs to be change, we can use the parameter {"order": X} within "width"
    # no_gutters = False is set for default to add space between columns. no_gutters = True -> no space between columns, 
    dbc.Row([
        dbc.Col(
                html.H1("Stocks Dashboard - 2023",
                        #To assign multiple bootstrap classes to a single className parameter, just type a space and add it
                        style={'textAlign': 'center', 'color': '#457B9D', 'font-family': 'Trebuchet MS, sans-serif'}
                        ),
                width = 12)
            ]),
    dbc.Row([
        dbc.Col([
                dbc.Row(
                        [
                                dbc.Col(card_one, 
                                        width="auto"
                                        ),
                                dbc.Col(card_two, 
                                        width="auto"
                                        )
                        ]
                        ),
                dcc.Graph(id='my-hist', 
                            figure={}
                        ),
                ], width = {"size":6, "order":2}
                ),
        dbc.Col([
                dbc.Card([
                    dbc.CardBody(
                        html.P(
                            "But what are Stocks anyway?🪬👅🪬",
                            className="card-text")
                                ),
                    dp.DashPlayer(id="player",
                            url="https://www.youtube.com/watch?v=p7HKvqRI_Bo",
                            controls=False,
                            width="100%",
                                 ),
                        ]#,style={"width": "24rem"}
                        )
                ], width = {"size":6, "order":1}
                )
            ]),
    dbc.Row([
        dbc.Col([
                dcc.Dropdown(id     = "my-dpdn0-stks",
                            multi   = False,
                            value   = sorted(stocks["Symbols"].unique())[1], 
                            options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                            ),
                dcc.Graph(id     = "candle-stk",
                          figure = {}
                         )
                ])
            ]),
    dbc.Row([
        dbc.Col([
                dcc.Dropdown(id     = "my-dpdn-stks",
                            multi   = False,
                            value   = sorted(stocks["Symbols"].unique())[2], 
                            options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                            ),
                dcc.Graph(id   = "line-fig-stk",
                        figure = {}
                        ),
                ],
                width = {"size":6, "order":2}),
        dbc.Col([
                dcc.Dropdown(id      = "my-dpdn2-stks",
                             multi   = True,
                             value   = sorted(stocks["Symbols"].unique())[0:3],
                             options = [{"label": x,"value": x} for x in sorted(stocks["Symbols"].unique())]
                            ),
                dcc.Graph(id   = "line-fig2-stks",
                        figure = {}
                        ),
            
                ],
                width = {"size":6, "order":1})
            ]),
], fluid = True
)

# Candlestick chart - Single
@callback(
    Output("candle-stk", "figure"),
    Input("my-dpdn0-stks", 'value')
        )

def candlestick_plot(selected_stock):
        dff = stocks[stocks["Symbols"] == selected_stock]
        
        fig = go.Figure(data=[go.Candlestick(x=dff['Date'],
                open=dff['Open'],
                high=dff['High'],
                low=dff['Low'],
                close=dff['Close'])],
                #template=template
                )
        return fig

# Histogram chart - Multiple
@callback(
    Output("my-hist", "figure"),
    Input("my-checklist", 'value'),
    Input("histo-date","date")
        )

def histogram_plot(selected_stonks,date_set):
        dff = stocks[stocks["Symbols"].isin(selected_stonks)]
        dff = dff[dff['Date']==date_set]
        
        fig = px.histogram(dff, 
                           x='Symbols',
                           y='Close',
                           color= "Symbols",
                           text_auto= True,
                           #template=template,
                           )
        return fig

# Line chart - Sinple
@callback(
    Output("line-fig-stk", "figure"),
    Input("my-dpdn-stks", 'value')
        )

def single_line_plot(selected_stonk):
        dff = stocks[stocks["Symbols"] == selected_stonk]
        fig = px.line(dff, 
                      x='Date', 
                      y='High',
                      #template=template
                      )
        return fig

# Line chart - Multiple
@callback(
    Output("line-fig2-stks", "figure"),
    Input("my-dpdn2-stks", 'value')
        )

def multiple_lines_plot(selected_stonks):
        dff = stocks[stocks["Symbols"].isin(selected_stonks)]
        fig = px.line(dff, 
                      x="Date",
                      y="Close",
                      color= "Symbols",
                      #template=template,
                      hover_data=["Open","Close","High","Low"])
        return fig

if __name__=='__main__':
    app.run_server(debug=True, port=8000)