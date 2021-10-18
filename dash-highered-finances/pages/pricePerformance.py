import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import pathlib
import plotly.express as px
import plotly.graph_objects as go


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_current_prices = pd.read_csv(DATA_PATH.joinpath("df_current_prices.csv"))
df_hist_prices = pd.read_csv(DATA_PATH.joinpath("df_hist_prices.csv"))
df_avg_returns = pd.read_csv(DATA_PATH.joinpath("df_avg_returns.csv"))
df_after_tax = pd.read_csv(DATA_PATH.joinpath("df_after_tax.csv"))
df_recent_returns = pd.read_csv(DATA_PATH.joinpath("df_recent_returns.csv"))
df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph.csv"))

df_debt_gender = pd.read_csv(DATA_PATH.joinpath("df_debt_gender.csv"))
df_firstgen = pd.read_csv(DATA_PATH.joinpath("df_debt_firstgen.csv"))
df_firstgen = pd.read_csv(DATA_PATH.joinpath("df_debt_firstgen.csv"))
df_debt_median = pd.read_csv(DATA_PATH.joinpath("df_debt_median.csv"))

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    # Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Median debt by gender"], className="subtitle padded"
                                    ),
                                    #html.Table(make_dash_table(df_current_prices)),
                                    dcc.Graph(id="histogram-debt-gender",figure = generate_histogram_debt_gender()),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["Median debt of first-generation college students"],
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id="histogram-debt-firstgen",figure = generate_histogram_debt_firstgen()),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Distribution of debt over time", className="subtitle padded"),
                                    dcc.Graph(
                                        id="boxplot-median-debt",figure=boxplot_median_debt()
                                        
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        [
                                            "Average annual returns--updated monthly as of 02/28/2018"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_avg_returns),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        [
                                            "After-tax returns--updated quarterly as of 12/31/2017"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_after_tax),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Recent investment returns"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table(df_recent_returns),
                                        className="tiny-header",
                                    ),
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


def generate_histogram_debt_gender():
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df_debt_gender["MALE_DEBT_MDN"],nbinsx=30,opacity=0.5,name="Male"))
    fig.add_trace(go.Histogram(x=df_debt_gender["FEMALE_DEBT_MDN"],nbinsx=30,opacity=0.5,name="Female"))
    # The two histograms are drawn on top of another
    fig.update_layout(barmode='stack')
    
    #fig = px.box(df_tuition, x="Year", y="TUITFTE",range_y=[0,30000])
    return fig


def generate_histogram_debt_firstgen():
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df_firstgen["NOTFIRSTGEN_DEBT_MDN"],nbinsx=30,opacity=0.5,name="Non first-gen"))
    fig.add_trace(go.Histogram(x=df_firstgen["FIRSTGEN_DEBT_MDN"],nbinsx=30,opacity=0.5,name="First-gen"))
    # The two histograms are drawn on top of another
    fig.update_layout(barmode='stack')
    
    return fig



def boxplot_median_debt():
    fig = px.box(df_debt_median, x="Year",y = "DEBT_MDN",color_discrete_sequence=['indianred'])
    return fig