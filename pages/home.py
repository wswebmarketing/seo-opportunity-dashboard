import dash
from dash import html, dcc, callback, Output, Input, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
from services.seo_analysis import get_seo_data
#LIBS UTILIZADAS APENAS PARA DESENVOLVIMENTO
'''from pprint import pprint
from tabulate import tabulate'''
from utils.seo_parser import keyword_opportunity_score

dash.register_page(
    __name__,
    path = "/",
    title = "Home"
)

layout = html.Div(
    [
        html.H1(
            "SEO Opportunity Dashboard",
            className = "text-center fw-bold"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Related Keywords",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    html.H3(
                                        id = "kpi_related_keywords",
                                        className = "card-text text-center fw-bold"
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 12, md = 3, lg = 3, xl = 3
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "People Also Ask",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    html.H3(
                                        id = "kpi_people_also_ask",
                                        className = "card-text text-center fw-bold"
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 12, md = 3, lg = 3, xl = 3
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Competitor Domains",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    html.H3(
                                        id = "kpi_competitor_domains",
                                        className = "card-text text-center fw-bold"
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 12, md = 3, lg = 3, xl = 3
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Organic Results",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    html.H3(
                                        id = "kpi_organic_results",
                                        className = "card-text text-center fw-bold"
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 12, md = 3, lg = 3, xl = 3
                )
            ],
            className = "m-5"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.InputGroup(
                                        [
                                            dbc.Input(
                                                id = "keyword-input",
                                                placeholder = "Enter a keyword...",
                                                type = "text"
                                            ),
                                            dbc.Button(
                                                id = "search-button",
                                                color = "success",
                                                className = "fa-solid fa-search"
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 6, md = 3, lg = 3, xl = 3
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "SERP Competitor Distribution",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    dcc.Graph(
                                        id = "graph_competitor_distribution",
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 6, md = 5, lg = 5, xl = 5
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Keyword Opportunities Score",
                                        className = "card-title text-center fw-bold"
                                    ),
                                    html.H3(
                                        id = "kpi_opportunity_score",
                                        className = "card-text text-center fw-bold"
                                    )
                                ]
                            )
                        )
                    ],
                    xs = 12, sm = 12, md = 4, lg = 4, xl = 4
                )
            ],
            className = "m-5"
        )
    ],
    className = "container p-5"
)

@callback(
    Output("kpi_related_keywords", "children"),
    Output("kpi_people_also_ask", "children"),
    Output("kpi_competitor_domains", "children"),
    Output("kpi_organic_results", "children"),
    Output("graph_competitor_distribution", "figure"),
    Output("kpi_opportunity_score", "children"),
    Input("search-button", "n_clicks"),
    Input("keyword-input", "value")
)

def update_dashboard(n_clicks, keyword):
    if(not ctx.triggered):
        return "0", "0", "0", "0", px.bar(), "0"

    if(not keyword):
        return "0", "0", "0", "0", px.bar(), "0"
    
    seo_data = get_seo_data(keyword)
    print("\n")

    organic_df = seo_data["organic"]
    related_df = seo_data["related"]
    questions_df = seo_data["questions"]

    total_keywords = len(related_df)
    total_questions = len(questions_df)
    total_competitors = organic_df["domain"].nunique()
    total_results = len(organic_df)

    domain_distribution = (
        organic_df["domain"]
        .value_counts()
        .reset_index()
    )
    domain_distribution.columns = ["domain", "count"]

    fig = px.bar(
        domain_distribution,
        x = "domain",
        y = "count",
        text = "count",
        title = "Top Domains in SERP"
    )
    fig.update_traces(textposition = "outside")

    score = keyword_opportunity_score(organic_df, related_df, questions_df)

    return(
        total_keywords,
        total_questions,
        total_competitors,
        total_results,
        fig,
        score
    )