import json

# Load the JSON data from the file
with open('bbc_articles/sport/sport_articles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Update the keys in each article
for article in data:
    article['title'] = article.pop('headline')
    article['href'] = article.pop('url')
    article['article'] = article.pop('content')

# Save the updated JSON data back to the file
with open('bbc_articles/sport/sport_articles.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)