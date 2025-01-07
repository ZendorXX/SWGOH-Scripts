import requests
from bs4 import BeautifulSoup

# Загрузка содержимого страницы
url = 'https://swgoh.gg/p/913995163/characters/'  # замените на фактический URL
response = requests.get(url)
content = response.content

# Парсинг страницы с использованием BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Поиск всех карточек персонажей
character_cards = soup.find_all('div', class_='unit-card-grid__cell')

with open(f'output/nighting.txt', 'w') as out:
    # Извлечение информации для каждого персонажа
    for card in character_cards:
        character_name = card['data-unit-name']
        character_relic = None
        character_level = None

        relic_badge = card.find('div', class_='character-portrait__relic')
        level_badge = card.find('div', class_='character-portrait__level')
        
        if relic_badge:
            character_relic = relic_badge.find('text').text
        elif level_badge:
            character_level = level_badge.find('text').text
        
        write_data = f'{character_name}:'

        if relic_badge and int(character_relic) >= 5:
                write_data += f' {character_relic}\n'
        else:
            continue

        out.write(write_data)

        '''
        print(f'Имя персонажа: {character_name}')
        if character_relic:
            print(f'Уровень реликвий: {character_relic}')
        if character_level:
            print(f'Уровень персонажа: {character_level}')
        print('-' * 40)
        '''