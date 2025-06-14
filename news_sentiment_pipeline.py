
import requests
import json

API_KEY = "99157a526bb641d88c991802920b57b6"
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(query, from_date, to_date, language="en"):
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "language": language,
        "sortBy": "relevancy",
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles
    else:
        print(f"Error: {response.status_code}")
        return []

if __name__ == "__main__":
    articles = fetch_news("DAX", "2025-06-12", "2025-06-14")
    for article in articles[:5]:
        print(article["title"])
