import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# 1. Carregar os dados
try:
    df = pd.read_csv('.venv/ecommerce_estatistica.csv')
except FileNotFoundError:
    df = pd.read_csv('/content/ecommerce_estatistica.csv')

# 2. Inicializar a aplicação Dash
app = Dash(__name__)

# 3. Layout da Aplicação
app.layout = html.Div([
    html.H1("Dashboard de Performance E-commerce", style={'textAlign': 'center', 'fontFamily': 'Arial'}),

    html.Div([
        html.Label("Selecione o Gênero (Categoria) para filtrar:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['Gênero'].unique())],
            value=df['Gênero'].unique()[0],
            clearable=False
        )
    ], style={'width': '40%', 'margin': '0 auto', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='revenue-graph'),
        dcc.Graph(id='rating-scatter')
    ], style={'display': 'flex', 'flexDirection': 'column'})
])


# 4. Callbacks para Interatividade
@app.callback(
    [Output('revenue-graph', 'figure'),
     Output('rating-scatter', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_graphs(selected_category):
    filtered_df = df[df['Gênero'] == selected_category]

    fig_rev = px.bar(
        filtered_df.groupby('Marca')['Preço'].sum().reset_index(),
        x='Marca', y='Preço',
        title=f'Receita Total por Marca - Categoria: {selected_category}',
        labels={'Preço': 'Receita (R$)'},
        color='Preço', color_continuous_scale='Viridis'
    )

    fig_scatter = px.scatter(
        filtered_df, x='Nota', y='Desconto',
        size='Preço', hover_name='Título',
        title=f'Distribuição de Notas e Descontos - {selected_category}',
        labels={'Nota': 'Avaliação', 'Desconto': 'Desconto (%)'}
    )

    return fig_rev, fig_scatter


# 5. Executar o servidor (Configurado para ambiente Local/PyCharm)
if __name__ == '__main__':
    app.run(debug=True)