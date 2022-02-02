import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('df_energy_vs_meteo.csv')
df_clean = df[['region (name)', 'Température (°C)', 'Humidité', 'annee_int', 'mois_int', 'Production totale', 'Consommation totale', 'population 2021']]

"""
Idées dashboard :
- évolution température vs temps pour une région donnée
- évolution humidité vs temps pour une région donnée
- évolution production vs consommation
- map avec consommation par région (curseur pour mois et année)
"""

app = dash.Dash(__name__)

# Here our layout i.e. how our page is going to look.
app.layout = html.Div(children=[
    # Display H1 title.
    html.H1(children="Energy dashboard"),

    # Display a paragraph inside a div.
    html.Div(children=html.P(children="""
        This product performs useful visualizations for electric energy consumption in France regions.
    """)),
    
    html.Div(children=html.P(children= df_clean['region (name)'][:5]  )),
])

if __name__ == "__main__":
    # Run the server!
    app.run_server(debug=True)