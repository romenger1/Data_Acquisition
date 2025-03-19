import pandas as pd
import plotly_express as px

#POLAR GRAPH
def create_polar(selected_theme):
    # Escolha do tema Plotly  ///color_continuous_scale= 'rdylbu_r',
    theme = template_theme1 if selected_theme == url_theme1 else template_theme2
    fig = px.bar_polar(
        df,
        r=df["Processo"],
        theta=df["sssssss"],
        color=df["Processo"],
        template="plotly_white",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_layout(template=theme)
    return fig
