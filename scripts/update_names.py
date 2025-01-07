from get_name import get_player_name

def update_names_file(allycodes_file: str, names_file: str):
    """Обновляет файл db/names.txt, используя allycodes из db/allycodes.txt."""
    with open(allycodes_file, 'r', encoding='utf-8') as file:
        allycodes = file.read().splitlines()

    names = []
    for allycode in allycodes:
        name = get_player_name(allycode)
        if name and name != "Имя игрока не найдено":
            names.append(name)

    with open(names_file, 'w', encoding='utf-8') as file:
        for name in names:
            file.write(f"{name}\n")

def main():
    update_names_file('db/allycodes.txt', 'db/names.txt')

if __name__ == '__main__':
    main()