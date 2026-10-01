class Character:
    def __init__(self, name, health, straight):
        self.name = name
        self.health = health
        self.straight = straight
    def __str__(self):
        return f'{self.name}, {self.health}, {self.straight}'
    def __bool__(self):
        return self.health > 0
    def __add__(self, other : Character):
        return [self, other]
    def __lt__(self, other : Character):
        return self.straight < other.straight
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return NotImplemented
        return self.straight == other.straight and self.health == other.health and self.name == other.name
    def __len__(self):
        return self.health
    def give_damage(self, other: Character):
        print('Attack!')
    def take_damage(self, damage):
        print('Take damage!')

class Warrior(Character):
    def give_damage(self, other: Character):
        other.health -= 10
    def take_damage(self, damage):
        self.health -= damage/2
class Mage(Character):
    def give_damage(self, other: Character):
        other.health -= 20
    def take_damage(self, damage):
        self.health -= damage*2

class Archer(Character):
    def give_damage(self, other: Character):
        other.health -= 40
    def take_damage(self, damage):
        self.health -= damage*3

warrior = Warrior("Conan", 100, 30)
mage = Mage("Merlin", 80, 20)
archer = Archer("Robin", 70, 25)

print(warrior)
print(mage)
print(archer)

print(bool(warrior))  # True

warrior.health = 0

print(bool(warrior))  # False

warrior.health = 100

print(len(warrior))  # 100
print(len(mage))     # 80

print(warrior < mage)   # False (30 < 20)
print(mage < warrior)   # True  (20 < 30)

warrior2 = Warrior("Conan", 100, 30)

print(warrior == warrior2)  # True
print(warrior == mage)      # False

team = warrior + mage

print(len(team))

print("Mage health before:", mage.health)

warrior.give_damage(mage)

print("Mage health after:", mage.health)

characters = [
    warrior,
    mage,
    archer
]

for character in characters:
    print(f"{character.name} attacks Mage")
    character.give_damage(mage)

print("Mage health:", mage.health)

print("Archer health before:", archer.health)
archer.take_damage(10)
print("Archer health after:", archer.health)

mage.health = 0

if mage:
    print("Mage is alive")
else:
    print("Mage is dead")

