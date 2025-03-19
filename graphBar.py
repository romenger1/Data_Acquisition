import pandas as pd
import plotly_express as px


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
                labels={'Ciclos': 'LifeExp'})

    # Aplicar o tema Plotly escolhido
    fig.update_layout(template=theme)

    return fig