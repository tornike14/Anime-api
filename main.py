from requests import request
import json
import sqlite3

url = "https://api.jikan.moe/v4/anime"

headers = {
	"Accept": "application/vnd.api+json",
	"content-type": "application/vnd.api+json"
}

response = request("GET", url, headers=headers)

# დავალება 1
print(response.headers)
print(response.status_code)

# დავალება 2
dict_response = json.loads(response.text)

with open('animes.json', 'w') as f1:
	json.dump(dict_response['data'], f1, indent=4)

# დავალება 3
with open('animes.json') as f1:
	data = json.load(f1)

anime_list = []

for p in data:
	anime = (p['title_english'], p['score'], p['year'])
	anime_list.append(anime)

# დავალება 4
conn = sqlite3.connect("anime_db.sqlite")
cursor = conn.cursor()

# ვქმნი კოლექციას სახელად "ანიმეები" რომელშიც ვქმნი ასევე ოთხ სვეტს, პირველ სვეტში დაიწერება აიდები ანიმეების და გაიზრდება რაოდენობასთან ერთად
# მეორე სვეტში არის ანიმეს დასახელება, მესამეში რეიტინგი და მეოთხეში გამოშვების წელი
cursor.execute('''CREATE TABLE IF NOT EXISTS animes
					(id INTEGER PRIMARY KEY AUTOINCREMENT,
					title VARCHAR(50),
					score FLOAT,
					release_date INTEGER);''')
# ამ ბრძანებით "animes" კოლექციაში executemany-ის საშვალებით გადავცემთ ლისტს რომელიც შედგება მრავალი თაფლ ტიპის მონაცემებისგან
# executemany-ს თუ მეორე არგუმენტად გადავცემთ ლისტს, იგი თავისით შეავსებს კოლექციასა ანუ შესაბამის მნიშვნელობებს ჩაწერს შესაბამის სვეტში
cursor.executemany('INSERT INTO animes (title, score, release_date) VALUES (?,?,?)', anime_list)
conn.commit()

conn.close()

