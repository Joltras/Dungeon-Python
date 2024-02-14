import threading
import time

import globals
from floors.floor import Floor
from rooms.room import Room

from rooms.tkinter.tkinter_room import TkinterRoom
from rooms.tkinter.tkinter_teleport_room import TkinterTeleportRoom


class TkinterFloor(Floor):
    def __init__(self, height: int, width: int, canvas, name: str, seed: str):
        """
        Creates a new floor width the given width and height.
        @param height: height of the floor
        @param width: width of the floor
        """
        super().__init__(height, width, seed)
        self._canvas = canvas
        self._first_draw = True
        self.name = name
        self._is_drawing = False

    def add_room(self, x: int, y: int, type=globals.RoomType.NORMAL_ROOM):
        self.add_to_floor_grid(x, y)
        self._rooms.append(TkinterRoom(x=x, y=y, room_type=type, room_id=self._room_id))
        self._room_id += 1

    def add_teleport_room(self, room: Room) -> None:
        t_room = TkinterTeleportRoom(x=room[0], y=room[1], room_id=self._room_id, teleport_room_id=room.get_id())
        self._rooms.append(t_room)
        self._room_id += 1

    @classmethod
    def from_floor(cls, floor: Floor, canvas, name: str):
        """
        Creates a new TkinterFloor from a floor.
        @param canvas: Canvas to draw on
        @param floor: floor to copy
        @param name: name of the floor
        @return: new TkinterFloor
        """
        tkinter_floor = TkinterFloor(floor._height, floor._width, canvas, name)
        for room in floor._rooms:
            tkinter_floor._rooms.append(TkinterRoom.from_room(room))
        return tkinter_floor

    def draw(self) -> None:
        """
        """
        self.stop_drawing()
        self._canvas.delete("all")
        for room in self._rooms:
            room.draw(self._canvas)

    def draw_thread(self, root) -> None:
        thread = threading.Thread(target=self.draw_step_by_step)
        thread.start()
        print(thread.ident)

    def stop_drawing(self) -> None:
        self._is_drawing = False

    def draw_step_by_step(self) -> None:
        """
        Draws the floor step by step.
        """
        self._canvas.delete("all")
        sorted_rooms = sorted(self._rooms, key=lambda room: room.get_id())
        self._is_drawing = True
        for room in sorted_rooms:
            if not self._is_drawing:
                sorted_rooms.clear()
                return
            room.draw(self._canvas)
            time.sleep(0.5)
