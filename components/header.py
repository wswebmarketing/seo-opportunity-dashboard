import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, callback, Output, Input, dcc

def header():
    nav_links = [
        dbc.NavLink(
            page["title"],
            href = page["path"],
            active = "exact",
            className = "mx-2"
        )
        for page in dash.page_registry.values()
    ]

    return html.Div(
        [
            dcc.Location(id = "url"),

            # Bootstrap Theme Dinâmico
            html.Link(
                id = "theme-link",
                rel = "stylesheet"   
            ),

            # Font Awesome
            html.Link(
                rel = "stylesheet",
                href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
            ),

            html.Link(
                rel = "icon",
                type = "image/x-icon",
                href = "assets/logo-ws-web-marketing-preto-icon.png"
            ),

            html.Header(
                [
                    dbc.Navbar(
                        id = "navbar",
                        color = "info",
                        expand = "md",
                        dark = False,
                        children = [
                            dbc.Container(
                                children = [
                                    dbc.NavbarBrand(
                                        children = [
                                            html.Img(
                                                id = "logo",
                                                src = "assets/logo-ws-web-marketing-preto.png"
                                            )
                                        ]
                                    ),
                                    dbc.NavbarToggler(
                                        id = "navbar-toggler",
                                        n_clicks = 0
                                    ),
                                    dbc.Collapse(
                                        dbc.Nav(
                                            children = [
                                                *nav_links,
                                                dbc.Nav(
                                                    children = [
                                                        html.I(
                                                            className = "fa-solid fa-sun m-1",
                                                            id = "theme-icon"
                                                        ),
                                                        dbc.Switch(
                                                            id = "theme-switch",
                                                            value = False
                                                        )
                                                    ],
                                                    className = "d-flex align-items-center"
                                                )
                                            ],
                                            className = "ms-auto",
                                            navbar = True
                                        ),
                                        id = "navbar-collapse",
                                        is_open = False,
                                        navbar = True   
                                    )
                                ]
                            )
                        ]
                    )
                ],
                id = "header",
                #style = {
                #    "backgroundColor": "#a9fe01"
                #}
            )
        ]
    )

@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    Input("navbar-collapse", "is_open")
)

def toggle_navbar(n, is_open):
    if(n):
        return(not is_open)
    return is_open