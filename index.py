#import all modules
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

#initiate the app
# THEMAS DO DASBOARD    ################################
tab_card={
    'heigth':'100%'
}
main_config = {
    'hovermode': 'x unified',
    'legend': {
        'yanchor':'top',
        'y':0.9,
        'xanchor': 'left',
        'x': 0.1,
        'title':{'text': None},
        'font':{'collor': 'white'},
        'bg_collor': 'rgba(0,0,0,0,5)'},
    'margin': {'l':10, 'r': 10, 't': 10, 'b': 10}
}

url_theme1 = dbc.themes.CYBORG
url_theme2 = dbc.themes.VAPOR
template_theme1 = "cyborg"
template_theme2 = "vapor"
# Escolha um tema escuro do Plotly
#isso desliga os botões do plotly
config_graph = {
    'displayModeBar': False, 'showTips': False
}

#Read the files
df = pd.read_excel("Pasta1.xlsx", sheet_name="Planilha1")
#print(df)
df = df[df['Ciclos'] > 0]
df['Setor'] = 'Xaroparia'

#build the components
#POLAR GRAPH
def create_polar(selected_theme):
    # Escolha do tema Plotly  ///color_continuous_scale= 'rdylbu_r',
    theme = template_theme1 if selected_theme == url_theme1 else template_theme2
    #agrupar por grocesso 
    process_valve_count = df.groupby('Processo')['Valvula'].nunique().reset_index(name='Num_Valvulas')
    #ordenar de forma crescente
    process_valve_count = process_valve_count.sort_values(by='Num_Valvulas', ascending=False)
    fig = px.bar_polar(
        process_valve_count,
        r="Num_Valvulas",
        theta="Processo",
        color="Num_Valvulas",
        template="plotly_white",
        color_continuous_scale=px.colors.sequential.RdBu_r,
        height= 600,
        title= 'Distribuição das Válvulas por Processo'
    )
     # Remover a  legenda 
    fig.update_layout(template=theme, coloraxis_showscale=False)
    return fig

#BARGRAPH
# Função para criar gráfico de barras
def create_bar_graph(selected_theme):
    # Escolha do tema Plotly adequado
    theme = template_theme1 if selected_theme == url_theme1 else template_theme2

    # Ordenar DataFrame pelos valores de 'Ciclos' em ordem decrescente
    sorted_df = df.sort_values(by='Ciclos', ascending=False)

    # Selecionar os 30 maiores valores
    top_30_df = sorted_df.head(30)

    # Criar o gráfico de barras
    fig = px.bar(top_30_df, x='Valvula', y='Ciclos', color='Ciclos',
                 color_continuous_scale='RdBu_r',
                labels={'Ciclos': 'LifeExp'},
                title= 'Top 10',
                height= 600)

    # Aplicar o tema Plotly escolhido
    fig.update_layout(template=theme, coloraxis_showscale=False)

    return fig

#TREEMAP
# Função para criar treemap
def create_treemap(selected_theme):
    # Escolha do tema Plotly  ///color_continuous_scale= 'rdylbu_r',
    theme = template_theme1 if selected_theme == url_theme1 else template_theme2
    fig = px.treemap(df, path=['Setor', 'Area', 'Processo', 'Valvula'], values='Ciclos',
                     color='Ciclos', hover_data=['LifeExp'],
                     color_continuous_scale= 'rdylbu_r',
                     labels={'Ciclos': 'LifeExp'},
                     height=530,
                     width=2340
                    )
    # Aplicar o tema Plotly escolhido
    fig.update_layout(template=theme, margin=dict(t=1, l=250, r=350, b=1),coloraxis_showscale=False)

    return fig

#Design the app layout

app.layout = dbc.Container(children=[
    #Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([ #Card de Cabeçalho do Dashboard
                    dbc.Row([
                        dbc.Col([
                            html.H4("XAROPARIA - Ciclos de Válvulas", style={'textAlign': 'center', 
                            'color': '#ffffff', 'font': 'sans-serif','margin':'14px'}),
                            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2])
                        ], style={'margin': '1px'})
                    ])
                ])
            ])
        ],lg=12, md=12, sm=12),

    ], className= 'g-2 my-auto', style={'margin-top': '7px'}),

    #Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([ # Posicionamento do Gráfico 1
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='bargraph', 
                                className='dbc', 
                                config=config_graph, 
                                figure=create_bar_graph(url_theme1)),
                                ], style={'textAlign': 'center', 'margin': '1px'})
                    ])
                ])
            ], style= tab_card)
        ],lg=6, md=6, sm=6),

         dbc.Col([
            dbc.Card([
                dbc.CardBody([ # Posicionamento do Gráfico 2
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='polar', 
                                className='dbc', 
                                config=config_graph, 
                                figure=create_polar(url_theme1)),
                            ], style={'textAlign': 'center', 'margin': '1px'})
                    ])
                ])
            ], style= tab_card)
        ],lg=6, md=6, sm=6)
    ]),

    
    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([ # Posicionamento do Gráfico 3
                    dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='treemap', 
                                className='dbc', 
                                config=config_graph, 
                                figure=create_treemap(url_theme1),
                                style={'margin': 'auto'}),
                            ])
                    ])
                ])
            ], style= tab_card)
        ],lg=12, md=12, sm=12),
    ])
], fluid=True, style={'height':'100vh'})



#Run the app
# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True, port='8051')