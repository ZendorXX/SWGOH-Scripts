with open('db/platoon_total.txt') as file:
    text = file.readlines()
    platoon_total = {}
    for line in text:
        key, value = list(line.split(':'))
        platoon_total[key] = int(value)

with open('input/input.txt') as file:
    for line in file.readlines():
        if line[len(line) - 1] == '\n':
            line = line[:len(line) - 1]
        print(platoon_total[line])