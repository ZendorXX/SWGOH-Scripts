import requests
from bs4 import BeautifulSoup
from get_name import get_player_name

def get_player_characters(allycode):
    url = f'https://swgoh.gg/p/{allycode}/characters/'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    character_cards = soup.find_all('div', class_='unit-card-grid__cell')
    characters = []

    for card in character_cards:
        character_name = card['data-unit-name']
        character_relic = 0
        character_level = 1
        character_stars = 0  # По умолчанию звёзд 0

        # Парсим уровень и релик
        relic_badge = card.find('div', class_='character-portrait__relic')
        level_badge = card.find('div', class_='character-portrait__level')

        if relic_badge:
            character_relic = int(relic_badge.find('text').text)
            character_level = 85
        elif level_badge:
            character_level = int(level_badge.find('text').text)
            character_relic = 0

        # Парсим уровень звёзд
        stars_container = card.find('div', class_='rarity-range')
        if stars_container:
            stars = stars_container.find_all('div', class_='rarity-range__star')
            character_stars = len(stars)  # Количество звёзд равно количеству элементов с классом rarity-range__star

        characters.append({
            'name': character_name,
            'level': character_level,
            'relic': character_relic,
            'stars': character_stars  # Добавлено поле "stars"
        })

    return characters

def get_player_ships(allycode):
    url = f'https://swgoh.gg/p/{allycode}/ships/'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    ship_cards = soup.find_all('div', class_='unit-card-grid__cell')
    ships = []

    for card in ship_cards:
        ship_name = card['data-unit-name']
        ship_level = 1  # По умолчанию уровень 1
        ship_stars = 0  # По умолчанию звёзд 0

        # Парсим уровень корабля
        level_badge = card.find('div', class_='ship-portrait__level')
        if level_badge:
            level_text = level_badge.find('text').text
            if level_text.isdigit():
                ship_level = int(level_text)

        # Парсим уровень звёзд корабля
        stars_container = card.find('div', class_='rarity-range')
        if stars_container:
            stars = stars_container.find_all('div', class_='rarity-range__star')
            ship_stars = len(stars)  # Количество звёзд равно количеству элементов с классом rarity-range__star

        ships.append({
            'name': ship_name,
            'level': ship_level,
            'stars': ship_stars
        })

    return ships

def main():
    with open('db/allycodes.txt', 'r') as file:
        allycodes = file.read().splitlines()

    for allycode in allycodes:
        try:
            name = get_player_name(allycode)
            characters = get_player_characters(allycode)
            ships = get_player_ships(allycode)

            filename = f"guild/{name}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"Игрок: {name}\n\n")
                
                file.write("Персонажи:\n")
                file.write("Имя персонажа\tУровень\tРелик\tЗвёзды\n")
                file.write("-" * 40 + "\n")
                for character in characters:
                    file.write(f"{character['name']}\t{character['level']}\t{character['relic']}\t{character['stars']}\n")
                
                file.write("\nКорабли:\n")
                file.write("Имя корабля\tУровень\tЗвёзды\n")
                file.write("-" * 30 + "\n")
                for ship in ships:
                    file.write(f"{ship['name']}\t{ship['level']}\t{ship['stars']}\n")

            print(f"Данные для игрока {name} сохранены в файл: {filename}")
        except Exception as e:
            print(f"Ошибка при обработке allycode {allycode}: {e}")

if __name__ == '__main__':
    main()