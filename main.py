import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from game_world import GameWorld
from player import Player
from game_objects import render_skybox

class Game:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("3D RPG Game")
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))

        self.clock = pygame.time.Clock()
        self.world = GameWorld()
        self.player = Player(Vector3(0, 1, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_e:
                    self.player.interact(self.world)
                elif event.key == pygame.K_i:
                    self.player.show_inventory()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.player.attack(self.world)
                elif event.button == 3:  # Right click
                    self.player.block()
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.world)
        self.world.update(self.player)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Apply player's view transformation
        glRotatef(self.player.rotation.x, 1, 0, 0)
        glRotatef(self.player.rotation.y, 0, 1, 0)
        glTranslatef(-self.player.position.x, -self.player.position.y, -self.player.position.z)

        # Render skybox
        render_skybox()

        # Render game world
        self.world.render()

        pygame.display.flip()

    def run(self):
        while self.handle_events():
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()