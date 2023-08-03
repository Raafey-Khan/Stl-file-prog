import requests
from bs4 import BeautifulSoup

def get_news_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h2', class_='headline')
        return [headline.text.strip() for headline in headlines]
    else:
        print(f"Error: Could not fetch data from {url}")
        return []

if __name__ == "__main__":
    news_url = "https://www.example-news-website.com"
    headlines = get_news_headlines(news_url)

    if headlines:
        print("Latest News Headlines:")
        for idx, headline in enumerate(headlines, 1):
            print(f"{idx}. {headline}")
    else:
        print("No headlines found.")
