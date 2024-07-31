import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 加載已收集的BBC文章
def load_bbc_articles():
    articles = []
    categories = []
    # 獲取bbc_articles目錄的路徑
    root_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bbc_articles')
    # 遍歷bbc_articles目錄下的所有類別資料夾
    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
            # 遍歷每個類別目錄下的所有JSON文件
            for file_name in os.listdir(category_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(category_path, file_name)
                    # 讀取JSON文件並提取文章內容
                    with open(file_path, 'r', encoding='utf-8') as file:
                        category_articles = json.load(file)
                        for article in category_articles:
                            articles.append(article['article'])
                            categories.append(category)
    return articles, categories

# 計算TF-IDF矩陣
# 目的：將新文章與BBC文章進行比較，找出最相似的BBC文章
def calculate_tfidf(new_article, bbc_articles):
    vectorizer = TfidfVectorizer()
    # 將新文章添加到BBC文章列表中，並計算TF-IDF
    tfidf_matrix = vectorizer.fit_transform(bbc_articles + [new_article])
    return tfidf_matrix

# 對新文章分類
def classify_article(new_article, bbc_articles, categories):
    # 計算TF-IDF矩陣
    tfidf_matrix = calculate_tfidf(new_article, bbc_articles)
    new_article_vector = tfidf_matrix[-1]   # 新文章的TF-IDF向量
    bbc_vectors = tfidf_matrix[:-1]         # 提取BBC文章的TF-IDF向量

    similarities = cosine_similarity(new_article_vector, bbc_vectors)
    most_similar_index = similarities.argmax()  # 找最相似的BBC文章的索引

    return categories[most_similar_index]


def main():
    print("正在加載BBC文章...")
    # 加載BBC文章資料集
    bbc_articles, categories = load_bbc_articles()
    print(f"BBC文章加載完成。共加載 {len(bbc_articles)} 篇文章。")

    while True:
        print("\n請輸入一篇文章（純文字），或輸入'q'退出：")
        user_input = input()

        if user_input.lower() == 'q':
            break

        # 對輸入的文章進行分類
        predicted_category = classify_article(user_input, bbc_articles, categories)
        print(f"\n這篇文章最可能屬於的類別是：{predicted_category}")


if __name__ == "__main__":
    main()