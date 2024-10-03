import random
from OpenGL.GL import *
from pygame.math import Vector3
from game_objects import Tree, Rock, Chest, NPC, render_ground

class GameWorld:
    def __init__(self):
        self.terrain_size = 100
        self.objects = self.generate_objects()
        self.npcs = self.generate_npcs()

    def generate_objects(self):
        objects = []
        for _ in range(50):
            x = random.uniform(-self.terrain_size/2, self.terrain_size/2)
            z = random.uniform(-self.terrain_size/2, self.terrain_size/2)
            y = 0  # Assume flat terrain for simplicity
            obj_type = random.choice([Tree, Rock, Chest])
            objects.append(obj_type(Vector3(x, y, z)))
        return objects

    def generate_npcs(self):
        npcs = []
        for _ in range(10):
            x = random.uniform(-self.terrain_size/2, self.terrain_size/2)
            z = random.uniform(-self.terrain_size/2, self.terrain_size/2)
            y = 0  # Assume flat terrain for simplicity
            npc_type = random.choice(['villager', 'merchant', 'guard'])
            npcs.append(NPC(Vector3(x, y, z), npc_type))
        return npcs

    def update(self, player):
        for obj in self.objects:
            obj.update(player)
        for npc in self.npcs:
            npc.update(player)

    def render(self):
        render_ground(self.terrain_size)
        for obj in self.objects:
            obj.render()
        for npc in self.npcs:
            npc.render()

    def get_nearby_objects(self, position, radius):
        return [obj for obj in self.objects if (obj.position - position).length() < radius]

    def get_nearby_npcs(self, position, radius):
        return [npc for npc in self.npcs if (npc.position - position).length() < radius]