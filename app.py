from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

url= 'https://plotly.github.io/datasets/country_indicators.csv'

df = pd.read_csv(filepath_or_buffer=url)

app = Dash(__name__, title='My Dash App')

app.layout = html.Div([
    html.Div([
        html.H1(children="Scatter Plot", style={'margin':'3px 2px'}),
        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),
                'Fertility rate, total (births per woman)',
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),
                'Life expectancy at birth, total (years)',
                id='yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        id='year--slider',
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},

    )
], style={'border': '2px solid black', 'padding':'3px 8px'})

@callback(
    Output(component_id='indicator-graphic', component_property='figure'),
    Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
    Input(component_id='xaxis-type', component_property='value'),
    Input(component_id='yaxis-type', component_property='value'),
    Input(component_id='year--slider', component_property='value')
)
def update_fig(xaxis_column_name, yaxis_column_name,
               xaxis_type, yaxis_type, year_value):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0.05)'})

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_layout(transition={'duration':559})

    return fig

server = app.server

if __name__=="__main__":
    app.run_server(debug=True)
