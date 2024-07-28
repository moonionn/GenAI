import requests
from bs4 import BeautifulSoup
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

# 遍歷字典，查找包含 ex."@\"business\"," 的部分並儲存其內容
def find_data(data, target):
    if isinstance(data, dict):
        for key, value in data.items():
            if f"@\"{target}\"," in key:
                return value
            result = find_data(value, target)  # 傳遞 target 參數
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_data(item, target)  # 傳遞 target 參數
            if result:
                return result
    return None