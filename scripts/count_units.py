from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

# Список персонажей и их требуемый уровень реликвий
characters_data = """
Clone Sergeant - Phase I	5
Dengar	5
Jolee Bindo	5
Bossk	5
First Order Officer	5
IG-88	5
Darth Sion	5
Darth Traya	5
Barriss Offee	5
Visas Marr	5
Sana Starros	5
Embo	5
Jyn Erso	5
Rebel Officer Leia Organa	5
Dark Trooper	5
Asajj Ventress	5
Hermit Yoda	5
Poe Dameron	5
Imperial Super Commando	5
Amilyn Holdo	6
Cad Bane	6
Hondo Ohnaka	6
B1 Battle Droid	6
Grand Moff Tarkin	7
Ki-Adi-Mundi	7
Nute Gunray	7
The Mandalorian (Beskar Armor)	7
Mara Jade, The Emperor's Hand	7
BT-1	7
Rey (Jedi Training)	7
Ewok Scout	7
Ninth Sister	7
Darth Sidious	7
Logray	7
Darth Maul	7
Grand Admiral Thrawn	7
Fifth Brother	7
BB-8	7
Kylo Ren (Unmasked)	7
Darth Vader	7
Sith Trooper	7
Seventh Sister	7
Threepio & Chewie	7
Greef Karga	7
General Grievous	7
Cara Dune	7
Jango Fett	7
Bastila Shan	7
0-0-0	7
Emperor Palpatine	7
Commander Luke Skywalker	7
HK-47	7
Bastila Shan (Fallen)	7
Jedi Knight Anakin	7
Wat Tambor	7
Chewbacca	8
Admiral Ackbar	8
Boushh (Leia Organa)	8
Krrsantan	8
Maul	8
Boba Fett	8
Grand Inquisitor	8
C-3PO	8
Iden Versio	8
Jedi Knight Revan	8
ARC Trooper	8
Colonel Starck	8
Boba Fett, Scion of Jango	8
Sith Empire Trooper	8
Sith Eternal Emperor	8
R2-D2	8
Supreme Leader Kylo Ren	8
Grand Master Yoda	8
Starkiller	8
Han Solo	8
Ben Solo	8
Sith Assassin	8
Count Dooku	8
Darth Malgus	8
Lord Vader	9
General Kenobi	9
Rey	9
Jedi Master Luke Skywalker	9
General Skywalker	9
Ahsoka Tano (Fulcrum)	9
Jedi Master Kenobi	9
Darth Revan	9
Jedi Knight Luke Skywalker	9
Commander Ahsoka Tano	9
Darth Malak	9
Admiral Piett	9
"""

# Преобразуем данные в словарь
characters_dict = {}
for line in characters_data.strip().split("\n"):
    name, relic_level = line.strip().split("\t")
    characters_dict[name] = int(relic_level)

# URL страницы unit-search
unit_search_url = "https://swgoh.gg/g/Jh-UF8xOQ9-OGLLHBDJg3Q/unit-search/"

# Инициализация Selenium WebDriver
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver
driver.get(unit_search_url)

# Словарь для подсчета персонажей
character_count = {name: 0 for name in characters_dict}

# Проходим по каждому персонажу
for character_name, required_relic_level in characters_dict.items():
    # Выбираем персонажа из выпадающего списка
    select_element = Select(driver.find_element(By.ID, "unit-select"))
    select_element.select_by_visible_text(character_name)
    
    # Ждем, пока таблица обновится
    time.sleep(2)
    
    # Извлекаем данные из таблицы
    table = driver.find_element(By.CLASS_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    # Проходим по каждой строке таблицы (исключая заголовок)
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 4:
            continue
        
        # Извлекаем уровень реликвий
        relic_tier = int(cells[3].text) if cells[3].text.isdigit() else 0
        
        # Проверяем, соответствует ли уровень реликвий требуемому
        if relic_tier >= required_relic_level:
            character_count[character_name] += 1

# Закрываем браузер
driver.quit()

# Выводим результат
for character, count in character_count.items():
    print(f"{character}: {count} игроков")