from services.serp_api import search_google
from utils.seo_parser import build_seo_dataset

def get_seo_data(keyword):
    data = search_google(keyword)
    parsed = build_seo_dataset(data)
    return parsed