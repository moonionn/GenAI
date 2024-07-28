## BBC News文章匹配與分類系統

專案介紹
---
自動抓取BBC News網站的文章，並根據使用者輸入的關鍵字，找出最匹配的文章。同時，該程式能夠根據給定文章的內容判斷其所屬類別。

項目架構
---
```
GenAI
├── .venv
├── bbc_articles  # 分門別類儲存各文章
│   ├── business
│   ├── culture
│   ├── earth
│   ├── innovation
│   ├── sport
│   └── travel
├── Crawler   # 爬蟲
│   ├── crawlerBusiness.py
│   ├── crawlerCulture.py
│   ├── crawlerEarth.py
│   ├── crawlerInnovation.py
│   ├── crawlerSport.py
│   └── crawlerTravel.py
├── ML  # Machine Learning
├── Widget  # 通用function
│   ├── fetch_article.py
└── └── main.py
```
## 方法
	1.	文章抓取與存儲
	•	從BBC News網站自動抓取不同類別的文章（如Sport, business等）。
	•	將抓取的文章存儲在本地目錄(bbc_articles)，並依照每篇文章的所屬類別。
	2.	詞彙處理與TF-IDF計算
	•	從本地目錄中讀取所有文章。
	•	為每篇文章的所有詞彙計算TF-IDF分數。
	3.	關鍵字匹配
	•	接受使用者輸入的3~5個英文關鍵字。
	•	根據關鍵字計算與每篇文章的相似度，找出最匹配的前5篇文章，並標示其類別。
	4.	文章分類
	•	接受使用者提供的一篇文章（純文字）。
	•	計算該文章各詞彙的TF-IDF分數，並與所有BBC News文章的TF-IDF向量做相似度比較。
	•	輸出此文章的所屬類別。


