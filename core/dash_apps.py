from django_plotly_dash import DjangoDash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Example Dataset
df = pd.DataFrame({
    'Year': [2015, 2016, 2017, 2018, 2019],
    'Happiness_Score': [7.5, 7.4, 7.3, 7.2, 7.1],
    'Region': ['Europe', 'Europe', 'Europe', 'Europe', 'Europe']
})

app = DjangoDash('example_interactive_dashboard')

app.layout = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in df['Year'].unique()],
        placeholder='Select Year'
    ),
    dcc.Graph(id='happiness-trend')
])

@app.callback(
    dash.dependencies.Output('happiness-trend', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    if selected_year:
        filtered_df = df[df['Year'] == selected_year]
    else:
        filtered_df = df

    fig = px.line(filtered_df, x='Year', y='Happiness_Score', title='Happiness Score Over Time')
    return fig

import matplotlib.pyplot as plt

# Static Chart
df.plot(x='Year', y='Happiness_Score', kind='bar')
plt.title('Happiness Score by Year')
plt.savefig('core/static/core/images/example_static_chart.png')

