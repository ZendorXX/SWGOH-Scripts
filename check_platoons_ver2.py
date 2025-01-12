import os
import sys
import unicodedata
from collections import defaultdict

def normalize_name(name: str) -> str:
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    return name

# Структура для хранения данных о юнитах игроков
players_units = defaultdict(lambda: {"characters": {}, "ships": {}})

# Чтение данных игроков
def read_player_data(player_file):
    with open(player_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    player_name = lines[0].strip().replace("Игрок: ", "")
    current_section = None
    
    for line in lines[1:]:
        line = line.strip()
        # Пропускаем разделительные строки
        if line == "----------------------------------------" or line == "------------------------------":
            continue
        # Определяем текущий раздел (персонажи или корабли)
        if line == "Персонажи:":
            current_section = "characters"
            continue
        elif line == "Корабли:":
            current_section = "ships"
            continue
        # Пропускаем строки с заголовками
        if line.startswith("Имя персонажа") or line.startswith("Имя корабля"):
            continue
        # Парсим данные, если текущий раздел определён
        if current_section and line:
            parts = line.split('\t')
            if len(parts) >= 3:
                name = normalize_name(parts[0])
                try:
                    if current_section == "characters":
                        level = int(parts[1])
                        relic = int(parts[2])
                        stars = int(parts[3])
                        players_units[player_name]["characters"][name] = {
                            "level": level,
                            "relic": relic,
                            "stars": stars
                        }
                    elif current_section == "ships":
                        level = int(parts[1])
                        stars = int(parts[2])
                        players_units[player_name]["ships"][name] = {
                            "level": level,
                            "stars": stars
                        }
                except ValueError:
                    # Пропускаем строки, которые не удалось распарсить
                    print(f"Ошибка при парсинге строки: {line} в файле {player_file}")
                    continue

# Чтение данных о взводах планет
def read_platoon_data(platoon_file):
    with open(platoon_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    platoon_units = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 3:
            name = normalize_name(parts[0])
            count = int(parts[1])
            relic_or_stars = int(parts[2])
            platoon_units.append({
                "name": name,
                "count": count,
                "relic_or_stars": relic_or_stars
            })
    
    return platoon_units

# Подсчёт доступных юнитов, соответствующих требованиям
def count_available_units(players_units, platoon_units):
    available_units = defaultdict(int)
    
    for unit in platoon_units:
        name = unit["name"]
        relic_or_stars = unit["relic_or_stars"]
        
        for player, data in players_units.items():
            if name in data["characters"]:
                if data["characters"][name]["relic"] >= relic_or_stars:
                    available_units[name] += 1
            elif name in data["ships"]:
                if data["ships"][name]["stars"] >= relic_or_stars:
                    available_units[name] += 1
    
    return available_units

# Распределение юнитов
def distribute_units(players_units, platoon_units, planet_name, player_assigned_units):
    # Словарь для хранения распределённых юнитов
    assigned_units = defaultdict(lambda: defaultdict(int))
    
    # Словарь для хранения недостающих юнитов
    missing_units = defaultdict(int)
    
    # Сначала сортируем юнитов по их редкости (чем меньше юнитов в гильдии, тем выше приоритет)
    unit_rarity = defaultdict(int)
    for player, data in players_units.items():
        for unit in data["characters"]:
            unit_rarity[unit] += 1
        for unit in data["ships"]:
            unit_rarity[unit] += 1
    
    # Сортируем юнитов по редкости
    sorted_units = sorted(platoon_units, key=lambda x: unit_rarity[x["name"]])
    
    # Распределяем юнитов
    for unit in sorted_units:
        name = unit["name"]
        required_count = unit["count"]
        relic_or_stars = unit["relic_or_stars"]
        
        # Ищем игроков, у которых есть этот юнит и он соответствует требованиям
        for player, data in players_units.items():
            if name in data["characters"]:
                if (data["characters"][name]["relic"] >= relic_or_stars and
                    player_assigned_units[player][name] == 0):  # Юнит ещё не выставлен на другую планету
                    assigned_units[player][name] = 1
                    player_assigned_units[player][name] = 1  # Помечаем юнита как использованного
                    required_count -= 1
                    if required_count == 0:
                        break  # Прекращаем поиск, если все требуемые юниты распределены
            elif name in data["ships"]:
                if (data["ships"][name]["stars"] >= relic_or_stars and
                    player_assigned_units[player][name] == 0):  # Юнит ещё не выставлен на другую планету
                    assigned_units[player][name] = 1
                    player_assigned_units[player][name] = 1  # Помечаем юнита как использованного
                    required_count -= 1
                    if required_count == 0:
                        break  # Прекращаем поиск, если все требуемые юниты распределены
        
        # Если юнитов не хватило, добавляем в недостачу
        if required_count > 0:
            missing_units[name] += required_count
    
    return missing_units, assigned_units

# Основная функция
def main():
    # Перенаправляем вывод в файл
    with open("output/output.txt", "w", encoding="utf-8") as f:
        sys.stdout = f  # Перенаправляем stdout в файл

        # Чтение данных игроков
        guild_folder = "guild"
        for player_file in os.listdir(guild_folder):
            if player_file.endswith(".txt"):
                read_player_data(os.path.join(guild_folder, player_file))
        
        # Чтение данных о взводах планет
        platoon_files = [
            ("platoons/4 sector/Kessel.txt", "Kessel"),
            ("platoons/4 sector/MedicalStation.txt", "MedicalStation"),
            ("platoons/4 sector/Lothal.txt", "Lothal")
        ]
        all_missing_units = defaultdict(lambda: defaultdict(int))
        all_required_units = defaultdict(int)
        all_available_units = defaultdict(int)
        player_assignments = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        planet_totals = defaultdict(int)
        player_totals = defaultdict(int)
        
        # Словарь для хранения использованных юнитов игроков
        player_assigned_units = defaultdict(lambda: defaultdict(int))
        
        # Подсчёт доступных юнитов для всех планет
        for platoon_file, planet_name in platoon_files:
            platoon_units = read_platoon_data(platoon_file)
            available_units = count_available_units(players_units, platoon_units)
            for unit, count in available_units.items():
                all_available_units[unit] = count  # Обновляем общее количество доступных юнитов
        
        for platoon_file, planet_name in platoon_files:
            platoon_units = read_platoon_data(platoon_file)
            missing_units, assigned_units = distribute_units(players_units, platoon_units, planet_name, player_assigned_units)
            
            for unit, count in missing_units.items():
                all_missing_units[planet_name][unit] += count
            for unit in platoon_units:
                all_required_units[unit["name"]] += unit["count"]
            
            # Сохраняем распределённые юниты для каждого игрока и планеты
            for player, units in assigned_units.items():
                for unit, count in units.items():
                    player_assignments[player][planet_name][unit] += count
                    player_totals[player] += count
                    planet_totals[planet_name] += count
        
        # Вывод результата
        print("Недостающие юниты для заполнения всех взводов:")
        for planet_name, missing_units in all_missing_units.items():
            print(f"\nПланета: {planet_name}")
            for unit, count in missing_units.items():
                available = all_available_units.get(unit, 0)
                required = all_required_units.get(unit, 0)
                print(f"{unit}: {available}/{required} (не хватает {count})")
        
        # Вывод информации о распределённых юнитах
        print("\nРаспределённые юниты по игрокам:")
        for player, planets in player_assignments.items():
            print(f"\nИгрок: {player}")
            total_player = 0
            for planet_name, units in planets.items():
                total_planet = 0
                print(f"  Планета: {planet_name}")
                for unit, count in units.items():
                    print(f"    {unit}: {count}")
                    total_planet += count
                print(f"  Всего на планету {planet_name}: {total_planet}")
                total_player += total_planet
            print(f"  Всего выставил юнитов: {total_player}")
        
        # Вывод суммарных данных по планетам
        print("\nСуммарные данные по планетам:")
        for planet_name, total in planet_totals.items():
            print(f"Планета {planet_name}: {total} юнитов")

if __name__ == "__main__":
    main()