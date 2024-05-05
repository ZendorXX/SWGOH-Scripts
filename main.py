def load_data(planet_name: str) -> dict:
    platoon = {}

    with open(f'platoons/{planet_name}.txt', 'r') as file:
        for line in file.readlines():
            unit, count = line.split('\t')
            platoon[unit] = int(count)

    return platoon

def phase_total(planet_list: list[dict]) -> dict:
    total = {}

    for planet in planet_list:
        for unit in planet.keys():
            if unit not in total:
                total[unit] = planet[unit]
                continue
            
            total[unit] += planet[unit]

    return dict(sorted(total.items(), key=lambda item: (-item[1], item[0])))

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


total_phase_5_6 = phase_total([MedicalStation, Kessel, Kashyyyk])

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
        out.write(f'{key}: {total[key]}\n')
