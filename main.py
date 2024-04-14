class Player:
    def __init__(self) -> None:
        self.name = ''
        self.units = []

    def set_name(self, name) -> None:
        self.name = name
    
    def get_name(self) -> str:
        return self.name


player = Player()
player.set_name('Alex')
print(player.get_name())