import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table
import numpy as np
import pandas as pd
import pathlib
import plotly.express as px 
from dash.dependencies import Input, Output, State

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))

df_median_earn = pd.read_csv(DATA_PATH.joinpath("df_median_earn6.csv"))

df_tuition = pd.read_csv(DATA_PATH.joinpath("df_TUITFTE_YEAR_STABBR.csv"))

df_dict={}
for i in range(2005,2019):
    filename = "df_tuition_"+str(i)+".csv"
    df = pd.read_csv(DATA_PATH.joinpath(filename))
    df_dict[i] = df






YEARS = list(np.arange(2005,2019))


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Tuition fees"),
                                    html.Br([]),
                                    html.P(
                                        "Student debt in the US amounts to $1.73 trillion. \
                                        Tuition in post-secondary institutions has continuously risen,\
                                        with a nation-wide average of $35,720 per student per year. \
                                        Moreover, employment prospects and income post-graduation are \
                                        widely variable for different majors and industries. \
                                        The decision to incur debt to afford higher education becomes, \
                                        in essence, a financial one, with consequences that affect the \
                                        livelihoods of millions of people. \
                                        Several policy makers have proposed ways to lessen the burden of \
                                        student debt on borrowers, but questions still remain about \
                                        the feasibility and impact of such measures on financial and \
                                        post-secondary institutions and on borrowers themselves.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Tuition Facts"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Distribution of median tuition fees over time",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id="box-plot",
                                             figure = generate_boxplot_median_tuition()),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Median tuition fees by state",
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        id="slider-container",
                                        children=[
                                            html.P(
                                                id="slider-text",
                                                children="Drag the slider to change the year:",
                                            ),
                                            dcc.Slider(
                                                id="years-slider",
                                                min=min(YEARS),
                                                max=max(YEARS),
                                                value=min(YEARS),
                                                marks={
                                                    str(year): {
                                                        "label": str(year),
                                                        "style": {"color": "#7fafdf"},
                                                    }
                                                    for year in YEARS
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="heatmap-container",
                                        children=[
                                            html.P(
                                                "Mean tuition revenue per student in year {0}".format(
                                                    min(YEARS)
                                                ),
                                                id="heatmap-title",
                                            ),
                                            dcc.Graph(id="choropleth"),
                                        ],
                                    ),
                                ],
                                className="row ",
                            ),
                        ],
                        className="sub_page",
                    ),
                ],
                className="page",
            )
        ]
    )
        

def generate_boxplot_median_tuition():
    fig = px.box(df_tuition, x="Year", y="TUITFTE",range_y=[0,30000],color_discrete_sequence=['indianred'])
    return fig

def generate_boxplot_median_earnings():
    fig = px.box(df_median_earn, x="Year", y="MN_EARN_WNE_P6",range_y=[0,60000],color_discrete_sequence=['indianred'])
    return fig


def demo_callbacks(app):
    @app.callback(
        Output("choropleth", "figure"), 
        [Input("years-slider", "value")],
    )
    def display_choropleth(year):
        fig = px.choropleth(
            df_dict[year],
            locations='STABBR',
            color="TUITFTE",
            color_continuous_scale='spectral_r',
            hover_name='TUITFTE',
            locationmode="USA-states",
            labels={"Mean tuition revenue per student":"Mean"},
            scope='usa'
        )
        return fig
    
    @app.callback(
        Output("heatmap-title", "children"), 
        [Input("years-slider", "value")])
    def update_map_title(year):
        return "Mean tuition revenue per student in year {0}".format(
            year
        )