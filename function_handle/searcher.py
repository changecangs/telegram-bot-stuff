import requests
from bs4 import BeautifulSoup

def google_search(query):
    search_url = "https://www.google.com/search"
    params = {
        'q': f'{query} site:codycross.info'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(search_url, params=params, headers=headers)
    response.raise_for_status()
    
    return response.text

def parse_search_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')['href']
        if link.startswith('/url?q='):
            link = link[7:].split('&')[0]
        results.append(link)
    
    return results

def get_info_from_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    info = soup.find('div', class_='alert alert-info')
    danger = soup.find('div', class_='alert alert-danger')
    
    if info and danger:
        return info.text.strip(), danger.text.strip()
    return None, None

def search(query):
    search_results_html = google_search(query)
    search_results = parse_search_results(search_results_html)
    
    for result in search_results:
        try:
            info, danger = get_info_from_page(result)
            if info and danger:
                print(f"Info: {info}")
                print(f"Danger: {danger}")
                return f"Info: {info} Danger: {danger}"
        except requests.exceptions.HTTPError as e:
            print(f"Failed to retrieve {result}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    