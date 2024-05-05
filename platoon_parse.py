with open('input/input.txt', 'r') as f:
    text = f.read()

data = text.split('\n')

parsed = {}

for i in range(0, len(data), 2):
    parsed[data[i]] = data[i + 1] 

with open('output/output.txt', 'w') as out:
    for key in parsed.keys():
        out.write(f'{key}\t {parsed[key]}\n')