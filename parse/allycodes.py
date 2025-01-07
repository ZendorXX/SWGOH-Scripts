import requests
from bs4 import BeautifulSoup

# URL страницы гильдии
url = 'https://swgoh.gg/g/Jh-UF8xOQ9-OGLLHBDJg3Q/'

# Заголовки для имитации запроса от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Отправляем GET-запрос
response = requests.get(url, headers=headers)

# Проверяем, успешен ли запрос
if response.status_code == 200:
    # Парсим HTML-страницу
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим все строки таблицы с участниками
    rows = soup.find_all('tr')
    
    # Открываем файл для записи
    with open('db/allycodes.txt', 'w') as file:
        for row in rows:
            # Находим ссылку на профиль участника
            profile_link = row.find('a', href=True)
            if profile_link and '/p/' in profile_link['href']:
                # Извлекаем allycode из ссылки
                allycode = profile_link['href'].split('/')[2]
                # Записываем allycode в файл
                file.write(allycode + '\n')
    print("Allycodes успешно записаны в файл allycodes.txt")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")