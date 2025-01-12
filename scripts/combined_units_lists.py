from collections import defaultdict

# Словарь для хранения суммарных количеств юнитов
units = defaultdict(lambda: [0, 8])

# Функция для обработки одного файла
def process_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                unit, count, relic_level = parts
                units[unit][0] += int(count)
                # Уровень реликвии остается максимальным из всех
                units[unit][1] = max(units[unit][1], int(relic_level))

# Обработка всех файлов
files = ['platoons/4 sector/Kessel.txt', 'platoons/4 sector/MedicalStation.txt', 'platoons/4 sector/Lothal.txt']
for file in files:
    process_file(file)

# Запись результата в общий файл
with open('platoons/4 sector/combined_units.txt', 'w') as output_file:
    for unit, (count, relic_level) in sorted(units.items()):
        output_file.write(f"{unit}\t{count}\t{relic_level}\n")

print("Файлы успешно объединены в 'combined_units.txt'")