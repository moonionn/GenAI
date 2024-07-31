import os
import json
from collections import defaultdict
import math


def load_articles():
    articles = []
    root_dir = '../bbc_articles'
    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
            for file_name in os.listdir(category_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(category_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        category_articles = json.load(file)
                        for article in category_articles:
                            article['category'] = category  # 添加類別到文章
                        articles.extend(category_articles)
    return articles

# 計算關鍵字和文章之間的相似度
# 目的：找出與關鍵字最相關的文章
def calculate_similarity(keywords, article):
    # 為關鍵字創建一個簡單的二元向量
    # 作用：將關鍵字和文章轉換為向量，並計算它們之間的餘弦相似度，用以衡量它們之間的相似程度
    keyword_vector = defaultdict(float)
    for keyword in keywords:
        keyword_vector[keyword] = 1.0  # 簡單二元向量

    # 獲取文章的TF-IDF向量
    article_vector = article['tfidf']

    # 計算餘弦相似度
    dot_product = sum(keyword_vector[word] * article_vector.get(word, 0) for word in keyword_vector)
    keyword_magnitude = math.sqrt(sum(value ** 2 for value in keyword_vector.values()))
    article_magnitude = math.sqrt(sum(value ** 2 for value in article_vector.values()))

    # 避免除以零
    if keyword_magnitude == 0 or article_magnitude == 0:
        return 0
    return dot_product / (keyword_magnitude * article_magnitude)

# 查找與關鍵字最匹配的文章
def find_matching_articles(keywords, articles, top_n=5):
    # 計算每篇文章與關鍵字的相似度
    similarities = [(article, calculate_similarity(keywords, article)) for article in articles]
    # 按相似度降序排序
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_n]


def main():
    articles = load_articles()

    while True:
        # 輸入3-5個關鍵字
        keywords = input("輸入3-5個英文關鍵字（用空格分隔），或輸入'q'退出：").lower().split()

        if keywords[0] == 'q':
            break

        # 檢查關鍵字數量是否符合要求
        if len(keywords) < 3 or len(keywords) > 5:
            print("請輸入3-5個關鍵字。")
            continue

        # 查找最匹配的文章(BBC文章)
        matching_articles = find_matching_articles(keywords, articles)

        print("\n最匹配的5篇文章：")
        for i, (article, similarity) in enumerate(matching_articles, 1):
            print(f"{i}. 標題: {article['title']}")
            print(f"   類別: {article['category']}")
            print(f"   相似度: {similarity:.4f}")
            print()


if __name__ == "__main__":
    main()