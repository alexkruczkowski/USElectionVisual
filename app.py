# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from urllib.request import urlopen
import json
import data_prep as dp

#import df
df = dp.read_file('countypres_2000-2016.csv',FIPS_column = 'FIPS')
df_clean = dp.clean_up(df, unique_val = 'party')
edf = dp.read_file('Electoral_College_Votes.csv', '')
summary_df = dp.format_table(df_clean, edf)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': "https://fonts.googleapis.com/css2?family=Montserrat",
        'rel': 'stylesheet'
    }
    ]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.Title = 'US Election Data'

app.layout = html.Div(children=[
    html.Div(
        className="header",
        children=[
            html.Div(
                className="inner_header",
                children = [
                    html.Div(
                        className="logo_container",
                        children = [html.H1('AlexK Dashboard')]
                            ),
                    html.Ul(
                        className="navigation",
                        children = [
                            html.A(html.Li("LinkedIn"), href='https://www.linkedin.com/in/akruczkowski/', target="_blank"),
                            html.A(html.Li("Github"), href='https://github.com/alexkruczkowski', target="_blank"),
                            html.A(html.Li("Contact"), href="mailto:ak.kruczkowski@gmail.com", target="_blank")
                                    ]
                            )
                            ],
                    )
                ]
            ),
    html.Div(
        className = "title_container",
        children = [
            html.Div(
                className = "inner_title",
                children  = [
                    html.Div(
                        className = "title_container",
                        children = [html.H3('US Federal Elections Visualized')]
                            )
                            ]
                    )
                    ]
                ),

    html.Br(),

    html.Div(
        className = "row",
        children = [
            html.Div(
                className = "four columns",
                children = [
                    html.Div(
                        className = "dropdown_filter",
                        children = [
                            dcc.Dropdown(
                            id='select_year',
                            options=[
                                {'label':'2000', 'value':2000},
                                {'label':'2004', 'value':2004},
                                {'label':'2008', 'value':2008},
                                {'label':'2012', 'value':2012},
                                {'label':'2016', 'value':2016}],
                            multi=False,
                            value=2012
                            )
                        ]
                    )
                    
                ]
            ),
            html.Div(
                className = "eight columns",
                children = [
                    html.Div(
                        className = "exp_text_container",
                        children = [
                            html.H6('Visualization of federal US election results at a county and state level. Select a year to get started')
                        ]
                    )
                    
                ]
            )
        ]
    ),

    html.Br(),
    #html.Div(id='output_container',children = []),
    html.Div(
        className = "six columns",
        children = [
            html.Div(
                className = 'map_container',
                children = [
                    dcc.Graph(
                    id='example-graph',
                    figure={})
                ]
            )
            
            
            ]
    ),
    html.Div(
        className = "five columns", 
        children = [
            html.Div(
                className = 'results_table', 
                children = [
                    html.Div(
                        id = 'output_table', 
                        children = [
                            
                        ]
                    )
                ]
                )
            ]
    )
])

@app.callback(
    [#dash.dependencies.Output(component_id='output_container', component_property='children'),
     dash.dependencies.Output(component_id='example-graph', component_property='figure')
     ,dash.dependencies.Output(component_id='output_table', component_property='children')
     ],
    [dash.dependencies.Input(component_id='select_year', component_property='value')])
def update_output(value):
    print(value)
    print(type(value))

    #container = 'You have selected "{}"'.format(value)

    df_year = df_clean[df_clean['year'] == value]

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth(df_year, geojson=counties, locations='fips_code', color='dem_vs_rep',
                           color_continuous_scale=px.colors.diverging.RdBu,
                           scope="usa",
                
                           hover_data=['democrat_total','republican_total'],
                           labels={'dem_vs_rep':'democratic vs republican','democrat_total':'democratic votes','republican_total':'republican votes'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
    fig.show()

    df = summary_df[summary_df['year'] == value]
   
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        page_size = 51,
        fixed_rows={'headers': True},
        style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '45rem',},
        style_cell={
        'whiteSpace': 'normal',
        'height': 'auto', },
        style_cell_conditional=[
            {'if': {'column_id': 'state'},
            'maxWidth': '6vw',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',},
            {'if': {'column_id': 'electoral_votes'},
            'minWidth': '4vw',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',},
        ]
                                )

    return fig, table


if __name__ == '__main__':
    app.run_server(debug=True)