#Este aplicativo executa a função principal de chamada para o Dash
#Executando o sistema Web em um servidor local

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally=True
server = app.server