import globals
from globals import Color
from floors.pygame_floor import PygameFloor
import pygame
from generators.generator import Generator
from collections import deque


class PygameGenerator(Generator):
    """
    Pygame version of the generator.
    """

    def __init__(self, seed: str, output_file_name: str, output_file_path: str, stage_id: int = 2):
        """
        Creates a new generator.
        @param seed: seed for the random generator
        @param output_file_name: Name for the output file
        @param output_file_path: Path for the output file
        @param stage_id: ID for the stage

        """
        super().__init__(seed, output_file_name, output_file_path, stage_id)
        self.screen = pygame.display.set_mode((globals.window_width, globals.window_height))
        self.clock = pygame.time.Clock()
        self._floors = deque()
        self._current_floor = -1

    def get_floors(self) -> deque:
        """
        Returns all floors that have been generated.
        @return: queue with all floors
        """
        return self._floors

    def _create_floor(self) -> None:
        """
        Creates a new pygame floor.
        """
        self._floors.append(PygameFloor(globals.FLOOR_HEIGHT, globals.FLOOR_WIDTH))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]

    def run(self) -> None:
        """
        Reacts to user input.
        """
        active: bool = True
        self.generate()
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.KEYDOWN:
                    self._key_down(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.generate()
            self.screen.fill(Color.WHITE.value)
            self._floors[self._current_floor].draw(self.screen)
            pygame.display.flip()
            self.clock.tick(5)

    def _key_down(self, event) -> None:
        """
        Checks which key was pressed and reacts to it.
        @param event:
        """
        if event.key == pygame.K_s:
            self.save()
        if event.key == pygame.K_LEFT and self._current_floor > 0:
            self._current_floor -= 1
        if event.key == pygame.K_RIGHT and self._current_floor < len(self._floors) - 1:
            self._current_floor += 1
