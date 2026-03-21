import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def search_google(keyword):
    try:
        url = "https://www.serpapi.com/search"

        params = {
            "engine": "google",
            "q": keyword,
            "hl": "pt",
            "location": "Brazil",
            "api_key": API_KEY
        }

        response = requests.get(url, params = params)

        return response.json()
    
    except(requests.exceptions.RequestException) as error:
        print(f"Erro ao realizar a requisição: {error}")
        raise error
    
    except(Exception) as error:
        print(f"Erro inesperado: {error}")
        raise error