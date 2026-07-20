class Enemy:

    # _type_of_enemy: str
    # health_points: int = 10
    # attack_damage: int = 1

    # def __init__(self) -> None:
    #     pass

    def __init__(self, type_of_enemy, health_points = 10, attack_damage = 1):
       self.__type_of_enemy = type_of_enemy # double underscore -> Private Encapsulation
       self.health_points = health_points
       self.attack_damage = attack_damage
       print(f'New {self.__type_of_enemy} enemy instance created')

    def get_type_of_enemy(self):
        return self.__type_of_enemy

    def set_type_of_enemy(self, type_of_enemy):
        self.__type_of_enemy = type_of_enemy

    def talk(self):
        print(f"I am a {self.__type_of_enemy}. Be prepared to fight!")
        return "done!"

    def walk_forward(self):
        print(f"{self.__type_of_enemy} moves closer to you")

    def attack(self):
        print(f"{self.__type_of_enemy} attacks for {self.attack_damage} damage")

    def health_check(self):
        print(f"{self.health_points} health points remaining")
