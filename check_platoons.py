import os
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
                if relic >= min_relic:  # Учитываем только персонажей с реликом >= min_relic
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
                    player_units[normalized_unit] = relic

            elif is_ships_section:
                unit, level, stars = parts
                stars = int(stars)
                if stars == 7:  # Учитываем только корабли с 7 звёздами
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
                    player_units[normalized_unit] = 0  # Для кораблей релик не учитывается

    for unit in player_units.keys():
        for platoon_unit in planet.keys():
            if unit == platoon_unit:
                if unit in player_units and (player_units[unit] >= planet[platoon_unit][1] or player_units[unit] == 0):
                    result += 1

    return result

def check_planet_coverage(planet_path: str, min_relic: int, names: list, used_units_global: dict) -> dict:
    """
    Проверяет покрытие взводов для одной планеты.
    Использует глобальный словарь used_units_global для отслеживания уже использованных юнитов.
    """
    # Загружаем данные для планеты
    planet = load_data(planet_path)

    # Подсчитываем общее количество доступных юнитов для каждого юнита
    total_ready_units = {}
    for unit in planet.keys():
        total_ready_units[unit] = 0

    # Собираем информацию о том, какие юниты были использованы каждым игроком
    used_units_by_player = {name: [] for name in names}

    # Ограничение на количество юнитов от одного игрока
    max_units_per_player = 10

    # Сначала собираем всех доступных юнитов
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
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
                    if relic >= min_relic and normalized_unit in planet.keys():
                        # Проверяем, не был ли юнит уже использован в другой планете
                        if normalized_unit not in used_units_global:
                            available_units.append((name, normalized_unit))

                elif is_ships_section:
                    unit, level, stars = parts
                    stars = int(stars)
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
                    if stars == 7 and normalized_unit in planet.keys():
                        # Проверяем, не был ли юнит уже использован в другой планете
                        if normalized_unit not in used_units_global:
                            available_units.append((name, normalized_unit))

    # Распределяем юниты с учётом ограничения на количество от одного игрока
    player_units_count = {name: 0 for name in names}  # Счётчик использованных юнитов для каждого игрока
    for name, unit in available_units:
        if player_units_count[name] < max_units_per_player:
            total_ready_units[unit] += 1
            used_units_by_player[name].append(unit)
            used_units_global[unit] = True  # Помечаем юнит как использованный
            player_units_count[name] += 1

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
        "total_required": sum([requirements[0] for requirements in planet.values()]),
        "used_units_by_player": used_units_by_player,  # Добавляем информацию об использованных юнитах
    }

def find_players_with_missing_units(names: list, missing_units: dict, min_relic: int) -> dict:
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
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
                    if normalized_unit in missing_units and abs(relic - min_relic) <= 10:
                        players_with_units[normalized_unit].append((name, relic))

                elif is_ships_section:
                    unit, level, stars = parts
                    stars = int(stars)
                    normalized_unit = normalize_name(unit)  # Нормализуем имя
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

        # Глобальный словарь для отслеживания использованных юнитов
        used_units_global = {}

        # Проверяем покрытие для каждой планеты
        results = []
        for planet_info in planets_to_check:
            try:
                result = check_planet_coverage(planet_info["path"], planet_info["min_relic"], names, used_units_global)
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
                        for unit, requirements in planet_data.items():
                            required_count = requirements[0]
                            available_count = result["coverage"].get(unit, 0)
                            if available_count < required_count:
                                missing_units[unit] = (required_count - available_count, requirements[1])

                        if missing_units:
                            out.write("Недостающие персонажи:\n")
                            for unit, (count, required_relic) in missing_units.items():
                                out.write(f"{unit}: нужно прокачать {count} шт. в р{required_relic}\n")

                            # Находим игроков с недостающими персонажами
                            players_with_units = find_players_with_missing_units(names, missing_units, planet_info["min_relic"])
                            
                            '''
                            out.write("\nИгроки с недостающими персонажами:\n")
                            for unit, players in players_with_units.items():
                                if players:
                                    out.write(f"{unit}:\n")
                                    for player, relic in players:
                                        out.write(f"  {player} (релик: {relic})\n")
                                else:
                                    out.write(f"{unit}: нет игроков с подходящим реликом\n")
                            '''
                        out.write("\n")

                    except Exception as e:
                        print(f"Ошибка при записи результатов для планеты {planet_path}: {e}")
        except Exception as e:
            print(f"Ошибка при записи в файл output/check_platoons.txt: {e}")

        print("Результаты сохранены в файл output/check_platoons.txt")

    except Exception as e:
        print(f"Неожиданная ошибка в функции main: {e}")

if __name__ == '__main__':
    main()