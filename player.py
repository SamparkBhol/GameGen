import pygame
from pygame.math import Vector3
import math

class Player:
    def __init__(self, position):
        self.position = position
        self.rotation = Vector3(0, 0, 0)
        self.speed = 0.1
        self.mouse_sensitivity = 0.1
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.inventory = []
        self.current_weapon = None
        self.skills = {
            'sword': 1,
            'magic': 1,
            'alchemy': 1
        }
        self.experience = 0
        self.level = 1
        self.gold = 0

    def update(self, keys, world):
        self.handle_movement(keys)
        self.handle_mouse()
        self.regenerate_stamina()
        self.check_level_up()

    def handle_movement(self, keys):
        move_vector = Vector3(0, 0, 0)
        if keys[pygame.K_w]:
            move_vector.z -= 1
        if keys[pygame.K_s]:
            move_vector.z += 1
        if keys[pygame.K_a]:
            move_vector.x -= 1
        if keys[pygame.K_d]:
            move_vector.x += 1

        if move_vector.length() > 0:
            move_vector.normalize_ip()
            move_vector *= self.speed

            # Apply rotation to movement
            rotated_move = Vector3(
                move_vector.x * math.cos(math.radians(self.rotation.y)) - move_vector.z * math.sin(math.radians(self.rotation.y)),
                move_vector.y,
                move_vector.x * math.sin(math.radians(self.rotation.y)) + move_vector.z * math.cos(math.radians(self.rotation.y))
            )

            self.position += rotated_move

    def handle_mouse(self):
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        self.rotation.y -= mouse_dx * self.mouse_sensitivity
        self.rotation.x -= mouse_dy * self.mouse_sensitivity
        self.rotation.x = max(-90, min(90, self.rotation.x))

    def attack(self, world):
        if self.stamina >= 10:
            self.stamina -= 10
            # Check for nearby enemies and apply damage
            for npc in world.get_nearby_npcs(self.position, 2):
                # Apply damage based on weapon and skills
                damage = 10 * self.skills['sword']
                if self.current_weapon:
                    damage *= self.current_weapon.damage_multiplier
                # Apply damage to NPC (not implemented in this example)
                print(f"Dealt {damage} damage to {npc.npc_type}")
                self.gain_experience(5)  # Gain experience for successful hit

    def block(self):
        if self.stamina >= 5:
            self.stamina -= 5
            # Implement blocking logic (e.g., reduce incoming damage for a short duration)
            print("Blocking incoming attacks")

    def regenerate_stamina(self):
        self.stamina = min(self.max_stamina, self.stamina + 0.1)

    def use_item(self, item):
        if item in self.inventory:
            if item == 'Health Potion':
                self.heal(20)
            elif item == 'Stamina Potion':
                self.restore_stamina(30)
            elif item == 'Magic Scroll':
                self.gain_experience(50)
            self.inventory.remove(item)

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        print(f"Healed for {amount}. Current health: {self.health}")

    def restore_stamina(self, amount):
        self.stamina = min(self.max_stamina, self.stamina + amount)
        print(f"Restored {amount} stamina. Current stamina: {self.stamina}")

    def take_damage(self, amount):
        self.health -= amount
        print(f"Took {amount} damage. Current health: {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print("Game Over")
        # Implement game over logic here

    def level_up_skill(self, skill):
        if skill in self.skills:
            self.skills[skill] += 1
            print(f"Leveled up {skill}. New level: {self.skills[skill]}")

    def equip_weapon(self, weapon):
        self.current_weapon = weapon
        print(f"Equipped {weapon.name}")

    def cast_spell(self, spell, world):
        if spell == 'fireball' and self.skills['magic'] >= 2:
            if self.stamina >= 20:
                self.stamina -= 20
                # Implement fireball spell
                print("Cast Fireball spell!")
                self.gain_experience(10)
            else:
                print("Not enough stamina to cast Fireball")
        elif spell == 'heal' and self.skills['magic'] >= 3:
            if self.stamina >= 30:
                self.stamina -= 30
                self.heal(30)
                print("Cast Heal spell!")
                self.gain_experience(15)
            else:
                print("Not enough stamina to cast Heal")
        else:
            print("Cannot cast spell")

    def craft_potion(self, potion_type):
        if self.skills['alchemy'] >= 2:
            # Check if player has necessary ingredients (not implemented in this example)
            self.inventory.append(potion_type)
            print(f"Crafted {potion_type}")
            self.gain_experience(5)
        else:
            print("Alchemy skill too low to craft potions")

    def gain_experience(self, amount):
        self.experience += amount
        print(f"Gained {amount} experience. Total experience: {self.experience}")
        self.check_level_up()

    def check_level_up(self):
        experience_needed = self.level * 100  # Simple level up formula
        if self.experience >= experience_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= (self.level - 1) * 100  # Subtract experience needed for previous level
        self.max_health += 10
        self.max_stamina += 5
        self.health = self.max_health
        self.stamina = self.max_stamina
        print(f"Leveled up! New level: {self.level}")
        print("You can now upgrade a skill. Choose 'sword', 'magic', or 'alchemy'.")
        # In a real game, you'd implement a way for the player to choose which skill to upgrade

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"Added {item} to inventory")

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"Removed {item} from inventory")
        else:
            print(f"{item} not in inventory")

    def show_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(f"- {item}")

    def earn_gold(self, amount):
        self.gold += amount
        print(f"Earned {amount} gold. Total gold: {self.gold}")

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            print(f"Spent {amount} gold. Remaining gold: {self.gold}")
            return True
        else:
            print(f"Not enough gold. Current gold: {self.gold}")
            return False

    def get_status(self):
        return f"""
        Level: {self.level}
        Health: {self.health}/{self.max_health}
        Stamina: {self.stamina}/{self.max_stamina}
        Experience: {self.experience}
        Gold: {self.gold}
        Skills:
          Sword: {self.skills['sword']}
          Magic: {self.skills['magic']}
          Alchemy: {self.skills['alchemy']}
        """

    def interact(self, world):
        nearby_objects = world.get_nearby_objects(self.position, 2)
        nearby_npcs = world.get_nearby_npcs(self.position, 2)
        
        if nearby_objects:
            for obj in nearby_objects:
                if hasattr(obj, 'interact'):
                    obj.interact(self)
                    break
        elif nearby_npcs:
            for npc in nearby_npcs:
                npc.interact(self)
                break
        else:
            print("Nothing to interact with nearby.")

# Weapon class to be used with Player
class Weapon:
    def __init__(self, name, damage_multiplier):
        self.name = name
        self.damage_multiplier = damage_multiplier

# Example usage:
# sword = Weapon("Iron Sword", 1.2)
# player.equip_weapon(sword)