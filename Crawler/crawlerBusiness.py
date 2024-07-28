import requests
from bs4 import BeautifulSoup
import json
import os
from Widget.fetch_article import extract_article_content, find_data

# 欲爬取網址
url = 'https://www.bbc.com/business'
save_file_name = target = 'business'

root_dir = '../bbc_articles/business'
if not os.path.exists(root_dir):    # 若目錄不存在，則建立目錄
    os.makedirs(root_dir)

# 發送 HTTP 請求，取得網頁內容
response = requests.get(url)

# 解析 HTML 內容
soup = BeautifulSoup(response.content, 'html.parser')

# 查找包含 JSON 資料的 script 標籤
scripts = soup.find_all('script', type='application/json')

# 提取並儲存 JSON 內容
for i, script in enumerate(scripts):
    # 獲取 script 標籤中的 JSON 內容
    json_content = script.string.strip()

    # 將 JSON 內容轉換為 Python 字典
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError:
        continue

    # 遍歷字典，查找包含 "@\"business\"," 的部分並儲存其內容
    business_data = find_data(data, target=target)

    # 如果找到符合條件的數據，則儲存
    if business_data:
        # 定義 JSON 檔案的儲存路徑
        file_path = os.path.join(root_dir, f'first_article_{save_file_name}.json')

        with open(file_path, 'w', encoding='utf-8') as json_file:
            # 將 JSON 內容寫入檔案
            json.dump(business_data, json_file, indent=4)

            print(f"JSON data saved to {file_path}")

        # 提取每個 content 中的 title 和 href 並儲存成新的 JSON
        extracted_data = []
        for section in business_data.get('sections', []):
            for content in section.get('content', []):
                title = content.get('title')
                href = content.get('href')
                if title and href:
                    full_url = f'https://www.bbc.com{href}'
                    # 提取文章內容
                    article_content = extract_article_content(full_url)
                    if article_content:
                        extracted_data.append({'title': title, 'href': href, 'article': article_content})

        # 定義新的 JSON 檔案的儲存路徑
        extracted_file_path = os.path.join(root_dir, f'{save_file_name}_articles.json')
        with open(extracted_file_path, 'w', encoding='utf-8') as extracted_json_file:
            json.dump(extracted_data, extracted_json_file, indent=4)

        print(f"Extracted data saved to {extracted_file_path}")