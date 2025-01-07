import csv

relic_value = 6

file_name = './csv/unit-export.csv'

count = 0

with open(file_name, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        if row['Relic Tier'] and int(row['Relic Tier']) >= relic_value:
            count += 1

print(f"Количество игроков с уровнем реликвий больше или равным {relic_value}: {count}")