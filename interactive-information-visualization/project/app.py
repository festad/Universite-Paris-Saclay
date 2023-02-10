from dash import Dash, dcc, html, Input, Output
from pathlib import Path

import plotly.express as px
import pandas as pd

SIZE_MAX = 40

path = Path(__file__).parent / 'dasy.csv'
df = pd.read_csv(path)

df_f = df
df_f = df[df.cause == 'Waste - agri-food systems']
df_f.sort_values(by=['year'], inplace=True)

# year = 2019
# df_f = df_f[df_f.year == year]

# Ratio of food-waste related emissions over total emissions
fig_feote = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_over_emission", 
                           size="value_over_emission", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX, 
                           color_continuous_scale=px.colors.sequential.Blues,
                           animation_frame="year",
                           projection="natural earth")

fig_feote.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "over total emissions"
))                           

# Food related emissions
fig_fre = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value", 
                           size="value", 
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           color_continuous_scale=px.colors.sequential.Greys,
                           animation_frame="year",
                           projection="natural earth") 

fig_fre.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions"
))   

# Food related emissions normalized by population
fig_frenp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_capita", 
                           size="value_per_capita",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Reds)

fig_frenp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per capita",
))                              

# Food related emissions normalized by GDP
fig_frengdp = px.scatter_geo(df_f, locations="iso_alpha", 
                           color="value_per_gdp", 
                           size="value_per_gdp",
                           hover_name="country",
                           # symbol='cause',
                           size_max=SIZE_MAX,
                           projection="natural earth", 
                           animation_frame="year",
                           color_continuous_scale=px.colors.sequential.Greens)

fig_frengdp.update_layout(coloraxis_colorbar=dict(
    title="Food-waste emissions\n" +
          "per GDP",
))                              

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Food waste'),
    html.Div([
        html.P('Source code:'),
        html.A('festad/Universite-Paris-Saclay/interactive-information-visualization', 
               href='https://github.com/festad/Universite-Paris-Saclay/tree/main/interactive-information-visualization/project')
    ]),
    dcc.Graph(figure=fig_feote),
    dcc.Graph(figure=fig_fre),
    dcc.Graph(figure=fig_frenp),
    dcc.Graph(figure=fig_frengdp),
])

app.run_server(debug=True)