import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from collections import deque
import globals
import utils
from floors.tkinter_floor import TkinterFloor
from generators.generator import Generator


class TkinterGenerator(Generator):
    def __init__(self, seed: str, output_file_name: str, output_file_path: str, stage_id: int = 2):
        """
        Creates a new generator.
        @param output_file_name: Name for the output file
        @param output_file_path: Path for the output file
        @param stage_id: ID for the stage
        @param seed: seed for the random generator

        """
        super().__init__(seed, output_file_name, output_file_path, stage_id)
        self._floors = deque()
        self._current_floor = -1
        self._tk = tk.Tk()
        color = globals.Color.GRAY.value
        hex_color = utils.rgb2hex(color[0], color[1], color[2])
        self._canvas = tk.Canvas(height=globals.FLOOR_HEIGHT * globals.ROOM_HEIGHT,
                                 width=globals.ROOM_WIDTH * globals.ROOM_WIDTH,
                                 background=hex_color)

    def _create_floor(self) -> None:
        """
        Creates a new TkinterFloor and appends it to the floor queue.
        """
        self._floors.append(TkinterFloor(globals.FLOOR_HEIGHT, globals.FLOOR_WIDTH, canvas=self._canvas))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]
        self._floors[self._current_floor].draw(tk)

    def _decrease_floor(self) -> None:
        """
        Lowers the index of the current floor.
        """
        if self._current_floor > 0:
            self._current_floor -= 1
            self._floors[self._current_floor].draw(tk)

    def _increase_floor(self) -> None:
        """
        Increases the index of the current floor.
        """
        if self._current_floor < len(self._floors) - 1:
            self._current_floor += 1
            self._floors[self._current_floor].draw(tk)

    def _generate_and_draw_floor(self) -> None:
        """
        Cals the generate method and the draw method of the floor.
        """
        self.generate()
        self._floors[self._current_floor].draw(tk)

    def save(self, path: str = "") -> str:
        """
        Shows a dialog for saving the floor to a file.
        @param path: Optional path
        @return: Path the floor has been saved to
        """
        options = {
            'defaultextension': globals.JSON_SUFFIX,
            'filetypes': [('Json', globals.JSON_SUFFIX)],
            'initialdir': self._output_file_path,
            'initialfile': "floor.json",
            'title': 'Datei speichern unter'
        }
        file_path = filedialog.asksaveasfilename(**options)
        print(file_path)
        return super().save(file_path)

    def run(self) -> None:
        """
        Sets up the ui elements and starts the main loop of the application.
        """
        self._tk.title("Dungeon Generator")
        self._tk.geometry("1200x600")
        name = tk.StringVar()
        name.set(globals.DEFAULT_FLOOR_NAME)
        ttk.Label(self._tk, text="Current Floor: " + name.get()).pack()
        self.generate()
        self._floors[self._current_floor].draw(tk)
        self._canvas.pack(anchor=tk.NW, expand=True)
        button_frame = tk.Frame(self._tk)
        button_frame.pack(pady=(0, 10))
        button_pre = ttk.Button(button_frame, text="<-", command=self._decrease_floor)
        button_pre.pack(side=tk.LEFT)
        button_gen = ttk.Button(button_frame, text="Generate", command=self._generate_and_draw_floor)
        button_gen.pack(side=tk.LEFT)
        button_next = ttk.Button(button_frame, text="->", command=self._increase_floor)
        button_next.pack(side=tk.LEFT)
        button_save = ttk.Button(button_frame, text="Save As", command=self.save)
        button_save.pack(side=tk.RIGHT, padx=(100, 0))
        self._tk.mainloop()
