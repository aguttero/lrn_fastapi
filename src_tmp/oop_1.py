from OOP.Enemy import *

zombie = Enemy('Zombie', 100, 3)
# zombie.type_of_enemy = 'Zombie'

# print(f'{zombie.__type_of_enemy} has {zombie.health_points} health points and can do attack of {zombie.attack_damage} damage')

print ("- - -")
print(f'{zombie.get_type_of_enemy()} has {zombie.health_points} health points and can do attack of {zombie.attack_damage} damage')

# --- This is the way to 'override' the private attribute
zombie._Enemy__type_of_enemy = "Vampire"

print ("- - -")
print(f'{zombie.get_type_of_enemy()} has {zombie.health_points} health points and can do attack of {zombie.attack_damage} damage')


# zombie.talk()
# zombie.walk_forward()
# zombie.attack()
