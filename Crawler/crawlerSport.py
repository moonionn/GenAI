import os
import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.bbc.com/sport'
save_file_name = 'sport_articles'

root_dir = '../bbc_articles/sport'
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

scripts = soup.find_all('script')

def extract_article_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve article from {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find('article')
    if not article:
        print(f"No article found in {url}")
        return None

    paragraphs = article.find_all('p')
    content = "\n".join(p.get_text() for p in paragraphs)
    return content

def find_sport_article_data(data):
    sport_article_data = []
    if isinstance(data, dict):
        if 'url' in data and 'headline' in data:
            url = data['url']
            if isinstance(url, str) and url.startswith('/sport/') and ('articles' or 'article') in url:
                full_url = f'https://www.bbc.com{url}'
                article_content = extract_article_content(full_url)
                sport_article_data.append({
                    'headline': data['headline'],
                    'url': url,
                    'content': article_content
                })
        for value in data.values():
            sport_article_data.extend(find_sport_article_data(value))
    elif isinstance(data, list):
        for item in data:
            sport_article_data.extend(find_sport_article_data(item))
    return sport_article_data

for script in scripts:
    if 'window.__INITIAL_DATA__=' in script.text:
        json_str = script.text.split('window.__INITIAL_DATA__=')[1].split('";')[0]
        json_str = json_str.strip().strip('"').replace('\\"', '"')

        try:
            full_data = json.loads(json_str)
            sport_article_data = find_sport_article_data(full_data)

            if sport_article_data:
                formatted_file_path = os.path.join(root_dir, f"{save_file_name}.json")
                with open(formatted_file_path, 'w', encoding='utf-8') as f:
                    json.dump(sport_article_data, f, ensure_ascii=False, indent=4)
                print(f"符合條件的數據已保存到 {formatted_file_path}")
                print(f"找到 {len(sport_article_data)} 個符合條件的文章")
            else:
                print("未找到符合條件的文章數據")

        except json.JSONDecodeError as e:
            print(f"JSON 解碼錯誤: {e}")
            print("原始 JSON 字符串:", json_str[:1000])
        break
else:
    print("未找到包含初始數據的 script 標籤。")