import os
import json
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import ssl

# Disable SSL verification (use this method cautiously)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Try to download NLTK data
try:
    nltk.download('punkt')
    nltk.download('stopwords')
except:
    print("Automatic download failed. Please download NLTK data manually.")
    print("Follow these steps:")
    print("1. Open a Python console")
    print("2. Run the following commands:")
    print("   import nltk")
    print("   nltk.download('punkt')")
    print("   nltk.download('stopwords')")
    print("3. If the above fails, visit https://www.nltk.org/data.html for manual download instructions.")
    exit(1)

# 根目錄
root_dir = '../bbc_articles'

# 預處理函數
def preprocess(text):
    tokens = word_tokenize(text.lower()) # 將文章轉換為小寫並分詞
    tokens = re.sub(r'[^\w\s]', '', ' '.join(tokens)).split() # 移除標點符號
    stop_words = set(stopwords.words('english')) # 加載英文停用詞

    # 移除停用詞和非字母單詞
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)

# 遍歷根目錄中的所有子資料夾
for category in os.listdir(root_dir):
    category_path = os.path.join(root_dir, category)
    if os.path.isdir(category_path):
        # 遍歷子資料夾中的所有JSON檔案
        for file_name in os.listdir(category_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(category_path, file_name)

                # 讀取JSON數據
                with open(file_path, 'r', encoding='utf-8') as file:
                    articles = json.load(file)

                # 預處理所有文章
                preprocessed_articles = [preprocess(article['article']) for article in articles]

                # 計算TF-IDF
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(preprocessed_articles)

                # 獲取特徵名稱（單詞）
                feature_names = vectorizer.get_feature_names_out()

                # 將TF-IDF分數寫回JSON數據
                for i, article in enumerate(articles):
                    scores = zip(feature_names, tfidf_matrix[i].toarray()[0])
                    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
                    article['tfidf'] = {word: score for word, score in sorted_scores}  # 保存所有單詞

                # 保存更新後的JSON數據
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(articles, file, ensure_ascii=False, indent=4)