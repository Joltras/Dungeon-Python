import pygame
import Globals as Globals
from Globals import Color
from floors.Floor import Floor


class PygameFloor(Floor):

    def __init__(self, height: int, width: int):
        """
        Creates a new floor width the given width and height.
        :param height: height of the floor
        :param width: width of the floor
        """
        super().__init__(height, width)
        self._rect = pygame.Rect(Globals.floor_plan_coordinates[1], Globals.floor_plan_coordinates[0],
                                 width * Globals.room_width, height * Globals.room_height)

    def __getstate__(self):
        state = dict(self.__dict__)
        del state['_rect']
        del state['_floor_grid']
        del state['_room_id']
        return state

    def toJSON(self):
        """
        Creates a json string for the current room object.
        :return: json string
        """
        current_index: int = 0
        max_index: int = len(self._rooms)
        json_string = "{\n\"rooms\": ["
        for room in self._rooms:
            if current_index < max_index - 1:
                json_string += room.toJSON() + ","
            else:
                json_string += room.toJSON()

            current_index += 1
        return json_string + "]\n}"

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the floor with all the rooms on the screen.
        :param screen: screen to draw on
        """
        for room in self._rooms:
            room.draw(screen)
        for room in self._rooms:
            room.draw_doors(screen)
        pygame.draw.rect(screen, Color.DARK_GRAY.value, self._rect, 2)








