import requests
from bs4 import BeautifulSoup
from get_name import get_player_name

def get_player_characters(allycode):
    url = f'https://swgoh.gg/p/{allycode}/characters/'
    # Загрузка содержимого страницы
    response = requests.get(url)
    content = response.content

    # Парсинг страницы с использованием BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Поиск всех карточек персонажей
    character_cards = soup.find_all('div', class_='unit-card-grid__cell')

    characters = []

    # Извлечение информации для каждого персонажа
    for card in character_cards:
        character_name = card['data-unit-name']
        character_relic = 0  # По умолчанию релик 0
        character_level = 1  # По умолчанию уровень 1

        relic_badge = card.find('div', class_='character-portrait__relic')
        level_badge = card.find('div', class_='character-portrait__level')

        if relic_badge:
            character_relic = int(relic_badge.find('text').text)
            character_level = 85  # Если есть релик, уровень автоматически 85
        elif level_badge:
            character_level = int(level_badge.find('text').text)
            character_relic = 0  # Если есть только уровень, релик автоматически 0

        # Добавляем информацию о персонаже в список
        characters.append({
            'name': character_name,
            'level': character_level,
            'relic': character_relic
        })

    return characters

def main():
    # Чтение allycodes из файла
    with open('db/allycodes.txt', 'r') as file:
        allycodes = file.read().splitlines()

    # Обработка каждого allycode
    for allycode in allycodes:
        try:
            # Получаем имя игрока
            name = get_player_name(allycode)

            # Получаем список персонажей
            characters = get_player_characters(allycode)

            # Сохраняем данные в файл с именем игрока
            filename = f"guild/{name}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                # Записываем имя игрока в файл
                file.write(f"Игрок: {name}\n\n")
                # Записываем информацию о персонажах
                file.write("Имя персонажа\tУровень\tРелик\n")
                file.write("-" * 30 + "\n")
                for character in characters:
                    file.write(f"{character['name']}\t{character['level']}\t{character['relic']}\n")

            print(f"Данные для игрока {name} сохранены в файл: {filename}")
        except Exception as e:
            print(f"Ошибка при обработке allycode {allycode}: {e}")

if __name__ == '__main__':
    main()