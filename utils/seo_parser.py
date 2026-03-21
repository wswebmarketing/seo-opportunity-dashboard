import pandas as pd
from pprint import pprint
#pprint(data.keys())

def parse_organic_results(data):
    results = []
    
    for item in data.get("organic_results", []):
        results.append(
            {
                "position": item.get("position"),
                "title": item.get("title"),
                "link": item.get("link"),
                "domain": item.get("displayed_link"),
            }
        )

    return pd.DataFrame(results)

def parse_related_keywords(data):
    keywords = []

    for item in data.get("related_searches", []):
        keywords.append(
            {
                "keyword": item.get("query")
            }
        )

    return pd.DataFrame(keywords)

def parse_people_also_ask(data):
    questions = []

    for item in data.get("people_also_ask", []):
        questions.append(
            {
                "question": item.get("question")
            }
        )

    return pd.DataFrame(questions)

def build_seo_dataset(data):
    organic_df = parse_organic_results(data)
    related_df = parse_related_keywords(data)
    questions_df = parse_people_also_ask(data)

    return(
        {
            "organic": organic_df,
            "related": related_df,
            "questions": questions_df
        }
    )

def keyword_opportunity_score(organic_df, related_df, questions_df):
    keyword_volume = len(related_df)
    question_volume = len(questions_df)
    competition = organic_df["domain"].nunique()
    
    score = (
        (keyword_volume * 2) + (question_volume * 3) - competition
    )
    
    return max(score, 0)

def build_keyword_opportunities(related_df, questions_df):
    data = []
    print("\n")
    print(questions_df.head())
    print(questions_df.columns)
    print(questions_df.empty)
    for keyword in related_df.get("keyword", []):
        score = len(keyword.split()) * 2
        data.append(
            {
                "keyword": keyword,
                "type": "related",
                "score": score
            }
        )
    
    for question in questions_df.get("question", []):
        score = len(question.split()) * 3
        data.append(
            {
                "keyword": question,
                "type": "question",
                "score": score
            }
        )
    
    return data

def classify_opportunities(score):
    if(score is None):
        return "Low"
    
    try:
        score = int(score)
    except:
        return "Low"
    
    if(score >= 15):
        return "High"
    elif(score >= 8):
        return "Medium"
    else:
        return "Low"
    
#pprint(data.get("related_searches"))