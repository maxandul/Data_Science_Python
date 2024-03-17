import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Wähle das Bootstrap Theme
BOOTSTRAP_THEME = dbc.themes.CYBORG  # Dies ist die URL für das Lux Theme

# Lade deinen DataFrame
df = pd.read_csv("data_exploration/titanic.csv")

# Initialisiere die Dash-App
app = dash.Dash(__name__, external_stylesheets=[BOOTSTRAP_THEME])

# Definiere die Spalten, die zur Auswahl stehen sollen
columns_to_include = ["Survived", "Pclass", "Sex", "Embarked", "Age"]

# App-Layout
app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in columns_to_include],
        value=columns_to_include[0]  # Standardmäßig die erste Spalte aus der Liste auswählen
    ),
    dcc.Graph(id='column-graph'),
    dcc.Graph(id='column-pie-chart'),  # Hinzugefügtes Element für das Kreisdiagramm
    html.Div(id='table-container')
])

# Callback für das Update des Graphen, des Kreisdiagramms und der Tabelle basierend auf der ausgewählten Spalte
@app.callback(
    [Output('column-graph', 'figure'),
     Output('column-pie-chart', 'figure'),  # Output für das Kreisdiagramm
     Output('table-container', 'children')],
    [Input('column-dropdown', 'value')]
)
def update_content(selected_column):
    # Überprüfe, ob die ausgewählte Spalte numerisch oder kategorisch ist
    if df[selected_column].dtype == 'object' or selected_column in ['Survived', 'Pclass', 'Sex', 'Embarked']:
        # Für kategorische Daten: Zeige Häufigkeitsverteilung und Kreisdiagramm
        value_counts = df[selected_column].value_counts().reset_index()
        value_counts.columns = ['unique_values', 'counts']
        fig_bar = px.bar(value_counts, x='unique_values', y='counts', title=f'Frequency of {selected_column}', template="plotly_dark")
        fig_pie = px.pie(value_counts, names='unique_values', values='counts', title=f'Percentage of {selected_column}', template="plotly_dark")
    else:
        # Für numerische Daten: Zeige nur das Histogramm (Kreisdiagramm ist für "Age" nicht sinnvoll)
        fig_bar = px.histogram(df, x=selected_column, title=f'Distribution of {selected_column}', template="plotly_dark")
        fig_pie = {}  # Leeres Diagramm, da Kreisdiagramm nicht anwendbar ist
    
    # Erstelle eine Tabelle für die ausgewählte Spalte
    table = html.Table([
        html.Thead(html.Tr([html.Th(selected_column)])),
        html.Tbody([html.Tr([html.Td(value)]) for value in df[selected_column].dropna().unique()])
    ], style={'width': '50%', 'display': 'inline-block'})
    
    return fig_bar, fig_pie, table

# Führe die App aus
if __name__ == '__main__':
    app.run_server(debug=True)
