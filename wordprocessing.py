import requests
from bs4 import BeautifulSoup
import re
import csv

# Specify the correct path to save the CSV file
file_path = r"C:\Users\siddu\Semester 5\Anna University word processing\Book1.csv"

for count in range(4000):
    # URL of the Wikihow page to scrape
    url = 'https://www.wikihow.com/Special:Randomizer'
    
    # Send an HTTP request to the URL and receive the HTML content
    response = requests.get(url)
    html_content = response.content
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    article_title = soup.find('title').text.strip()
    print(article_title + ":" + str(count))
    
    # Extract the subheadings and paragraphs using the appropriate HTML tags
    subheadings = []
    paragraphs = []
    steps = soup.find_all('div', {'class': 'step'})
    
    for step in steps:
        subheading_element = step.find('b')
        if subheading_element is not None:
            subheading_text = subheading_element.text.strip().replace('\n', '')
            subheading_text = subheading_text.encode('ascii', errors='ignore').decode()
            subheading_text = re.sub(r'\s+', ' ', subheading_text)
            subheadings.append(subheading_text)
            subheading_element.extract()
        
        for span_tag in step.find_all('span'):
            span_tag.extract()
        
        paragraph_text = step.text.strip().replace('\n', '').replace('\t', '')
        paragraph_text = paragraph_text.encode('ascii', errors='ignore').decode()
        paragraph_text = re.sub(r'\s+', ' ', paragraph_text)
        paragraphs.append(paragraph_text)
    
    # Check if there are subheadings to write to the CSV
    if len(subheadings):
        with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for i in range(len(subheadings)):
                writer.writerow([article_title, subheadings[i], paragraphs[i]])
