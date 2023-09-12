import tkinter as tk
from tkinter import ttk
from collections import deque
import globals
import utils
from floors.tkinter_floor import TkinterFloor
from generators.generator import Generator


class TkinterGenerator(Generator):
    def __init__(self, seed: str, output_file: str, stage_id: int = 2):
        """
        Creates a new generator.
        :param seed: seed for the random generator
        :param output_file: file to save the floor to
        """
        super().__init__(seed, output_file, stage_id)
        self._floors = deque()
        self._current_floor = -1
        self._tk = tk.Tk()
        color = globals.Color.GRAY.value
        hex = utils.rgb2hex(color[0], color[1], color[2])
        self._canvas = tk.Canvas(height=globals.FLOOR_HEIGHT * globals.ROOM_HEIGHT,
                                 width=globals.ROOM_WIDTH * globals.ROOM_WIDTH,
                                 background=hex)

    def _create_floor(self) -> None:
        self._floors.append(TkinterFloor(globals.FLOOR_HEIGHT, globals.FLOOR_WIDTH, canvas=self._canvas))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]
        self._floors[self._current_floor].draw(tk)

    def _decrease_floor(self):
        if self._current_floor > 0:
            self._current_floor -= 1
            self._floors[self._current_floor].draw(tk)

    def _increase_floor(self):
        if self._current_floor < len(self._floors) - 1:
            self._current_floor += 1
            self._floors[self._current_floor].draw(tk)

    def _generate_and_draw_floor(self):
        self.generate()
        self._floors[self._current_floor].draw(tk)

    def run(self):
        self._tk.title("Dungeon Generator")
        self._tk.geometry("1200x600")
        ttk.Label(self._tk, text="Current Floor").pack()
        self.generate()
        self._floors[self._current_floor].draw(tk)
        self._canvas.pack(anchor=tk.NW, expand=True)
        button_frame = tk.Frame(self._tk)
        button_frame.pack()
        button_pre = ttk.Button(button_frame, text="<-", command=self._decrease_floor)
        button_pre.pack(side=tk.LEFT)
        button_gen = ttk.Button(button_frame, text="Generate", command=self.generate)
        button_gen.pack(side=tk.LEFT)
        button_next = ttk.Button(button_frame, text="->", command=self._increase_floor)
        button_next.pack(side=tk.LEFT)
        self._tk.mainloop()