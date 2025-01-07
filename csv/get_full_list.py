import requests
from bs4 import BeautifulSoup
import csv

# URL страницы
url = 'https://swgoh.gg/p/827134165/characters/'

# Заголовки для запроса (может потребоваться для имитации браузера)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Получение HTML-кода страницы
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Нахождение всех блоков с персонажами
characters = soup.find_all('div', class_='unit-card__primary')

# Открытие CSV файла для записи
with open('characters.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Заголовки столбцов
    writer.writerow(['Имя персонажа', 'Количество звезд', 'Уровень персонажа', 'Уровень снаряжения', 'Уровень реликвий'])

    # Обработка каждого персонажа
    for character in characters:
        # Имя персонажа
        name = character.find('div', class_='unit-card__name').text.strip()

        # Количество звезд
        stars = len(character.find('div', class_='rarity-range').find_all('div', class_='rarity-range__star'))

        # Уровень персонажа
        relic_level = character.find('div', class_='character-portrait__relic')
        if relic_level:
            relic_text = relic_level.find('text').text.strip()
            if relic_text.isdigit():
                character_level = 85
            else:
                character_level = 1  # По умолчанию, если нет реликвии
        else:
            character_level = 1

        # Уровень снаряжения
        equipment_level = character.find('div', class_='progress-bar')['style'].split(':')[1].replace('%', '').strip()

        # Уровень реликвий
        if relic_level:
            relic_text = relic_level.find('text').text.strip()
            if relic_text.isdigit():
                relic_level_value = int(relic_text)
            else:
                relic_level_value = 0
        else:
            relic_level_value = 0

        # Запись данных в CSV
        writer.writerow([name, character_level, stars, 13, relic_level_value])

print("Данные успешно записаны в characters.csv")