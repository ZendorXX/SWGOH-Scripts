from collections import defaultdict
import os

# Словарь для хранения данных о юнитах
units = defaultdict(lambda: {"total_count": 0, "relic_level": 8, "planets": {}})

# Функция для обработки одного файла
def process_file(filename):
    with open(filename, 'r') as file:
        # Извлекаем имя планеты из пути к файлу
        planet_name = os.path.basename(filename).replace(".txt", "")
        
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                unit, count, relic_level = parts
                count = int(count)
                relic_level = int(relic_level)
                
                # Обновляем общее количество и уровень реликвии
                units[unit]["total_count"] += count
                units[unit]["relic_level"] = max(units[unit]["relic_level"], relic_level)
                
                # Добавляем информацию о планете
                units[unit]["planets"][planet_name] = count

# Обработка всех файлов
files = [
    'platoons/4 sector/Kessel.txt',
    'platoons/4 sector/MedicalStation.txt',
    'platoons/4 sector/Lothal.txt'
]
for file in files:
    process_file(file)

# Запись результата в общий файл
with open('platoons/4 sector/combined_units.txt', 'w') as output_file:
    for unit, data in sorted(units.items()):
        total_count = data["total_count"]
        relic_level = data["relic_level"]
        planets_info = ", ".join([f"{planet}: {count}" for planet, count in data["planets"].items()])
        
        # Форматируем строку для записи в файл
        #output_file.write(f"{unit}\t{total_count}\t{relic_level}\t{planets_info}\n")
        output_file.write(f"{unit}\t{total_count}\t{relic_level}\n")

print("Файлы успешно объединены в 'combined_units.txt'")