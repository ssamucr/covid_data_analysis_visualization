import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv('./owid-covid-data-preprocesado.csv.gz')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # para servidores WSGI (gunicorn main:server)

cases_stringency_scatter = px.scatter(df,
                                          x='stringency_index',
                                          y='new_cases_per_million',
                                          color='stringency_index',
                                          color_continuous_scale='Viridis',
                                          title='Nuevos casos por millón vs índice de restricción')


cases_stringency_scatter.update_layout(
    plot_bgcolor='#0e1012',
    paper_bgcolor='#0e1012',
    font_color='white',
    title_font_color='white',
    xaxis_title_font_color='white',
    yaxis_title_font_color='white',
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label('Fecha: ', className='label-fecha'),
            dcc.DatePickerSingle(
                id='date-picker',
                date=df['date'].min(),
                display_format='YYYY-MM-DD'
            ),
        ], width=2, className='container-fecha'),
        dbc.Col(html.H1('Visualización de la propagación del COVID-19', className='title'), width=10)
    ], justify='center', align='center'),

    dbc.Row([
        dbc.Col([
            html.Label('Casos globales'),
            html.Div(id='global-cases', children="No hay datos para visualizar"),
            html.Div(id='new-global-cases', children="No hay datos para visualizar")
        ], width=3, className='columna-global', style={'border': '2px solid #F09819'}),
        dbc.Col([
            html.Label('Muertes globales'),
            html.Div(id='global-deaths', children="No hay datos para visualizar"),
            html.Div(id='new-global-deaths', children="No hay datos para visualizar")
        ], width=3, className='columna-global', style={'border': '2px solid #EB3349'}),
        dbc.Col([
            html.Label('Vacunaciones globales'),
            html.Div(id='global-vaccinations', children="No hay datos para visualizar"),
            html.Div(id='new-global-vaccinations', children="No hay datos para visualizar")
        ], width=3, className='columna-global', style={'border': '2px solid #93F9B9'})
    ], justify='center', align='center', className='container-global'),

    dbc.Row([
        dbc.Col([
            html.Label('Localización:', className='label-localizacion'),
            dcc.Dropdown(
                id='location-dropdown',
                options=[{'label': loc, 'value': loc} for loc in df['location'].unique()],
                value='Afghanistan'
            ),
            html.Div(id='location-info', children="No hay datos para visualizar"),
            html.Div(id='location-cases', children="No hay datos para visualizar"),
            html.Div(id='location-deaths', children="No hay datos para visualizar"),
            html.Div(id='location-vaccinations', children="No hay datos para visualizar")
        ], width=2, className='container-localizacion'),

        dbc.Col([
            dcc.Graph(id='cases-date-graph')
        ], width=5, className='container-grafica'),

        dbc.Col([
            dcc.Graph(id='deaths-date-graph')
        ], width=5, className='container-grafica')
    ], justify='center', align='center'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccinations-date-graph')
        ], width=5, className='container-grafica'),

        dbc.Col([
            dcc.Graph(id='deaths-vaccinations-graph')
        ], width=5, className='container-grafica')
    ], justify='end', align='center'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccination-map')
        ], width=12)
    ], justify='center', align='center'),

    dbc.Row([
        dbc.Col([
            html.Label('Selecciona países para colorear:'),
            dcc.Dropdown(
                id='country-color-dropdown',
                options=[{'label': loc, 'value': loc} for loc in df['location'].unique()],
                multi=True,
                value=['Afghanistan']
            ),
            dcc.Graph(id='vaccinated-deaths-scatter'),
        ], width=7),
        dbc.Col([
            dcc.Graph(id='cases-stringency-scatter', figure=cases_stringency_scatter)
        ], width=5, className='container-grafica')
    ], justify='center', align='center'),
])


