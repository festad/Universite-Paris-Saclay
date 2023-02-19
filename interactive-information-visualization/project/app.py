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


# ============================================================
# RIGHT TAB
# ============================================================

# =========================================
# MAP - FOOD RELATED EMISSIONS
# =========================================
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

# ======================================================
# MAP - FOOD RELATED EMISSIONS NORMALIZED BY POPULATION
# ======================================================
df_f = df
df_f = df[df.cause == 'Waste - agri-food systems']
df_f.sort_values(by=['year'], inplace=True)

anim_fig_map_frenp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_capita", 
                           size="value_per_capita",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Reds)

anim_fig_map_frenp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per capita",
))                              

# ======================================================
# MAP - FOOD RELATED EMISSIONS NORMALIZED BY GDP
# ======================================================
df_f = df
df_f = df[df.cause == 'Waste - agri-food systems']
df_f.sort_values(by=['year'], inplace=True)

anim_fig_map_frengdp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_gdp", 
                           size="value_per_gdp",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Greens)

anim_fig_map_frengdp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per GDP",
))     

# =================================================================================
# Top polluters (countries) from 1990 to 2019, cause: 'Waste - agri-food systems'
# =================================================================================
dff = df[df.cause == 'Waste - agri-food systems']
# Put the countries as columns and the years as rows
dff = dff.pivot(columns='country', values='value', index='year')
# dff = dff[dff.index >= 2002]
dff.dropna(axis=1, inplace=True)
dff = dff.sum().sort_values(ascending=False).head(20)

fig_bar_top_polluters = px.bar(dff, x=dff.index, y=dff.values)
fig_bar_top_polluters.update_layout(
    title=f'Top polluters from 1990 to 2019',
    xaxis_title="Country",
    yaxis_title="Emissions (kt)",
)

# =================================================================================
# Top polluters (countries) from 1990 to 2019, cause: 'Waste - agri-food systems',
# normalized by population
# =================================================================================
dff = df[df.cause == 'Waste - agri-food systems']
# Put the countries as columns and the years as rows
dff = dff.pivot(columns='country', values='value_per_capita', index='year')
# dff = dff[dff.index >= 2002]
dff.dropna(axis=1, inplace=True)
dff = dff.sum().sort_values(ascending=False).head(20)

fig_bar_top_polluters_per_capita = px.bar(dff, x=dff.index, y=dff.values)
fig_bar_top_polluters_per_capita.update_layout(
    title=f'Top polluters per capita from 1990 to 2019',
    xaxis_title="Country",
    yaxis_title="Emissions (kt) per capita",
)

# =================================================================================
# Top polluters (countries) from 1990 to 2019, cause: 'Waste - agri-food systems',
# normalized by GDP
# =================================================================================
dff = df[df.cause == 'Waste - agri-food systems']
# Put the countries as columns and the years as rows
dff = dff.pivot(columns='country', values='value_per_gdp', index='year')
# dff = dff[dff.index >= 2002]
dff.dropna(axis=1, inplace=True)
dff = dff.rename(columns={'Central African Republic': 'C. African Rep.'})
dff = dff.sum().sort_values(ascending=False).head(20)

fig_bar_top_polluters_per_gdp = px.bar(dff, x=dff.index, y=dff.values)
fig_bar_top_polluters_per_gdp.update_layout(
    title=f'Top polluters per GDP from 1990 to 2019',
    xaxis_title="Country",
    yaxis_title="Emissions (kt) per $",
)


app = Dash(__name__)

str_intro_food_waste = """
Global food loss and waste is responsible for around 8% of the total emissions of greenhouse gases (GHG) in the world.
How much is the influence of food waste on the emissions of greenhouse gases in different countries?
Which countries are the biggest polluters? And what happens when we consider emissions per capita or per GDP?
This small interactive dashboard will help you investigating and answering these questions.
Keep in mind: the data are strictly related to the emissions of CH4 (methane) only, other
gases like N2O (nitrous oxide) or CO2 (carbon dioxide), although influential on the global warming, are not considered.
"""

str_feote_vs_fre = """
What immediately emerges from comparing these two maps is that the countries
in which food waste is a prevalent cause of emissions are not the biggest polluters
in terms of food waste emissions.
As an example, Rwanda is the first country a user can spot when looking at the first map,
but it's even difficult to find it in the second map.
The same, but inverse, goes for China or India, which are the biggest polluters in terms of food waste emissions,
but they are not among the countries with the highest food waste emissions over total emissions."""

str_causes = """
There are three main reasons for food waste emissions of CH4:
- Domestic waste of water,
- Industrial waste of water,
- Solid food waste.
These three causes influence the emissions in different ways in different countries and also over time.
Move the slider to see how the emissions of the three causes change over time and click on the bubbles
on one of the two maps on the left to focus on a specific country.
Click on the button 'Reset' to go back to the global view.
"""

str_normalizations = """
These maps, alongside the bar charts, show that the countries that most contributed to the global food waste emissions
from 1990. 
The bar charts show the sum of the values over the years.
Different points of view put in light different rankings: the top polluters are
not the top polluters per capita, which again are not the top polluters per GDP.
"""

