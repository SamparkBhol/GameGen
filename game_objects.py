from OpenGL.GL import *
from OpenGL.GLU import *
import random
from pygame.math import Vector3

def render_cube(size):
    glBegin(GL_QUADS)
    # Front face
    glNormal3f(0, 0, 1)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Back face
    glNormal3f(0, 0, -1)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, -size, -size)
    # Top face
    glNormal3f(0, 1, 0)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    # Bottom face
    glNormal3f(0, -1, 0)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)
    # Right face
    glNormal3f(1, 0, 0)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)
    # Left face
    glNormal3f(-1, 0, 0)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)
    glEnd()

def render_ground(size):
    glColor3f(0.2, 0.8, 0.2)  # Green color for ground
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-size/2, 0, -size/2)
    glVertex3f(-size/2, 0, size/2)
    glVertex3f(size/2, 0, size/2)
    glVertex3f(size/2, 0, -size/2)
    glEnd()

def render_skybox():
    glDisable(GL_LIGHTING)
    glColor3f(0.5, 0.7, 1.0)  # Light blue color for sky
    glBegin(GL_QUADS)
    # Front
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    # Back
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    # Left
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    # Right
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    # Top
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glEnd()
    glEnable(GL_LIGHTING)

class GameObject:
    def __init__(self, position):
        self.position = position

    def update(self, player):
        pass

    def render(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        self.draw()
        glPopMatrix()

    def draw(self):
        pass

class Tree(GameObject):
    def draw(self):
        glColor3f(0.5, 0.35, 0.05)  # Brown for trunk
        glPushMatrix()
        glScalef(0.1, 1, 0.1)
        render_cube(1)
        glPopMatrix()

        glColor3f(0, 0.8, 0)  # Green for leaves
        glPushMatrix()
        glTranslatef(0, 1, 0)
        glScalef(0.5, 0.5, 0.5)
        render_cube(1)
        glPopMatrix()

class Rock(GameObject):
    def draw(self):
        glColor3f(0.5, 0.5, 0.5)  # Gray for rock
        glPushMatrix()
        glScalef(0.3, 0.3, 0.3)
        render_cube(1)
        glPopMatrix()

class Chest(GameObject):
    def __init__(self, position):
        super().__init__(position)
        self.is_open = False
        self.contents = ["Gold", "Health Potion", "Magic Scroll"]

    def draw(self):
        glColor3f(0.6, 0.4, 0.2)  # Brown for chest
        glPushMatrix()
        glScalef(0.4, 0.3, 0.3)
        render_cube(1)
        glPopMatrix()

        if self.is_open:
            glColor3f(1, 1, 0)  # Yellow for open lid
            glPushMatrix()
            glTranslatef(0, 0.3, -0.15)
            glRotatef(-90, 1, 0, 0)
            glScalef(0.4, 0.05, 0.3)
            render_cube(1)
            glPopMatrix()

    def interact(self, player):
        if not self.is_open:
            self.is_open = True
            print("You open the chest and find:")
            for item in self.contents:
                print(f"- {item}")
                player.add_to_inventory(item)
            self.contents = []
        else:
            print("The chest is empty.")

class NPC(GameObject):
    def __init__(self, position, npc_type):
        super().__init__(position)
        self.npc_type = npc_type
        self.dialogue = self.generate_dialogue()

    def draw(self):
        if self.npc_type == 'villager':
            glColor3f(0.8, 0.6, 0.4)
        elif self.npc_type == 'merchant':
            glColor3f(0.4, 0.4, 0.8)
        elif self.npc_type == 'guard':
            glColor3f(0.8, 0.2, 0.2)
        
        glPushMatrix()
        glScalef(0.2, 0.5, 0.2)
        render_cube(1)
        glPopMatrix()

    def generate_dialogue(self):
        if self.npc_type == 'villager':
            return ["Hello, traveler!", "Beautiful day, isn't it?", "Be careful in the woods!"]
        elif self.npc_type == 'merchant':
            return ["Want to buy something?", "I have the best goods in town!", "Everything must go!"]
        elif self.npc_type == 'guard':
            return ["Move along, citizen.", "Everything's under control.", "Report any suspicious activity."]
        return ["..."]

    def interact(self, player):
        print(f"{self.npc_type.capitalize()} says: {random.choice(self.dialogue)}")
        if self.npc_type == 'merchant':
            self.trade(player)

    def trade(self, player):
        items_for_sale = ["Health Potion", "Stamina Potion", "Magic Scroll"]
        prices = {"Health Potion": 50, "Stamina Potion": 40, "Magic Scroll": 100}
        
        print("Items for sale:")
        for item, price in prices.items():
            print(f"- {item}: {price} gold")
        
        choice = input("What would you like to buy? (or 'nothing'): ")
        if choice in items_for_sale:
            if player.spend_gold(prices[choice]):
                player.add_to_inventory(choice)
                print(f"You bought a {choice}!")
            else:
                print("Not enough gold!")
        elif choice.lower() != 'nothing':
            print("Invalid choice.")