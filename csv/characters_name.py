import requests
from bs4 import BeautifulSoup
import csv

# URL страницы персонажей
url = "https://swgoh.gg/characters/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Найти все карточки персонажей
character_cards = soup.find_all("div", class_="unit-card-grid__cell")

# Список для хранения данных
characters = []

# Обработка каждой карточки
for card in character_cards:
    # Имя персонажа
    name = card.get("data-unit-name", "Unknown").strip()
    
    # Тип персонажа (всегда "character")
    character_type = "character"
    
    # Добавление информации в список
    characters.append({"name": name, "type": character_type})

# Вывод в CSV файл
output_file = 'output/characters.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Заголовки колонок
    writer.writerow(["Name", "Type"])
    # Запись данных
    for char in characters:
        writer.writerow([char["name"], char["type"]])

print(f"Данные сохранены в файл: {output_file}")