import requests
from bs4 import BeautifulSoup

def fetch_puzzle_data(name, group_number, puzzle_number):
    url = f"https://codycross-answer.com/{name}/group-{group_number}-puzzle-{puzzle_number}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    puzzle_data = {}
    
    puzzle_entries = soup.find_all('div', class_='PuzzleQnA')
    for entry in puzzle_entries:
        question = entry.find('h2', class_='PuzzleQuestion').get_text()
        answer = entry.find('p', class_='PuzzleAnswer').get_text()
        puzzle_data[question] = answer
    
    return puzzle_data

def search_answer(puzzle_data, puzzle_question):
    return puzzle_data.get(puzzle_question, "Question not found")
