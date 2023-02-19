from dash import Dash, dcc, html, Input, Output, ctx
from pathlib import Path
# import PreventUpdate
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objs as go

import pandas as pd

import numpy as np

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
                        #    animation_frame="year",
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
df_f = df[(df.cause == 'Waste - agri-food systems') & (df.year == DEFAULT_YEAR)]
df_f.sort_values(by=['year'], inplace=True)

default_fig_map_fre = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value", 
                           size="value", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           color_continuous_scale=px.colors.sequential.Greys,
                        #    animation_frame="year",
                           projection="natural earth") 

default_fig_map_fre.update_layout(coloraxis_colorbar=dict(
    title="Total Food-waste emissions"
))

# Map showing the food related emissions
# in a given year
def draw_fig_map_fre(year):
    df_fre = df[(df.cause == ALL_CAUSES) & (df.year == year)]
    fig_fre = px.scatter_geo(df_fre, locations="iso_alpha", 
                           color="value", 
                           size="value", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           color_continuous_scale=px.colors.sequential.Greys,
                           projection='natural earth')

    fig_fre.update_layout(coloraxis_colorbar=dict(
        title="Total Food-waste emissions"
    ))   
    return fig_fre

# ============================================================
# Different causes of food-waste related emissions
# ============================================================

# Default bar chart showing the difference causes of emissions
dff = df[df.cause != ALL_CAUSES]
dom_wastewater = dff[dff.cause == 'Domestic wastewater'].value.sum()
ind_wastewater = dff[dff.cause == 'Industrial wastewater'].value.sum()
sol_food_waste = dff[dff.cause == 'Solid food waste'].value.sum()

# print(dom_wastewater, ind_wastewater, sol_food_waste)
default_fig_bar_causes = px.bar(x=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'], 
        y=[dom_wastewater, ind_wastewater, sol_food_waste],
        color=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'])

default_fig_bar_causes.update_layout(
    title=f'Causes of emissions summed up from 1990',
    xaxis_title="Food-waste cause",
    yaxis_title="Emissions (kt)",
)

def draw_general_fig_bar_causes(year):
    global df
    dff = df[df.cause != ALL_CAUSES]
    dff = dff[dff.year == year]
    dom_wastewater = dff[dff.cause == 'Domestic wastewater'].value.sum()
    ind_wastewater = dff[dff.cause == 'Industrial wastewater'].value.sum()
    sol_food_waste = dff[dff.cause == 'Solid food waste'].value.sum()
    fig_bar_causes = px.bar(x=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'],
            y=[dom_wastewater, ind_wastewater, sol_food_waste],
            color=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'])
    fig_bar_causes.update_layout(
        title=f'Causes of emissions in {year}',
        xaxis_title="Food-waste cause",
        yaxis_title="Emissions (kt)",
    )
    return fig_bar_causes


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
ind_wastewater = []
home_wastewater = []
solid_waste = []
for year in range(1990, 2020):
    tdf = dff[dff['year'] == year]
    ind_wastewater.append(tdf[tdf['cause'] == 'Industrial wastewater'].value.sum())
    home_wastewater.append(tdf[tdf['cause'] == 'Domestic wastewater'].value.sum())
    solid_waste.append(tdf[tdf['cause'] == 'Solid food waste'].value.sum())
res = dict()
res['Year'] = np.array(range(1990, 2020))
res['Industrial wastewater'] = np.array(ind_wastewater)
res['Domestic wastewater'] = np.array(home_wastewater)
res['Solid food waste'] = np.array(solid_waste)
rdf = pd.DataFrame(res)
default_fig_line_causes = px.line(rdf, x='Year', 
                            y=['Domestic wastewater', 'Industrial wastewater', 'Solid food waste'],
                            color_discrete_sequence=px.colors.qualitative.Dark24)

default_fig_line_causes.update_layout(
    title=f'Trend of food-waste related emissions from 1990 to 2019',
    xaxis_title="Year",
    yaxis_title="Emissions (kt)"
)

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

# ============================================================
# RIGHT TAB Food related emissions
# ============================================================
df_f = df
df_f = df[df.cause == 'Waste - agri-food systems']
df_f.sort_values(by=['year'], inplace=True)

anim_fig_map_fre = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value", 
                           size="value", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           color_continuous_scale=px.colors.sequential.Greys,
                           animation_frame="year",
                           projection="natural earth") 

anim_fig_map_fre.update_layout(coloraxis_colorbar=dict(
    title="Total Food-waste emissions"
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

    html.Button('Reset', id='btn-reset'),

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
                            dcc.Graph(id='id_fig_map_fre', figure=default_fig_map_fre)
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
        ]),

    # SHOULD GO ON RIGHT TAB
    dcc.Graph(id='anim_fig_map_fre', figure=anim_fig_map_fre)
        
])

LAST_YEAR = None
LAST_COUNTRY = None

# Update map and bar chart when year slider is changed
@app.callback(
    Output(component_id='id_fig_map_feote', component_property='figure'),
    Output(component_id='id_fig_bar_causes', component_property='figure'),
    Output(component_id='id_fig_line_causes', component_property='figure'),
    Output(component_id='id_fig_map_fre', component_property='figure'),
    Input(component_id='year-slider', component_property='value'),
    Input(component_id='id_fig_map_feote', component_property='clickData'),
    Input(component_id='btn-reset', component_property='n_clicks')
)
def update_over_year(value, clickData, btn_reset):
    global LAST_YEAR
    global LAST_COUNTRY

    global default_fig_map_feote
    global default_fig_bar_causes
    global default_fig_line_causes
    global default_fig_map_fre

    if clickData is not None:
        LAST_COUNTRY = clickData['points'][0]['hovertext']
    if value is not None:
        LAST_YEAR = value    

    if LAST_YEAR is not None and LAST_COUNTRY is None:
        return draw_fig_map_feote(LAST_YEAR), draw_general_fig_bar_causes(LAST_YEAR), default_fig_line_causes, draw_fig_map_fre(LAST_YEAR)
    
    if "btn-reset" == ctx.triggered_id:
        return draw_fig_map_feote(LAST_YEAR), draw_general_fig_bar_causes(LAST_YEAR), default_fig_line_causes, draw_fig_map_fre(LAST_YEAR)

    return draw_fig_map_feote(LAST_YEAR), draw_fig_bar_causes(LAST_COUNTRY, LAST_YEAR), draw_fig_line_causes(LAST_COUNTRY), draw_fig_map_fre(LAST_YEAR)


app.run_server(debug=True)