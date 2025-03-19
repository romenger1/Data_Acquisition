import pandas as pd
import plotly_express as px

# Função para criar treemap
def create_treemap(selected_theme):
    # Escolha do tema Plotly  ///color_continuous_scale= 'rdylbu_r',
    theme = template_theme1 if selected_theme == url_theme1 else template_theme2
    fig = px.treemap(df, path=['Setor', 'Area', 'Processo', 'Valvula'], values='Ciclos',
                     color='Ciclos', hover_data=['LifeExp'],
                     color_continuous_scale= 'rdylbu_r',
                     labels={'Ciclos': 'LifeExp'},
                     height= 860
                    )
    # Aplicar o tema Plotly escolhido
    fig.update_layout(template=theme, margin=dict(t=1, l=1, r=1, b=1))

    return fig