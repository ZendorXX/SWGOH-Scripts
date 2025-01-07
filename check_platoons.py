import os

def load_data(planet_path: str) -> dict:
    platoon = {}

    try:
        with open(planet_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file.readlines(), start=1):
                try:
                    unit, count, relics = line.strip().split('\t')
                    platoon[unit] = [int(count), int(relics)]
                except ValueError as e:
                    print(f"Ошибка в файле {planet_path}, строка {line_number}: {line.strip()}")
                    print(f"Ожидалось 3 значения, разделенных табуляцией, но получено: {line.strip().split('\t')}")
                    raise e
    except Exception as e:
        print(f"Ошибка при загрузке файла {planet_path}: {e}")
        raise e

    return platoon

def cnt_ready_units_for_planet(name: str, planet: dict, min_relic: int, used_units: dict) -> int:
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
                player_units[unit] = relic
    
    for unit in player_units.keys():
        for platoon_unit in planet.keys():
            if unit == platoon_unit and player_units[unit] >= planet[platoon_unit][1]:
                # Проверяем, не был ли персонаж уже использован
                if name not in used_units:
                    used_units[name] = []
                if unit not in used_units[name]:
                    result += 1
                    used_units[name].append(unit)  # Помечаем персонажа как использованного

    return result

def check_planet_coverage(planet_path: str, min_relic: int, names: list, used_units: dict) -> dict:
    # Загружаем данные для планеты
    try:
        planet = load_data(planet_path)
    except Exception as e:
        print(f"Ошибка при загрузке данных для планеты {planet_path}: {e}")
        return {
            "planet_name": os.path.basename(planet_path).replace('.txt', ''),
            "coverage": {},
            "total_covered": 0,
            "total_required": 0
        }

    # Считаем, сколько персонажей с реликом >= min_relic есть у каждого игрока
    player_ready_units = {}
    for name in names:
        player_ready_units[name] = cnt_ready_units_for_planet(name, planet, min_relic, used_units)

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
                if relic >= min_relic and unit in planet.keys():
                    # Проверяем, не был ли персонаж уже использован
                    if name not in used_units:
                        used_units[name] = []
                    if unit not in used_units[name]:
                        total_ready_units[unit] += 1
                        used_units[name].append(unit)  # Помечаем персонажа как использованного

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
    # Список планет и минимальных реликов для каждой
    planets_to_check = [
        {"path": "platoons/4 sector/Kessel.txt", "min_relic": 8},
        {"path": "platoons/4 sector/Lothal.txt", "min_relic": 8},
        {"path": "platoons/4 sector/MedicalStation.txt", "min_relic": 8},
    ]

    # Список имен игроков в гильдии
    names = []
    with open('db/names.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            names.append(line.strip())

    # Словарь для учета использованных персонажей
    used_units = {name: [] for name in names}  # Формат: {имя_игрока: [список_использованных_персонажей]}

    # Проверяем покрытие для каждой планеты
    results = []
    for planet_info in planets_to_check:
        result = check_planet_coverage(planet_info["path"], planet_info["min_relic"], names, used_units)
        results.append(result)

    # Выводим результаты в файл
    os.makedirs('output', exist_ok=True)  # Создаем папку output, если её нет
    with open('output/check_platoons.txt', 'w', encoding='utf-8') as out:
        for result in results:
            out.write(f"Покрытие взводов для планеты {result['planet_name']}:\n")
            for unit, coverage in result["coverage"].items():
                try:
                    out.write(f"{unit}: {coverage}/{load_data(planet_info['path'])[unit][0]}\n")
                except KeyError as e:
                    print(f"Ошибка: Персонаж {unit} отсутствует в данных для планеты {planet_info['path']}.")
                    print(f"Список персонажей для планеты {planet_info['path']}: {list(load_data(planet_info['path']).keys())}")
                    raise e
            out.write(f"Общее покрытие: {result['total_covered']}/{result['total_required']}\n\n")

    print("Результаты сохранены в файл output/check_platoons.txt")

if __name__ == '__main__':
    main()