app.layout = html.Div(children=[

    html.H1(children='Food waste emissions (1990-2019)', style={"width": "80%", "margin": "auto"}),
    html.Br(),

    html.H3(children=str_intro_food_waste, style={"width": "80%", "margin": "auto"}),
    html.Br(),
    html.Br(),

    # dcc.Slider(
    #     id='year-slider',
    #     min=df_f.year.min(),
    #     max=df_f.year.max(),
    #     value=df_f.year.min(),
    #     marks={str(year): str(year) for year in df_f.year.unique()},
    #     step=None
    # ),

    # html.Button('Reset', id='btn-reset'),

    html.Table(style={'width': '100%'}, children=[
        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(str_feote_vs_fre, style={"width": "80%", "margin": "auto"}),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(str_causes, style={"width": "80%", "margin": "auto"}),
            ])
        ]),
        html.Br(),
        html.Br(),

        html.Tr(children=[
            html.Td(style={'width': '50%', "margin": "auto"}, children=[
                dcc.Slider(
                    id='year-slider',
                    min=df_f.year.min(),
                    max=df_f.year.max(),
                    value=df_f.year.min(),
                    marks={str(year): str(year) for year in df_f.year.unique()},
                    step=None
                ),
            ]),
            html.Td(style={'width': '50%', "margin": "auto"}, children=[
                # Reset button
                html.Div(
                    style={"width": "50px"}
                ),
                html.Button('Reset', id='btn-reset'),
            ])
        ]),
        html.Br(),

        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_feote', figure=default_fig_map_feote)
                            ]),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_bar_causes', figure=default_fig_bar_causes)
                        ])
            ])
        ]),
        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_fre', figure=default_fig_map_fre)
                            ]),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_line_causes', figure=default_fig_line_causes)
                        ])
            ])
        ]),
    ]),
    html.Br(),
    html.Br(),



    # html.Div(style={'display': 'grid', 
    #                          'gridTemplateColumns': '1fr 1fr', 
    #                          'height': '100vh'}, 

    #         children=[

    #         # First column
    #         html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
    
    #             html.Div(str_feote_vs_fre, style={}),
                
    #             html.Div(style={},
    #                     children=[
    #                         dcc.Graph(id='id_fig_map_feote', figure=default_fig_map_feote)
    #                         ]),

    #             html.Div(style={},
    #                     children=[
    #                         dcc.Graph(id='id_fig_map_fre', figure=default_fig_map_fre)
    #                         ])
    #         ]),

    #         # Second column
    #         html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
    
    #             html.Div(str_causes, style={}),

    #             html.Div(style={},
    #                     children=[
    #                         dcc.Graph(id='id_fig_bar_causes', figure=default_fig_bar_causes)
    #                     ]),

    #             html.Div(style={},
    #                     children=[
    #                         dcc.Graph(id='id_fig_line_causes', figure=default_fig_line_causes)
    #                     ])
    #         ])
    #     ]),

        


        html.Div(str_normalizations, style={"width": "80%", "margin": "auto"}),
        html.Br(),
        html.Br(),
        # html.Div(style={'display': 'grid', 
        #                      'gridTemplateColumns': '1fr 1fr', 
        #                      'height': '100vh'}, 

        #     children=[

        #     # First column
        #     html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='id_anim_fig_map_fre', figure=anim_fig_map_fre)
        #                     ]),
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='id_fig_map_frenp', figure=anim_fig_map_frenp)
        #                     ]),
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='id_fig_map_frengdp', figure=anim_fig_map_frengdp)
        #                     ])

        #         # methane_dbc
        #     ]),

        #     # Second column
        #     html.Div(style={'display': 'grid', 'gridTemplateRows': '1fr 1fr'}, children=[
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='fig_bar_top_polluters', figure=fig_bar_top_polluters),
        #                 ]),
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='fig_bar_top_polluters_per_capita', figure=fig_bar_top_polluters_per_capita),
        #                 ]),
        #         html.Div(style={},
        #                 children=[
        #                     dcc.Graph(id='fig_bar_top_polluters_per_gdp', figure=fig_bar_top_polluters_per_gdp),
        #                 ])
        #     ])
        # ])

    # SHOULD GO ON RIGHT TAB
    # dcc.Graph(id='anim_fig_map_fre', figure=anim_fig_map_fre),
    # dcc.Graph(id='fig_bar_top_polluters', figure=fig_bar_top_polluters),
    # dcc.Graph(id='fig_bar_top_polluters_per_capita', figure=fig_bar_top_polluters_per_capita),
    # dcc.Graph(id='fig_bar_top_polluters_per_gdp', figure=fig_bar_top_polluters_per_gdp)
        
    html.Table(style={'width': '100%'}, children=[
        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_anim_fig_map_fre', figure=anim_fig_map_fre)
                            ]),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_bar_top_polluters', figure=fig_bar_top_polluters)
                            ]),
            ])
        ]), 

        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_frenp', figure=anim_fig_map_frenp)
                            ]),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_bar_top_polluters_per_capita', figure=fig_bar_top_polluters_per_capita)
                            ]),
                ]),
        ]),

        html.Tr(children=[
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_map_frengdp', figure=anim_fig_map_frengdp)
                            ]),
            ]),
            html.Td(style={'width': '50%'}, children=[
                html.Div(style={},
                        children=[
                            dcc.Graph(id='id_fig_bar_top_polluters_per_gdp', figure=fig_bar_top_polluters_per_gdp)
                        ]),
            ])
        ])
    ])

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