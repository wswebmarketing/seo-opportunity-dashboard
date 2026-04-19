import dash
from dash import html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from services.seo_analysis import get_seo_data
from utils.seo_parser import keyword_opportunity_score

dash.register_page(
    __name__,
    path = "/serp-analysis",
    title = "SERP Analysis"
)

layout = html.Div(
    [
        html.H1(
            "Estamos na página de análise de palavras-chave",
            className = "text-center fw-bold"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id = "keyword-input",
                                placeholder = "Enter a keyword...",
                                type = "text"
                            ),
                            dbc.Button(
                                "Search",
                                id = "search-button",
                                color = "success"
                            )
                        ]
                    ),
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                ),
                dbc.Col(
                    html.H4(
                        id = "score-output"
                    ),
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                )
            ],
            className = "m-5"
        ),
        html.Div(
            [
                html.H4(
                    "Organic Results",
                    className = "text-center fw-bold"
                ),
                dash_table.DataTable(
                    id = "organic-results-table",
                    page_size = 10,
                    style_table = {
                        "overflowX": "auto",
                        "width": "100%",
                        "fontFamily": "inherit"
                    },
                    style_header = {
                        "fontWeight": "bold",
                        "textAlign": "center"
                    }
                )
            ],
            className = "m-5"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            "Related Keywords",
                            className = "text-center fw-bold"
                        ),
                        dash_table.DataTable(
                            id = "related-keywords-table",
                            page_size = 10
                        )
                    ],
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                ),
                dbc.Col(
                    [
                        html.H4(
                            "People Also Ask",
                            className = "text-center fw-bold"
                        ),
                        dash_table.DataTable(
                            id = "questions-table",
                            page_size = 10
                        )
                    ],
                    xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                )
            ]
        )
    ],
    className = "container p-5"
)

@callback(
    Output("organic-results-table", "data"),
    Output("organic-results-table", "columns"),
    Output("related-keywords-table", "data"),
    Output("related-keywords-table", "columns"),
    Output("questions-table", "data"),
    Output("questions-table", "columns"),
    Output("score-output", "children"),
    Input("search-button", "n_clicks"),
    Input("keyword-input", "value")
)

def update_serp(n_clicks, keyword):
    if(not keyword):
        return [], [], [], [], [], [], "Enter a keyword"
    
    try:
        data = get_seo_data(keyword)
        print(data)

        organic_df = data["organic"]
        related_df = data["related"]
        questions_df = data["questions"]

        score = keyword_opportunity_score(organic_df, related_df, questions_df)
        print(score)

        return(
            organic_df.to_dict("records"),
            [{"name": col, "id": col} for col in organic_df.columns],
            related_df.to_dict("records"),
            [{"name": col, "id": col} for col in related_df.columns],
            questions_df.to_dict("records"),
            [{"name": col, "id": col} for col in questions_df.columns],
            f"Keyword Opportunity Score: {score:.2f}"
        )
    
    except Exception as error:
        return [], [], [], [], [], [], f"Error: {str(error)}"