import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
from datetime import datetime

import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Input(id='starting-pot', type='number', value=0),
    dcc.Input(id='growth', type='number', value=1.065),
    dcc.Slider(
        id='savings-slider',
        min=0,
        max=2000,
        value=100,
        marks={str(x): str(x) for x in np.arange(0,2000,100)},
        step=None
    )
])

year = int(datetime.now().year)
num_years = 40
year_range = np.arange(year, year+num_years+1)
num_years_range = year_range - year
#growths = np.array(num_years*[growth])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('savings-slider', 'value'), Input('starting-pot', 'value'),
    Input('growth', 'value')])
def update(monthly_savings, starting_pot, growth):

    year = int(datetime.now().year)
    num_years = 40
    year_range = np.arange(year, year+num_years+1)
    num_years_range = year_range - year

    cash_savings = int(starting_pot) + 12*monthly_savings*num_years_range
    
    p_nom = [starting_pot]
    p_real = [starting_pot]
    for i in np.arange(num_years + 1):
        p_nom.append(p_nom[-1]*growth + 12*monthly_savings)
        p_real.append(p_real[-1]*(1 + growth-1.025) + 12*monthly_savings)

    portfolio_nom = np.array(p_nom)
    portfolio_real = np.array(p_real)

    cash_scatter = go.Scatter(x = year_range,
    y = cash_savings)

    portfolio_nom_scatter = go.Scatter(x=year_range, y = portfolio_nom)
    portfolio_real_scatter = go.Scatter(x=year_range, y = portfolio_real)

    return {
        'data': [cash_scatter, portfolio_nom_scatter,portfolio_real_scatter],
        'layout': go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Amount saved'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)