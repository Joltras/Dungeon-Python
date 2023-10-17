from globals import RoomType
import globals
from rooms.room import Room
import tkinter as tk
import utils


class TkinterRoom(Room):
    def __init__(self, x: int, y: int, room_id: int, room_type: RoomType, width=globals.ROOM_WIDTH,
                 height=globals.ROOM_HEIGHT, ):
        super().__init__(x, y, room_id, room_type)
        self._width = width
        self._height = height

    def draw(self, canvas: tk.Canvas):
        x0 = self._x * globals.ROOM_WIDTH
        y0 = self._y * globals.ROOM_HEIGHT
        x1 = x0 + self._width
        y1 = y0 + self._height
        color = globals.Room_Colors[self._type].value
        hex_color = utils.rgb2hex(color[0], color[1], color[2])
        canvas.create_rectangle((x0, y0), (x1, y1), fill=hex_color)

    @classmethod
    def from_room(cls, room: Room):
        return TkinterRoom(room._x, room._y, room._id, room._type)