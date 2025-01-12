import os
import unicodedata

def normalize_name(name: str) -> str:
    """
    Нормализует имя персонажа, удаляя специальные символы и приводя к нижнему регистру.
    """
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    return name

def load_data(planet_path: str) -> dict:
    """
    Загружает данные о взводах для планеты.
    """
    platoon = {}
    with open(planet_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            unit, count, relics = line.strip().split('\t')
            normalized_unit = normalize_name(unit)
            platoon[normalized_unit] = [int(count), int(relics)]
    return platoon

def check_planet_coverage(planets_to_check: list, min_relic: int, names: list) -> dict:
    """
    Проверяет покрытие взводов для всех планет одновременно.
    Возвращает словарь с результатами для каждой планеты.
    """
    # Загружаем данные для всех планет
    planets_data = {}
    for planet_info in planets_to_check:
        planet_path = planet_info["path"]
        planets_data[planet_path] = load_data(planet_path)

    # Собираем все доступные юниты
    available_units = []
    for name in names:
        with open(f'guild/{name}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            is_characters_section = False
            is_ships_section = False

            for line in lines:
                if "Персонажи:" in line:
                    is_characters_section = True
                    is_ships_section = False
                    continue
                if "Корабли:" in line:
                    is_characters_section = False
                    is_ships_section = True
                    continue
                if not line.strip() or "Имя персонажа" in line or "Имя корабля" in line or "---" in line:
                    continue  # Пропускаем заголовки и разделители

                parts = line.strip().split('\t')
                if len(parts) < 3:  # Если строка не содержит всех данных, пропускаем
                    continue

                if is_characters_section:
                    unit, level, relic, stars = parts
                    relic = int(relic)
                    normalized_unit = normalize_name(unit)
                    if relic >= min_relic:
                        available_units.append((name, normalized_unit))

                elif is_ships_section:
                    unit, level, stars = parts
                    stars = int(stars)
                    normalized_unit = normalize_name(unit)
                    if stars == 7:
                        available_units.append((name, normalized_unit))

    # Определяем редкость юнитов
    unit_rarity = {}
    for _, unit in available_units:
        if unit in unit_rarity:
            unit_rarity[unit] += 1
        else:
            unit_rarity[unit] = 1

    # Сортируем юниты по редкости (от редких к частым)
    sorted_units = sorted(available_units, key=lambda x: unit_rarity[x[1]])

    # Собираем общие требования для всех планет
    total_requirements = {}
    for planet_path, planet_data in planets_data.items():
        for unit, requirements in planet_data.items():
            if unit in total_requirements:
                total_requirements[unit] += requirements[0]
            else:
                total_requirements[unit] = requirements[0]

    # Распределяем юниты с учётом ограничения на количество от одного игрока
    max_units_per_player = 10
    player_units_count = {name: 0 for name in names}  # Счётчик использованных юнитов для каждого игрока
    used_units_global = {}  # Словарь для отслеживания использованных юнитов
    used_units_by_player = {name: [] for name in names}  # Словарь для отслеживания юнитов по игрокам
    used_units_by_planet = {planet_path: {} for planet_path in planets_data.keys()}  # Словарь для отслеживания юнитов по планетам

    for name, unit in sorted_units:
        if player_units_count[name] < max_units_per_player:
            if unit in total_requirements and total_requirements[unit] > 0:
                total_requirements[unit] -= 1
                used_units_global[unit] = used_units_global.get(unit, 0) + 1
                used_units_by_player[name].append(unit)
                player_units_count[name] += 1

                # Распределяем юнит по планетам
                for planet_path, planet_data in planets_data.items():
                    if unit in planet_data and used_units_by_planet[planet_path].get(unit, 0) < planet_data[unit][0]:
                        used_units_by_planet[planet_path][unit] = used_units_by_planet[planet_path].get(unit, 0) + 1
                        break  # Юнит распределён для одной планеты, переходим к следующему

    # Проверяем покрытие для каждой планеты
    results = []
    for planet_path, planet_data in planets_data.items():
        platoon_coverage = {}
        for unit, requirements in planet_data.items():
            required_count = requirements[0]
            available_count = used_units_by_planet[planet_path].get(unit, 0)
            platoon_coverage[unit] = {
                "available": available_count,
                "required": required_count,
            }

        results.append({
            "planet_name": os.path.basename(planet_path).replace('.txt', ''),
            "coverage": platoon_coverage,
            "total_covered": sum([min(cov["available"], cov["required"]) for cov in platoon_coverage.values()]),
            "total_required": sum([requirements[0] for requirements in planet_data.values()]),
            "used_units_by_player": used_units_by_player,  # Добавляем информацию об использованных юнитах
        })

    return results

def find_players_with_missing_units(names: list, missing_units: dict, min_relic: int) -> dict:
    """
    Находит игроков с недостающими персонажами.
    """
    players_with_units = {}

    for unit in missing_units.keys():
        players_with_units[unit] = []

    for name in names:
        with open(f'guild/{name}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            is_characters_section = False
            is_ships_section = False

            for line in lines:
                if "Персонажи:" in line:
                    is_characters_section = True
                    is_ships_section = False
                    continue
                if "Корабли:" in line:
                    is_characters_section = False
                    is_ships_section = True
                    continue
                if not line.strip() or "Имя персонажа" in line or "Имя корабля" in line or "---" in line:
                    continue  # Пропускаем заголовки и разделители

                parts = line.strip().split('\t')
                if len(parts) < 3:  # Если строка не содержит всех данных, пропускаем
                    continue

                if is_characters_section:
                    unit, level, relic, stars = parts
                    relic = int(relic)
                    normalized_unit = normalize_name(unit)
                    if normalized_unit in missing_units and abs(relic - min_relic) <= 10:
                        players_with_units[normalized_unit].append((name, relic))

                elif is_ships_section:
                    unit, level, stars = parts
                    stars = int(stars)
                    normalized_unit = normalize_name(unit)
                    if normalized_unit in missing_units and stars == 7:
                        players_with_units[normalized_unit].append((name, 0))  # Для кораблей релик не учитывается

    # Сортируем игроков по уровню релика в порядке убывания
    for unit in players_with_units.keys():
        players_with_units[unit].sort(key=lambda x: x[1], reverse=True)

    return players_with_units

def main():
    try:
        # Список планет и минимальных реликов для каждой
        planets_to_check = [
            {"path": "platoons/4 sector/Kessel.txt", "min_relic": 8},
            {"path": "platoons/4 sector/MedicalStation.txt", "min_relic": 8},
            {"path": "platoons/4 sector/Lothal.txt", "min_relic": 8},
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

        # Проверяем покрытие для всех планет
        results = check_planet_coverage(planets_to_check, 8, names)

        # Выводим результаты в файл
        os.makedirs('output', exist_ok=True)  # Создаем папку output, если её нет
        try:
            with open('output/check_platoons.txt', 'w', encoding='utf-8') as out:
                for result in results:
                    try:
                        out.write(f"Покрытие взводов для планеты {result['planet_name']}:\n")
                        for unit, coverage in result["coverage"].items():
                            out.write(f"{unit}: {coverage['available']}/{coverage['required']}\n")
                        out.write(f"Общее покрытие: {result['total_covered']}/{result['total_required']}\n\n")

                        # Выводим список использованных юнитов
                        out.write("Использованные юниты:\n")
                        for name, units in result["used_units_by_player"].items():
                            if units:
                                out.write(f"{name}:\n")
                                for unit in units:
                                    out.write(f"  {unit}\n")
                        out.write("\n")

                        # Определяем недостающих персонажей
                        missing_units = {}
                        for unit, coverage in result["coverage"].items():
                            if coverage["available"] < coverage["required"]:
                                missing_units[unit] = (coverage["required"] - coverage["available"], 8)  # Пример: требуемый релик 8

                        if missing_units:
                            out.write("Недостающие персонажи:\n")
                            for unit, (count, required_relic) in missing_units.items():
                                out.write(f"{unit}: нужно прокачать {count} шт. в р{required_relic}\n")

                            # Находим игроков с недостающими персонажами
                            players_with_units = find_players_with_missing_units(names, missing_units, 8)
                            
                            out.write("\nИгроки с недостающими персонажами:\n")
                            for unit, players in players_with_units.items():
                                if players:
                                    out.write(f"{unit}:\n")
                                    for player, relic in players:
                                        out.write(f"  {player} (релик: {relic})\n")
                                else:
                                    out.write(f"{unit}: нет игроков с подходящим реликом\n")

                        out.write("\n")

                    except Exception as e:
                        print(f"Ошибка при записи результатов для планеты {result['planet_name']}: {e}")
        except Exception as e:
            print(f"Ошибка при записи в файл output/check_platoons.txt: {e}")

        print("Результаты сохранены в файл output/check_platoons.txt")

    except Exception as e:
        print(f"Неожиданная ошибка в функции main: {e}")

if __name__ == '__main__':
    main()