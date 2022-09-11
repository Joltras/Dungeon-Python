import Globals
from Globals import Color
from floors.PygameFloor import PygameFloor
import pygame
from generators.Generator import Generator
from collections import deque


class PygameGenerator(Generator):
    def __init__(self, seed: str, output_file: str, stage_id: int = 2):
        """
        Creates a new generator.
        :param seed: seed for the random generator
        :param output_file: file to save the floor to
        :param ui: whether to show the floor or not
        """
        super().__init__(seed, output_file, stage_id)
        self.screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.clock = pygame.time.Clock()
        self._floors = deque()
        self._current_floor = -1

    def toJSON(self):
        j = "{\n" + '"seed": "' + self._seed + '",\n' + '"width": ' + str(Globals.width) + ',\n"height": ' + \
            str(Globals.height) + ',\n"floor": ' + self._floors[self._current_floor].to_json() + "\n}"
        return j

    def _create_floor(self):
        self._floors.append(PygameFloor(Globals.height, Globals.width))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]
        return PygameFloor(Globals.height, Globals.width)

    def run(self):
        active: bool = True
        self.generate()
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save()
                    if event.key == pygame.K_LEFT:
                        if self._current_floor > 0:
                            self._current_floor -= 1
                    if event.key == pygame.K_RIGHT:
                        if self._current_floor < len(self._floors) - 1:
                            self._current_floor += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.generate()
            self.screen.fill(Color.WHITE.value)
            self._floors[self._current_floor].draw(self.screen)
            pygame.display.flip()
            self.clock.tick(5)
