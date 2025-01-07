import os
import requests
from bs4 import BeautifulSoup

import unicodedata

def normalize_name(name: str) -> str:
    """
    Нормализует имя персонажа, удаляя специальные символы и приводя к нижнему регистру.
    """
    # Удаляем специальные символы (например, Î, é и т.д.)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    return name

def load_data(planet_path: str) -> dict:
    platoon = {}

    with open(planet_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            unit, count, relics = line.strip().split('\t')
            normalized_unit = normalize_name(unit)  # Нормализуем имя
            platoon[normalized_unit] = [int(count), int(relics)]

    return platoon

def cnt_ready_units_for_planet(name: str, planet: dict, min_relic: int) -> int:
    result = 0
    player_units = {}
    with open(f'guild/{name}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Пропускаем первые две строки (заголовок и разделитель)
        for line in lines[4:]:
            if not line.strip():  # Пропускаем пустые строки
                continue
            parts = line.strip().split('\t')
            if len(parts) < 3:  # Если строка не содержит всех данных, пропускаем
                continue
            unit, level, relic = parts
            relic = int(relic)
            if relic >= min_relic:  # Учитываем только персонажей с реликом >= min_relic
                normalized_unit = normalize_name(unit)  # Нормализуем имя
                player_units[normalized_unit] = relic
    
    for unit in player_units.keys():
        for platoon_unit in planet.keys():
            if unit == platoon_unit and player_units[unit] >= planet[platoon_unit][1]:
                result += 1

    return result

def check_planet_coverage(planet_path: str, min_relic: int, names: list) -> dict:
    # Загружаем данные для планеты
    planet = load_data(planet_path)

    # Считаем, сколько персонажей с реликом >= min_relic есть у каждого игрока
    player_ready_units = {}
    for name in names:
        player_ready_units[name] = cnt_ready_units_for_planet(name, planet, min_relic)

    # Подсчитываем общее количество доступных персонажей для каждого юнита
    total_ready_units = {}
    for unit in planet.keys():
        total_ready_units[unit] = 0

    for name in names:
        with open(f'guild/{name}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines[4:]:  # Пропускаем первые две строки
                if not line.strip():  # Пропускаем пустые строки
                    continue
                parts = line.strip().split('\t')
                if len(parts) < 3:  # Если строка не содержит всех данных, пропускаем
                    continue
                unit, level, relic = parts
                relic = int(relic)
                normalized_unit = normalize_name(unit)  # Нормализуем имя
                if relic >= min_relic and normalized_unit in planet.keys():
                    total_ready_units[normalized_unit] += 1

    # Сравниваем с требованиями взводов
    platoon_coverage = {}
    for unit, requirements in planet.items():
        required_count = requirements[0]
        available_count = total_ready_units.get(unit, 0)
        platoon_coverage[unit] = min(available_count, required_count)

    return {
        "planet_name": os.path.basename(planet_path).replace('.txt', ''),
        "coverage": platoon_coverage,
        "total_covered": sum(platoon_coverage.values()),
        "total_required": sum([requirements[0] for requirements in planet.values()])
    }

def main():
    try:
        # Список планет и минимальных реликов для каждой
        planets_to_check = [
            {"path": "platoons/4 sector/Lothal.txt", "min_relic": 8},
            {"path": "platoons/4 sector/Kessel.txt", "min_relic": 8},
            {"path": "platoons/4 sector/MedicalStation.txt", "min_relic": 8},
        ]

        # Список имен игроков в гильдии
        names = []
        try:
            with open('db/names.txt', 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    names.append(line.strip())
        except FileNotFoundError:
            print("Ошибка: Файл db/names.txt не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении файла db/names.txt: {e}")
            return

        # Проверяем покрытие для каждой планеты
        results = []
        for planet_info in planets_to_check:
            try:
                result = check_planet_coverage(planet_info["path"], planet_info["min_relic"], names)
                results.append((planet_info["path"], result))  # Сохраняем путь к планете вместе с результатом
            except FileNotFoundError:
                print(f"Ошибка: Файл планеты {planet_info['path']} не найден.")
                continue
            except Exception as e:
                print(f"Ошибка при обработке планеты {planet_info['path']}: {e}")
                continue

        # Выводим результаты в файл
        os.makedirs('output', exist_ok=True)  # Создаем папку output, если её нет
        try:
            with open('output/check_platoons.txt', 'w', encoding='utf-8') as out:
                for planet_path, result in results:
                    try:
                        planet_data = load_data(planet_path)  # Загружаем данные для текущей планеты
                        out.write(f"Покрытие взводов для планеты {result['planet_name']}:\n")
                        for unit, coverage in result["coverage"].items():
                            if unit in planet_data:  # Проверяем, есть ли персонаж в данных планеты
                                out.write(f"{unit}: {coverage}/{planet_data[unit][0]}\n")
                            else:
                                out.write(f"{unit}: {coverage}/0\n")  # Если персонажа нет, выводим 0
                        out.write(f"Общее покрытие: {result['total_covered']}/{result['total_required']}\n\n")
                    except Exception as e:
                        print(f"Ошибка при записи результатов для планеты {planet_path}: {e}")
        except Exception as e:
            print(f"Ошибка при записи в файл output/check_platoons.txt: {e}")

        print("Результаты сохранены в файл output/check_platoons.txt")

    except Exception as e:
        print(f"Неожиданная ошибка в функции main: {e}")

if __name__ == '__main__':
    main()