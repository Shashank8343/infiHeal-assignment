import requests
from bs4 import BeautifulSoup

def fetch_articles(query: str):
    search_url = f"https://api.bing.microsoft.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    for item in soup.find_all('div', class_='article-summary'):
        title = item.find('h2').text
        link = item.find('a')['href']
        summary = item.find('p').text
        articles.append({'title': title, 'link': link, 'summary': summary})
    
    return articles
