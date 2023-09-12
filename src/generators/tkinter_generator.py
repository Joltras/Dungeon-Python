import tkinter as tk
from collections import deque
import globals
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

    def _create_floor(self) -> None:
        self._floors.append(TkinterFloor(globals.FLOOR_HEIGHT * globals.ROOM_HEIGHT, globals.FLOOR_WIDTH * globals.ROOM_WIDTH))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]

    def run(self):
        self._tk.title("Dungeon Generator")
        self._tk.geometry("1000x500")
        tk.Label(self._tk, text="Current Floor").pack()
        self.generate()
        self._floors[self._current_floor].draw(tk)
        button_pre = tk.Button(text="<-")
        button_pre.pack(side=tk.LEFT)
        self._tk.mainloop()