class Enemy:

    # _type_of_enemy: str
    # health_points: int = 10
    # attack_damage: int = 1

    # def __init__(self) -> None:
    #     pass

    def __init__(self, type_of_enemy, health_points = 10, attack_damage = 1):
       self._type_of_enemy = type_of_enemy
       self.health_points = health_points
       self.attack_damage = attack_damage
       print(f'New {self._type_of_enemy} enemy instance created')


    def talk(self):
        print(f"I am a {self._type_of_enemy}. Be prepared to fight!")
        return "done!"

    def walk_forward(self):
        print(f"{self._type_of_enemy} moves closer to you")

    def attack(self):
        print(f"{self._type_of_enemy} attacks for {self.attack_damage} damage")

    def health_check(self):
        print(f"{self.health_points} health points remaining")
