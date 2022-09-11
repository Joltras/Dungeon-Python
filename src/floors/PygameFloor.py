import pygame
import Globals as Globals
from Globals import Color, RoomType
from floors.Floor import Floor
from rooms.PygameNormalRoom import PygameNormalRoom
from rooms.PygameTeleportRoom import PygameTeleportRoom
from rooms.Room import Room


class PygameFloor(Floor):
    """
    A pygame version of the floor.
    """

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

    def to_json(self):
        """
        Creates a json string for the current room object.
        :return: json string
        """
        current_index: int = 0
        max_index: int = len(self._rooms)
        json_string = "{\n\"rooms\": ["
        for room in self._rooms:
            if current_index < max_index - 1:
                json_string += room.to_json() + ","
            else:
                json_string += room.to_json()

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

    def add_room(self, x: int, y: int, room_type=RoomType.NORMAL_ROOM):
        """
        Creates and adds a room to the floor.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :param room_type: type of the room (default = normal room)
        """
        self.add_to_floor_grid(x, y)
        self._rooms.append(PygameNormalRoom(x=x, y=y, room_type=room_type, room_id=self._room_id))
        self._room_id += 1

    def add_teleport_room(self, room: Room) -> None:
        """
        Creates and adds a new Teleport room to the floor.
        New teleport room is placed at the location from the given room.
        :param room: Room which is connected to the teleport room.
        """
        t_room = PygameTeleportRoom(x=room.get_x(), y=room.get_y(), room_id=self._room_id,
                                    room_type=RoomType.BOSS_TELEPORT_ROOM, teleport_room_id=room.get_id())
        self._rooms.append(t_room)
        self._room_id += 1








