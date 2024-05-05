with open('db/platoon_total.txt') as file:
    text = file.readlines()
    platoon_total = []
    for line in text:
        platoon_total.append(list(line.split(':'))[0])

with open('db/Irisha_units.txt') as file:
    text = file.read()
    player_units = list(text.split('\n'))

with open('output/check.txt', 'w') as file:
    for unit in platoon_total:
        if unit in player_units:
            file.write(f'{unit}\n')