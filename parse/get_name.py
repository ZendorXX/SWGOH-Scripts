import requests
from bs4 import BeautifulSoup

def get_player_name(allycode):
    # Формируем URL
    url = f"https://swgoh.gg/p/{allycode}/"
    
    # Отправляем GET-запрос
    response = requests.get(url)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем заголовок с именем игрока
        player_name_tag = soup.find('h1', class_='m-0')
        
        if player_name_tag:
            # Извлекаем текст и убираем лишние пробелы
            player_name = player_name_tag.text.strip()
            # Убираем "'s Profile" из строки
            player_name = player_name.replace("'s Profile", "").strip()
            return player_name
        else:
            return "Имя игрока не найдено"
    else:
        return f"Ошибка: {response.status_code}"