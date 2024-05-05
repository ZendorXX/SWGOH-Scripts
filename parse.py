import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_data_characters(url: str) -> list:
    responce = requests.get(url, headers=headers)

    if responce.status_code != 200:
        return None

    soup = BeautifulSoup(responce.text, 'html.parser')

    data = list(str(soup.select("li.media")).split('\n'))

    result = []

    garbage_symbols = ['<', '[']

    for element in data:
        if element[0] not in garbage_symbols: 
            result.append(element) 
            continue

    return result

def check(s: str) -> bool:
    if not(s[0] == '<' and s[1] == 'a'):
        return False
    
    closing_cnt = s.count('>')

    if closing_cnt != 2:
        return False

    return True

def extract(s: str) -> str:
    '<a class="collection-ship-name-link" href="/p/827134165/ships/tie-advanced-x1" rel="nofollow">TIE Advanced x1</a>'

    start_pos = 0
    for i in range(len(s)):
        if s[i] == '>':
            start_pos = i + 1
            break
    
    end_pos = 0
    for i in range(1, len(s)):
        if s[i] == '<':
            end_pos = i
            break

    return s[start_pos:end_pos]


def get_data_ships(url: str) -> list:
    responce = requests.get(url, headers=headers)

    if responce.status_code != 200:
        return None

    soup = BeautifulSoup(responce.text, 'html.parser')

    data = list(str(soup.select("li.media")).split('\n'))

    result = []

    garbage_symbols = ['<', '[']

    for element in data:
        if element[0] not in garbage_symbols: 
            result.append(element) 
        elif check(element):
            result.append(extract(element))

    with open('output/tmp.txt', 'w') as out:
        out.write(str(result))

    return result

def data_to_dict(data: list) -> dict:
    result = {}

    for i in range(0, len(data) - 1, 2):
        result[data[i + 1]] = int(data[i])
    
    return result

# уровень корабля - процент готовности - релики пилотов
def parse_ships(data: list) -> dict:
    result = {}
    
    digits_cnt = 0
    for i in range(len(data)):
        if data[i][0].isdigit():
            digits_cnt += 1
        else:
            print((digits_cnt - 1) // 2) 
            result[data[i]] = list(map(int, data[i - digits_cnt : i]))
            digits_cnt = 0
    
    return result

def write_dict(dict: dict, file: str) -> None:
    with open(file, 'w') as out:
        for key in dict.keys():
            out.write(f'{key}: {dict[key]}\n')

myallycode = 827134165
allycode = 484439191

characters = data_to_dict(get_data_characters(f'https://swgoh.gg/p/{allycode}/characters/'))
ships = parse_ships(get_data_ships(f'https://swgoh.gg/p/{allycode}/ships/'))

file = 'output/Irisha_units.txt'

with open(file, 'w') as out:
    #out.write('Characters\n')

    for key in characters.keys():
        #out.write(f'{key}: {characters[key]}\n')
        out.write(f'{key}\n')

    #out.write('Ships\n')

    for key in ships.keys():
        #out.write(f'{key}: {ships[key]}\n')
        out.write(f'{key}\n')

