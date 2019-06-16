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
        value=500,
        marks={str(x): str(x) for x in np.arange(0,2100,100)},
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
    cash_real = [starting_pot]
    for i in np.arange(num_years + 1):
        p_nom.append(p_nom[-1]*growth + 12*monthly_savings*1.0200)
        p_real.append(p_real[-1]*(1 + growth-1.0200) + 12*monthly_savings*1.0200)
        cash_real.append((cash_real[-1] + 12*monthly_savings)/1.0200)

    portfolio_nom = np.array(p_nom)
    portfolio_real = np.array(p_real)

    milestones = [50000,100000, 500000, 1000000]

    milestones = [m for m in milestones if m > starting_pot]


    milestone_years = []
    for m in milestones:
        if p_nom[-1] > m:
            milestone_years.append(year_range[np.argmax(np.array(portfolio_nom)>m)])
    
    annotations =  [dict(x = year, y = m, text = '£' + "{:,}".format(m) + ' saved by ' + str(year), 
                        showarrow = False,
                        bordercolor='#c7c7c7',
                        borderwidth=2,
                        borderpad=4,
                        bgcolor='#ff7f0e',
                        opacity=0.8) for (m,year) in zip(milestones, milestone_years)]
    

    cash_scatter = go.Scatter(x = year_range,
    y = cash_savings, name = 'Cash')

    cash_real_scatter = go.Scatter(x = year_range, y = cash_real,
    name = 'Cash adjusted for 2% inflation')

    portfolio_nom_scatter = go.Scatter(x=year_range, 
    y = portfolio_nom, name = 'Savings')

    portfolio_real_scatter = go.Scatter(x=year_range, 
    y = portfolio_real, name = 'Savings adjusted for 2% inflation')

    

    return {
        'data': [cash_scatter, cash_real_scatter, portfolio_nom_scatter,portfolio_real_scatter],
        'layout': go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Value', 'range':[0,1200000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            annotations=annotations
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)