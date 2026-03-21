import dash
from dash import Dash, html, callback, Output, Input
import dash_bootstrap_components as dbc
from components.header import header

LIGHT_THEME = dbc.themes.FLATLY
DARK_THEME = dbc.themes.CYBORG

app = Dash(
    __name__,
    use_pages = True,
    suppress_callback_exceptions = True
)

app.layout = html.Div(
    [
        header(),
        html.Div(
            dash.page_container,
            id = "page-container"
        )
    ]
)

@callback(
    Output("theme-link", "href"),
    Output("theme-icon", "className"),
    Output("navbar", "color"),
    Output("navbar", "dark"),
    Output("logo", "src"),
    Output("page-container", "className"),
    #Output("header", "style"),
    Input("theme-switch", "value")
)

def update_theme(toggle):
    if(toggle):
        return(
            DARK_THEME,
            "fa-solid fa-moon text-white me-2",
            "dark",
            True,
            "assets/logo-ws-web-marketing-branco.png",
            "text-white"
        )
    return(
        LIGHT_THEME,
        "fa-solid fa-sun text-warning me-2",
        "info",
        False,
        "assets/logo-ws-web-marketing-preto.png",
        "text-dark"
    )

if(__name__ == "__main__"):
    app.run(debug = True)
    
'''import requests
from pprint import pprint

keyword = "digital marketing"

url = "https://serpapi.com/search"

params = {
    "engine": "google",
    "q": keyword,
    "hl": "pt",
    "location": "Brazil",
    "api_key": API_KEY
}

response = requests.get(url, params = params)
data = response.json()
pprint(data.keys())
print("\n")
pprint(data["organic_results"][0])
print("\n")
pprint(data["organic_results"][0]["title"])

for result in data.get("organic_results", []):
    pprint(result.get("title"))'''