with open('input/check.txt') as file:
    text = file.readlines()

parsed = []
for line in text:
    parsed.append(list(line.split()))

characters = {}
ships = {}
for item in parsed:
    key = ''
    for i in range(0, len(item) - 1):
        key += item[i] + ' '
    if len(item[len(item) - 1]) > 1:
        ships[key] = item[len(item) - 1]
    else:
        characters[key] = int(item[len(item) - 1])

characters = dict(sorted(characters.items(), key=lambda item: item[1]))

with open('output/output.txt', 'w') as file:
    for key in characters.keys():
        file.write(f'{key}: {characters[key]}\n')

    for key in ships.keys():
        file.write(f'{key}: {ships[key]}\n')