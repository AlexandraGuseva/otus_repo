import csv
import json

books = []
with open('books.csv', mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_lower = {k.lower(): v for k, v in row.items()}
        book = {
            "title": row_lower.get("title", ""),
            "author": row_lower.get("author", ""),
            "pages": int(row_lower.get("pages", 0)),
            "genre": row_lower.get("genre", ""),
        }
        books.append(book)
with open("users.json", mode="r", encoding="utf-8") as f:
    users_data = json.load(f)

users = []
for item in users_data:
    user = {
        "name": item.get("name", ""),
        "gender": item.get("gender", ""),
        "age": int(item.get("age", 0)) if item.get("age") is not None else 0,
        "address": item.get("address", ""),
        "books": [],
    }
    users.append(user)

user_index = 0
num_users = len(users)

for book in books:
    users[user_index]["books"].append(book)
    user_index = (user_index + 1) % num_users
    with open("result.json", mode="w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

print("Домашняя работа выполнена.")