@app.callback(
    [Output('global-cases', 'children'),
     Output('global-deaths', 'children'),
     Output('global-vaccinations', 'children'),
     Output('new-global-cases', 'children'),
     Output('new-global-deaths', 'children'),
     Output('new-global-vaccinations', 'children'),
     Output('location-info', 'children'),
     Output('location-cases', 'children'),
     Output('location-deaths', 'children'),
     Output('location-vaccinations', 'children'),
     Output('cases-date-graph', 'figure'),
     Output('deaths-date-graph', 'figure'),
     Output('vaccinations-date-graph', 'figure'),
     Output('deaths-vaccinations-graph', 'figure'),
     Output('vaccination-map', 'figure'),
     Output('vaccinated-deaths-scatter', 'figure')],
    [Input('date-picker', 'date'),
     Input('location-dropdown', 'value'),
     Input('country-color-dropdown', 'value')]
)
def update_dashboard(date, location, selected_countries):
    # Las filas agregadas de OWID (World, continentes, grupos de ingreso) se excluyen
    # de los totales globales para no contar los mismos casos varias veces.
    global_data = df[(df['date'] == date) & ~df['iso_code'].astype(str).str.startswith('OWID_')]
    general_data = df
    location_data = df[(df['date'] == date) & (df['location'] == location)]

    global_cases = global_data['total_cases'].sum()
    global_deaths = global_data['total_deaths'].sum()
    global_vaccinations = global_data['people_vaccinated'].sum()

    new_global_cases = global_data['new_cases_smoothed'].sum()
    new_global_deaths = global_data['new_deaths_smoothed'].sum()
    new_global_vaccinations = global_data['new_people_vaccinated_smoothed'].sum()

    location_cases = location_data['total_cases'].sum()
    location_deaths = location_data['total_deaths'].sum()
    location_vaccinations = location_data['people_vaccinated'].sum()

    cases_fig = px.line(
        df[df['location'] == location],
        x='date',
        y='total_cases_per_million',
        title='Casos por millón vs fecha'
    )

    deaths_fig = px.line(
        df[df['location'] == location],
        x='date',
        y='total_deaths_per_million',
        title='Muertes por millón vs fecha'
    )

    vaccinations_fig = px.line(
        df[df['location'] == location],
        x='date',
        y='people_vaccinated_per_hundred',
        title='Personas vacunadas por cada cien vs fecha'
    )

    deaths_vaccinations_fig = px.scatter(
        df[df['location'] == location],
        x='people_vaccinated_per_hundred',
        y='new_deaths_per_million',
        title='Nuevas muertes diarias vs Personas vacunadas'
    )

    map_fig = px.choropleth(
        global_data,
        locations='iso_code',
        color='people_vaccinated_per_hundred',
        hover_name='location',
        color_continuous_scale='Viridis',
        title='Vacunaciones globales'
    )

    filtered_data = general_data[general_data['location'].isin(selected_countries)]

    vaccinated_deaths_scatter = px.scatter(filtered_data,
                                           x='people_vaccinated_per_hundred',
                                           y='new_deaths_per_million',
                                           color='location',
                                           title='Personas vacunadas por cada ciento vs Nuevas muertes por millón')

    figures = [cases_fig, deaths_fig, vaccinations_fig, deaths_vaccinations_fig, map_fig, vaccinated_deaths_scatter]
    for fig in figures:
        fig.update_layout(
            plot_bgcolor='#0e1012',
            paper_bgcolor='#0e1012',
            font_color='white',
            title_font_color='white',
            xaxis_title_font_color='white',
            yaxis_title_font_color='white',
        )

    return (f"{global_cases:,.0f}", f"{global_deaths:,.0f}", f"{global_vaccinations:,.0f}",
            f"Nuevos +{new_global_cases:,.0f}", f"Nuevos +{new_global_deaths:,.0f}", f"Nuevos +{new_global_vaccinations:,.0f}",
            f"Información de {location}",
            f"Casos: {location_cases:,.0f}", f"Muertes: {location_deaths:,.0f}",
            f"Vacunaciones: {location_vaccinations:,.0f}",
            cases_fig, deaths_fig, vaccinations_fig, deaths_vaccinations_fig, map_fig,
            vaccinated_deaths_scatter)


if __name__ == '__main__':
    app.run(debug=True)
