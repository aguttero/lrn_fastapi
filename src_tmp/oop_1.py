from OOP.Enemy import *

zombie = Enemy('Zombie')
# zombie.type_of_enemy = 'Zombie'

print(f'{zombie._type_of_enemy} has {zombie.health_points} health points and can do attack of {zombie.attack_damage}')

# zombie.talk()
# zombie.walk_forward()
# zombie.attack()
