import sqlite3 as sql
from bs4 import BeautifulSoup as bs
import requests
from time import sleep

url = "https://books.toscrape.com/"

response = requests.get(url)

if response.status_code == 200:
    response.encoding = 'utf-8'
    html = response.text
    print("Fetched html successfully")
else:
    print(f"html fetch failed: Error {response.status_code}")
    exit()

soup = bs(html,"html.parser")
book_data = []

books = soup.find_all("article",class_="product_pod")

for book in books:
    title = book.h3.a['title']
    price = book.find("p",class_="price_color").text.strip()
    book_data.append((title,price))

print(f"Books found {len(book_data)}")

sleep(2)

print("Adding to Database")

conn = sql.connect("../../DE/Books.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books_data(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Title TEXT,
Price TEXT);
""")

cursor.executemany("INSERT INTO books_data (Title,Price) VALUES (?,?)",book_data)

cursor.execute("SELECT * FROM books_data")

for row in cursor.fetchall():
    print(row)


conn.commit()
conn.close()

print("Added to database")