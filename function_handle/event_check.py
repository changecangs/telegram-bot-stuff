import requests
from bs4 import BeautifulSoup

def get_event_data(event_name, event_level):
    # Build the URL with the provided queries
    url = f"https://codycross.info/en/events/{event_name}/{event_level}/"
    
    # Define headers to make the request appear like it's coming from a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    # Make a GET request to fetch the HTML content with the custom headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 403:
        print(f"Error 403: Access to {url} is forbidden. Try updating the headers.")
        return []
    elif response.status_code != 200:
        print(f"Error: Unable to fetch data from {url}")
        return []
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the relevant part of the page where questions and answers are listed
    words_div = soup.find('div', class_='words')
    
    if not words_div:
        print("Error: Couldn't find the 'words' section on the page.")
        return []
    
    # Extract each <p> element and parse its contents
    qa_pairs = []
    for p_tag in words_div.find_all('p'):
        # Extract the question (text before the <br> tag)
        question = p_tag.text.split('\n')[0].strip()
        
        # Extract the answer from the <a> tag's onclick attribute
        a_tag = p_tag.find('a')
        if a_tag:
            onclick_text = a_tag.get('onclick', '')
            answer = onclick_text.split("'<strong>")[1].split("</strong>'")[0]
            qa_pairs.append(f"{question} : {answer}")
    
    return qa_pairs
