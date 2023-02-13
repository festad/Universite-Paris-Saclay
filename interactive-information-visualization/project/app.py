from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
# import PreventUpdate
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objs as go

import pandas as pd

SIZE_MAX = 40

path = Path(__file__).parent / 'dasy.csv'
df = pd.read_csv(path)

ALL_CAUSES = 'Waste - agri-food systems'

DEFAULT_YEAR = 2019
DEFAULT_COUTRY = 'France'

# df_f = df
# df_f = df[df.cause == 'Waste - agri-food systems']
# df_f.sort_values(by=['year'], inplace=True)

# year = 2019
# df_f = df_f[df_f.year == year]



# ============================================================
# FIGURES 
# ============================================================

# ============================================================
# Ratio of food-waste related emissions over total emissions
# ============================================================

# Default map showing the ratio of food-waste related emissions over total emissions
dff = df[(df.cause == ALL_CAUSES) & (df.year == DEFAULT_YEAR)]
default_fig_map_feote = px.scatter_geo(dff, locations="iso_alpha", 
                           color="value_over_emission", 
                           size="value_over_emission", 
                           hover_name="country",
                           size_max=SIZE_MAX, 
                           color_continuous_scale=px.colors.sequential.Viridis_r,
                           # animation_frame="year",
                           projection="natural earth")

default_fig_map_feote.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "over total emissions"
))                       

# Map showing the ratio of food-waste related emissions over total emissions
# in a given year
def draw_fig_map_feote(year):
    df_feote = df[(df.cause == ALL_CAUSES) & (df.year == year)]
    fig_feote = px.scatter_geo(df_feote, locations="iso_alpha", 
                           color="value_over_emission", 
                           size="value_over_emission", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX, 
                           color_continuous_scale=px.colors.sequential.Viridis_r,
                           projection='natural earth')

    fig_feote.update_layout(coloraxis_colorbar=dict(
        title="Food-waste emissions\n" +
              "over total emissions"
    ))   
    return fig_feote

# ============================================================
# Food related emissions
# ============================================================
df_f = df
df_f = df[df.cause == 'Waste - agri-food systems']
df_f.sort_values(by=['year'], inplace=True)

default_fig_map_fre = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value", 
                           size="value", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           color_continuous_scale=px.colors.sequential.Greys,
                           animation_frame="year",
                           projection="natural earth") 

default_fig_map_fre.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions"
))   

# ============================================================
# Different causes of food-waste related emissions
# ============================================================

# Default bar chart showing the difference causes of emissions
dff = df[df.cause != ALL_CAUSES]
dom_wastewater = dff[dff.cause == 'Domestic wastewater'].value.sum()
ind_wastewater = dff[dff.cause == 'Industrial wastewater'].value.sum()
sol_food_waste = dff[dff.cause == 'Solid food waste'].value.sum()

print(dom_wastewater, ind_wastewater, sol_food_waste)
default_fig_bar_causes = px.bar(x=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'], y=[dom_wastewater, ind_wastewater, sol_food_waste])

# Bar chart showing the difference causes of emissions
# in a given country and in a given year
def draw_fig_bar_causes(country, year):
    df_cause = df[(df.country == country) & (df.year == year) & (df.cause != ALL_CAUSES)]
    fig_cause = px.bar(df_cause, x='cause', y='value', color='cause')
    fig_cause.update_layout(
        title=f'Causes of emissions in {country} in {year}',
        xaxis_title="Food-waste cause",
        yaxis_title="Emissions (kt)",
    )
    return fig_cause


# ==========================================================
# LINE CHART - TREND OF FOOD-WASTE RELATED 
# EMISSIONS IN A GIVEN COUNTRY
# ==========================================================

# Default line chart showing the trend of food-waste related emissions
dff = df[df.cause != ALL_CAUSES]
default_fig_line_causes = px.line(dff, x='year', y='value', color='cause')

# Line chart showing the trend of food-waste related emissions
# in a given country
def draw_fig_line_causes(country):
    df_trend = df[(df.country == country) & (df.cause != ALL_CAUSES)]
    fig_trend = px.line(df_trend, x='year', y='value', color='cause')
    fig_trend.update_layout(
        title=f'Trend of food-waste related emissions in {country}',
        xaxis_title="Year",
        yaxis_title="Emissions (kt)",
    )
    return fig_trend


# Food related emissions normalized by population
default_fig_map_frenp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_capita", 
                           size="value_per_capita",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Reds)

default_fig_map_frenp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per capita",
))                              

# Food related emissions normalized by GDP
default_fig_map_frengdp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_gdp", 
                           size="value_per_gdp",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Greens)

default_fig_map_frengdp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per GDP",
))                              

app = Dash(__name__)



app.layout = html.Div(children=[
    dcc.Slider(
        id='year-slider',
        min=df_f.year.min(),
        max=df_f.year.max(),
        value=df_f.year.min(),
        marks={str(year): str(year) for year in df_f.year.unique()},
        step=None
    ),
    html.Div(style={'display': 'grid', 
                             'gridTemplateColumns': '1fr 1fr', 
                             'height': '100vh'}, 

            children=[

            # First column
            html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_feote', figure=default_fig_map_feote)
                            ]),
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_frengdp', figure=default_fig_map_frengdp)
                            ])
                # methane_dbc
            ]),

            # Second column
            html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_bar_causes', figure=default_fig_bar_causes)
                        ]),
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_line_causes', figure=default_fig_line_causes)
                        ])
            ])
        ])
])

LAST_YEAR = 2019
LAST_COUNTRY = 'France'

# Update map and bar chart when year slider is changed
@app.callback(
    Output(component_id='id_fig_map_feote', component_property='figure'),
    Output(component_id='id_fig_bar_causes', component_property='figure'),
    Output(component_id='id_fig_line_causes', component_property='figure'),
    Input(component_id='year-slider', component_property='value'),
    Input(component_id='id_fig_map_feote', component_property='clickData')
)
def update_over_year(value, clickData):
    global LAST_YEAR
    global LAST_COUNTRY
    if value is None or clickData is None:
        raise PreventUpdate
    else:
        LAST_YEAR = value
        LAST_COUNTRY = clickData['points'][0]['hovertext']
        return draw_fig_map_feote(value), draw_fig_bar_causes(LAST_COUNTRY, LAST_YEAR), draw_fig_line_causes(LAST_COUNTRY)

app.run_server(debug=True)