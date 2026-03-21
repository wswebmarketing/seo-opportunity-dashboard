import dash
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
'''
LIBS UTILIZADAS APENAS PARA DESENVOLVIMENTO
from tabulate import tabulate
from pprint import pprint'''
from services.seo_analysis import get_seo_data
from utils.seo_parser import build_keyword_opportunities, classify_opportunities

dash.register_page(
    __name__,
    path = "/keyword-opportunities",
    title = "Keyword Opportunities"
)

layout = html.Div(
    [
        html.H1(
            "Estamos na página de oportunidades de palavras-chave",
            className = "text-center fw-bold"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id = "keyword-input-up",
                                placeholder = "Enter a keyword...",
                                type = "text"
                            ),
                            dbc.Button(
                                "Analyze",
                                id = "button-op",
                                color = "success"
                            )
                        ]
                    ),
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                ),
                dbc.Col(
                    dbc.Table(
                        id = "table-opportunities",
                        className = "text-center",
                        bordered = True,
                        striped = True,
                        hover = True
                    ),
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                )
            ],
            className = "m-5",
        )
    ],
    className = "container p-5"
)

@callback(
    Output("table-opportunities", "children"),
    Input("button-op", "n_clicks"),
    State("keyword-input-up", "value")
)

def update_table(n_clicks, keyword):
    if(not keyword):
        return []
    seo_data = get_seo_data(keyword)
    related_df = seo_data["related"]
    questions_df = seo_data["questions"]
    data = build_keyword_opportunities(related_df, questions_df)
    df = pd.DataFrame(data)
    if(not df.empty and "score" in df.columns):
        df["score"] = pd.to_numeric(df["score"], errors = "coerce")
        df["classification"] = df["score"].apply(classify_opportunities)
    else:
        df["classification"] = []
    #Criação da tabela HTML a partir do DataFrame criado
    header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Keyword"),
                    html.Th("Type"),
                    html.Th("Score"),
                    html.Th("Classification")
                ]
            ),
            className = "fw-bold"
        )
    ]
    rows = []
    for _, row in df.iterrows():
        rows.append(
            html.Tr(
                [
                    html.Td(row["keyword"]),
                    html.Td(row["type"]),
                    html.Td(row["score"]),
                    html.Td(row["classification"])
                ]
            )
        )
    body = [
        html.Tbody(rows)
    ]
    return header + body