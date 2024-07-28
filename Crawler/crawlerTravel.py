import os
import requests
from bs4 import BeautifulSoup
import json
from Widget.fetch_article import extract_article_content, find_data

url = 'https://www.bbc.com/travel'
save_file_name = target = 'travel'

root_dir = '../bbc_articles/travel'
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
scripts = soup.find_all('script', type='application/json')


for i, script in enumerate(scripts):
    json_content = script.string.strip()

    try:
        data = json.loads(json_content)
    except json.JSONDecodeError:
        continue

    travel_data = find_data(data, target=target)

    if travel_data:
        file_path = os.path.join(root_dir, f'first_article_{save_file_name}.json')

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(travel_data, json_file, indent=4)

            print(f"JSON data saved to {file_path}")

        extracted_data = []
        for section in travel_data.get('sections', []):
            for content in section.get('content', []):
                title = content.get('title')
                href = content.get('href')
                if title and href:
                    full_url = f'https://www.bbc.com{href}' if not href.startswith('http') else href
                    article_content = extract_article_content(full_url)
                    if article_content:
                        extracted_data.append({'title': title, 'href': href, 'article': article_content})

        extracted_file_path = os.path.join(root_dir, f'{save_file_name}_articles.json')
        with open(extracted_file_path, 'w', encoding='utf-8') as extracted_json_file:
            json.dump(extracted_data, extracted_json_file, indent=4)

        print(f"Extracted data saved to {extracted_file_path}")