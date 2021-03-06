import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('df_energy_vs_meteo.csv')
df_clean = df[['region (name)', 'Température (°C)', 'Humidité', 'annee_int', 'mois_int', 'Production totale', 'Consommation totale', 'population 2021']]
df_clean['mois_str'] = df_clean['mois_int'].apply(str)
df_clean['annee_str'] = df_clean['annee_int'].apply(str)
df_clean['date'] = df_clean['annee_str'] + '-' + df_clean['mois_str']
df_clean['date'] = pd.to_datetime(df_clean['date'])

# start with one imposed region : Auvergne-Rhône-Alpes (last 3 years)
df_auv = df_clean[df_clean['region (name)'] == "Auvergne-Rhône-Alpes"]
df_auv = df_auv[(df_auv['date'].dt.year == 2020) | (df_auv['date'].dt.year == 2019) | (df_auv['date'].dt.year == 2018) ]

# def region names :
region_names = df_clean['region (name)'].unique().tolist()

"""
Idées dashboard :
- évolution température vs temps pour une région donnée
- évolution humidité vs temps pour une région donnée
- évolution production vs consommation
- map avec consommation par région (curseur pour mois et année)
"""

def generate_graph():
    """This function takes a DataFrame and return a pie inside a component.
    """
    dataframe = df_auv
    fig = px.scatter(dataframe, x = 'date', y = 'Température (°C)', title = 'Temperature in Auvergne-Rhône-Alpes last tree years :')
    return dcc.Graph(
        id="Auvergne-temp-graph",
        figure=fig,
    )



app = dash.Dash(__name__)

# Here our layout i.e. how our page is going to look.
app.layout = html.Div(children=[

    # Display H1 title.
    html.H1(children="Energy dashboard"),

    # Display a paragraph inside a div.
    html.Div(children=html.P(children="""
        This product performs useful visualizations for electric energy consumption in France regions.
    """)),

    html.Div(

        children=[
                    html.P(children="Select your Region:"),

                    dcc.Dropdown(
                        id="select-region-name",
                        options=[{"label": name, "value": name}
                                 for name in region_names],
                    ),
                    html.Div(children = dcc.Graph(id = 'graph_temp'))
                ]
            )

    ])

@app.callback(
    dash.dependencies.Output("graph_temp", "figure"),
    dash.dependencies.Input("select-region-name", "value"))
def generate_graph_2(region = "Ile-de-France"):
    """This function takes a DataFrame and return a pie inside a component.
    """
    dataframe = df_clean[df_clean['region (name)'] == region]
    dataframe = dataframe[(dataframe['date'].dt.year == 2020) | (dataframe['date'].dt.year == 2019) | (dataframe['date'].dt.year == 2018) ]
    fig = px.scatter(dataframe, x = 'date', y = 'Température (°C)', title = 'Temperature in ' + region + ' last tree years :')
    return fig



if __name__ == "__main__":
    # Run the server!
    app.run_server(debug=True)