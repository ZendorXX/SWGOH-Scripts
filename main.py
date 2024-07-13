def load_data(planet_name: str) -> dict:
    platoon = {}

    with open(f'platoons/{planet_name}.txt', 'r') as file:
        for line in file.readlines():
            unit, count, relics = line.split('\t')
            platoon[unit] = [int(count), int(relics)]

    return platoon

def phase_total(planet_list: list[dict]) -> dict: #TODO: correct adding units with different relics
    total = {}

    for planet in planet_list:
        for unit in planet.keys():
            if unit not in total or total[unit][1] != planet[unit][1]:
                total[unit] = [planet[unit][0], planet[unit][1]]
                continue
            
            total[unit][0] += planet[unit][0]

    #return dict(sorted(total.items(), key=lambda item: (-item[1][0], item[0])))
    return total

Corelia = load_data('1 sector/Corelia')
Coruscant = load_data('1 sector/Coruscant')
Mustafar = load_data('1 sector/Mustafar')

Bracca = load_data('2 sector/Bracca')
Felucia = load_data('2 sector/Felucia')
Geonosis = load_data('2 sector/Geonosis')

Dathomir = load_data('3 sector/Dathomir')
Kashyyyk = load_data('3 sector/Kashyyyk')
Tatooine = load_data('3 sector/Tatooine')

MedicalStation = load_data('4 sector/MedicalStation')
Kessel = load_data('4 sector/Kessel')


def cnt_ready_units_for_planet(name: str, planet: dict) -> int:
    result = 0
    player_units = {}
    with open(f'guild/{name}.txt') as file:
        for line in file.readlines():
            unit, relics = line.split(':')
            if int(relics) <= 9:
                player_units[unit] = int(relics)
    
    for unit in player_units.keys():
        for platoon_unit in planet.keys():
            if unit == platoon_unit and player_units[unit] >= planet[platoon_unit][1]:
                result += 1

    return result

def ready_units_for_planet(name: str, planet: dict) -> list:
    result = []
    player_units = {}
    with open(f'guild/{name}.txt') as file:
        for line in file.readlines():
            unit, relics = line.split(':')
            if int(relics) <= 9:
                player_units[unit] = int(relics)

    for unit in player_units.keys():
        for platoon_unit in planet.keys():
            if unit == platoon_unit and player_units[unit] >= planet[platoon_unit][1]:
                result.append([unit, player_units[unit]])

    return result

def get_player_units_for_platoons(name: str) -> list:
    result_set = set()
    for planet in planets:
            ready_units = ready_units_for_planet(name, planet)
            for item in ready_units:
                result_set.add(tuple(item))
                
    result = []
    for item in result_set:
        result.append(list(item))

    return result


planets = [
    Corelia,
    Coruscant,
    Mustafar,
    Bracca,
    Felucia,
    Geonosis,
    Dathomir,
    Kashyyyk,
    Tatooine,
    MedicalStation,
    Kessel
    ]

def main():
    result = get_player_units_for_platoons('Ifa n sc')
    with open('output/output2.txt', 'w') as out:
        for item in result:
            out.write(f'{item[0]}: {item[1]}\n')
    

    '''
    names = []

    with open('db/names.txt', 'r') as file:
        for line in file.readlines():
            names.append(line[:len(line) - 1])

    cnt_ready_units = {}

    for name in names:
        cnt_ready_units[name] = 0

    for key in cnt_ready_units.keys():
        ready_units = 0
        for planet in planets:
            ready_units += cnt_ready_units_for_planet(key, planet)
        cnt_ready_units[key] = ready_units

    cnt_ready_units = dict(sorted(cnt_ready_units.items(), key=lambda item: item[1]))

    with open('output/output.txt', 'w') as out:
        for key in cnt_ready_units.keys():
            out.write(f'{key}: {cnt_ready_units[key]}\n')
    '''

if __name__ == '__main__':
    main()


'''total_phase_5_6 = phase_total([MedicalStation, Kessel, Kashyyyk])

total = phase_total([
    Corelia,
    Coruscant,
    Mustafar,
    Bracca,
    Felucia,
    Geonosis,
    Dathomir,
    Kashyyyk,
    Tatooine,
    MedicalStation,
    Kessel
    ])

with open('output/output.txt', 'w') as out:
    for key in total.keys():
        out.write(f'{key}: {total[key]}\n')'''
