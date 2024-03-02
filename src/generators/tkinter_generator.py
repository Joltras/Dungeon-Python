"""
Module for the TkinterGenerator class.
"""

import os
import secrets
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from collections import deque
from utils import utils, globals as my_globals
from floors.floor import Floor
from floors.tkinter_floor import TkinterFloor
from generators.generator import Generator


class TkinterGenerator(Generator):
    """
    Tkinter version of the generator.
    """
    def __init__(
        self, seed: str, output_file_name: str, output_file_path: str, stage_id: int = 2
    ):
        """
        Creates a new generator.
        @param output_file_name: Name for the output file
        @param output_file_path: Path for the output file
        @param stage_id: ID for the stage
        @param seed: seed for the random generator

        """
        super().__init__(seed, output_file_name, output_file_path, stage_id)
        self._floors = deque()
        self._current_floor_index = -1
        self._tk = tk.Tk()
        color = my_globals.Color.LIGHT_GRAY.value
        hex_color = utils.rgb2hex(color[0], color[1], color[2])
        self._canvas = tk.Canvas(
            height=my_globals.FLOOR_HEIGHT * my_globals.ROOM_HEIGHT,
            width=my_globals.ROOM_WIDTH * my_globals.ROOM_WIDTH,
            background=hex_color,
        )
        self._path = tk.StringVar()
        self._path.set(self._output_file_path)
        self._name = tk.StringVar()
        self._seed_var = tk.StringVar()
        self._seed_var.set(self._seed)
        self._next_seed = tk.StringVar()
        self._next_seed.set(secrets.token_hex(16))
        self._name.set(self._output_file_name)
        self._menu_bar = tk.Menu(self._tk)
        self._current_theme = "light"
        self.apply_theme()

    def apply_theme(self) -> None:
        """
        Applies the current theme to the application.
        """
        if self._current_theme == "light":
            self._set_light_theme()
        else:
            self._set_dark_theme()

    def _set_light_theme(self) -> None:
        self._tk.configure(background="light gray", highlightbackground="black")
        style = ttk.Style(self._tk)
        style.configure(
            "TButton", background="white", foreground="black", hover="black"
        )
        style.configure("TFrame", background="light gray", foreground="black")
        style.theme_use("default")
        self._canvas.configure(background="white", highlightbackground="black")

    def _set_dark_theme(self) -> None:
        self._tk.configure(background="dark gray", highlightbackground="white")
        self._canvas.configure(background="black", highlightbackground="white")
        style = ttk.Style(self._tk)
        style.configure("TFrame", background="dark gray", foreground="white")
        style.configure("TButton", background="black", foreground="white")
        # set color on hover
        style.map("TButton", background=[("active", "gray")])

    def switch_theme(self) -> None:
        """
        Switches the theme of the application.
        """
        if self._current_theme == "light":
            self._current_theme = "dark"
        else:
            self._current_theme = "light"
        self.apply_theme()

    def _create_floor(self) -> None:
        """
        Creates a new TkinterFloor and appends it to the floor queue.
        """
        self._floors.append(
            TkinterFloor(
                my_globals.FLOOR_HEIGHT,
                my_globals.FLOOR_WIDTH,
                canvas=self._canvas,
                name=my_globals.DEFAULT_FLOOR_NAME + my_globals.JSON_SUFFIX,
                seed=self._next_seed.get(),
            )
        )
        self._current_floor_index = len(self._floors) - 1
        self._floor = self._floors[self._current_floor_index]
        self._name.set(self._floors[self._current_floor_index].name)

    def _decrease_floor(self) -> None:
        """
        Lowers the index of the current floor.
        """
        if self._current_floor_index > 0:
            self._floor.stop_drawing()
            self._current_floor_index -= 1
            self._floors[self._current_floor_index].draw()
            self._floor = self._floors[self._current_floor_index]
            self._name.set(self._floors[self._current_floor_index].name)
            self._seed_var.set(self._floor.seed)

    def _increase_floor(self) -> None:
        """
        Increases the index of the current floor.
        """
        last_floor = len(self._floors) - 1
        if self._current_floor_index < last_floor:
            self._floor.stop_drawing()
            self._current_floor_index += 1
            current_floor = self._floors[self._current_floor_index]
            current_floor.draw()
            self._floor = current_floor
            self._name.set(current_floor.name)
            self._seed_var.set(self._floor.seed)

    def _generate_and_draw_floor(self) -> None:
        """
        Cals the generate method and the draw method of the floor.
        """
        self.generate(self._next_seed.get())
        self._seed_var.set(self._next_seed.get())
        self._next_seed.set(secrets.token_hex(16))
        # self._floors[self._current_floor].draw(tk)
        self._floors[self._current_floor_index].draw_thread(tk)
        self._floor = self._floors[self._current_floor_index]

    def open(self) -> None:
        """
        Shows a dialog for opening a file.
        Stores the path and the name of the file.
        """
        options = utils.json_file_options.copy()
        options["initialdir"] = self._output_file_path
        options["title"] = "Open File"
        path = filedialog.askopenfilename(**options)
        if len(path) > 0:
            self._output_file_path = os.path.dirname(path)
            self._output_file_name = os.path.basename(path)
            self._name.set(self._output_file_name)
            self._path.set(self._output_file_path)
            encoding = "utf-8"
            with open(path, "r", encoding= encoding) as file:
                json_string = file.read()
                self._floor.stop_drawing()
                self._floor = TkinterFloor.from_floor(
                    Floor.from_json(json_string), self._canvas, self._output_file_name
                )
                self._floors.append(self._floor)
                self._current_floor_index = len(self._floors) - 1
                self._floors[self._current_floor_index].draw()
                self._seed_var.set(self._floor.seed)

    def save(self, path: str = "") -> str:
        """
        Shows a dialog for saving the floor to a file.
        @param path: Optional path
        @return: Path the floor has been saved to
        """
        if len(path) > 0:
            save_file = False
            # Check if the file already exists
            if os.path.exists(path):
                # Show dialog for overwriting the file
                if messagebox.askyesno(
                    "File already exists", "Do you want to overwrite the file?"
                ):
                    save_file = True
            else:
                save_file = True
            if save_file:
                # Save the file to the given path
                path = super().save(path)
                # Show dialog for saving the file
                messagebox.showinfo("Save", "File saved successfully!")

            return path
        options = utils.json_file_options.copy()
        options["initialdir"] = self._output_file_path
        options["initialfile"] = self._output_file_name
        options["title"] = "Save File"
        file_path = filedialog.asksaveasfilename(**options)
        if len(file_path) > 0:
            self._output_file_path = os.path.dirname(file_path)
            self._output_file_name = os.path.basename(file_path)
            self._name.set(self._output_file_name)
            self._path.set(self._output_file_path)
            self._floors[self._current_floor_index].name = self._name.get()
        print(file_path)

        return super().save(file_path)

    def run(self) -> None:
        """
        Sets up the ui elements and starts the main loop of the application.
        """
        self._tk.title(utils.window_title)
        self._tk.geometry(utils.window_size)
        self._tk.resizable(False, False)
        self.generate()
        self._floors[self._current_floor_index].draw()
        self._canvas.pack(anchor=tk.NW, expand=True)
        self.add_information_frame()
        self.add_buttons()
        self.create_menu_bar()
        self.apply_theme()
        self._tk.mainloop()

    def add_information_frame(self) -> None:
        """
        Adds a frame to the application which shows information about the current floor.
        """
        information_frame = ttk.Frame()
        # Create information frame
        information_frame.pack(pady=(0, 10))
        name_text = ttk.Label(information_frame, text="Floor name: ")
        name_text.pack(side=tk.LEFT)
        name_label = ttk.Label(information_frame, textvariable=self._name)
        name_label.pack(side=tk.LEFT)
        path_text = ttk.Label(information_frame, text="Current path: ")
        path_text.pack(side=tk.LEFT, padx=(25, 0))
        path_label = ttk.Label(information_frame, textvariable=self._path)
        path_label.pack(side=tk.LEFT)
        seed_text = ttk.Label(information_frame, text="Seed: ")
        seed_text.pack(side=tk.LEFT, padx=(25, 0))
        seed_label = ttk.Label(information_frame, textvariable=self._seed_var)
        seed_label.pack(side=tk.LEFT)

    def add_buttons(self) -> None:
        """
        Adds buttons to the application.
        """
        # Create button frame
        button_frame = ttk.Frame(self._tk)
        button_frame.pack(pady=(0, 10))
        button_pre = ttk.Button(button_frame, text="<-", command=self._decrease_floor)
        button_pre.pack(side=tk.LEFT, padx=10)
        # Left arrow to decrease
        self._tk.bind("<Left>", lambda event: self._decrease_floor())
        button_gen = ttk.Button(
            button_frame, text="Generate", command=self._generate_and_draw_floor
        )
        button_gen.pack(side=tk.LEFT, padx=10)
        # Space to generate
        self._tk.bind("<space>", lambda event: self._generate_and_draw_floor())
        button_next = ttk.Button(button_frame, text="->", command=self._increase_floor)
        button_next.pack(side=tk.LEFT, padx=10)
        # Right arrow to increase
        self._tk.bind("<Right>", lambda event: self._increase_floor())
        # Next seed entry
        next_seed_label = ttk.Label(button_frame, text="Next seed: ")
        next_seed_label.pack(side=tk.LEFT, padx=10)
        next_seed_entry = ttk.Entry(button_frame, textvariable=self._next_seed)
        next_seed_entry.bind(
            "<Return>", lambda event: self._seed_var.set(self._next_seed.get())
        )
        next_seed_entry.pack(side=tk.LEFT, padx=10)

    def create_menu_bar(self) -> None:
        """
        Creates a menu bar for the application.
        """
        # Create a menu bar
        menu_bar = tk.Menu(self._tk)
        self._tk.config(menu=menu_bar)
        menu_bar.add_command(label="Open", command=self.open, accelerator="Ctrl+o")
        menu_bar.add_command(
            label="Save",
            command=lambda: self.save(
                os.path.join(self._output_file_path, self._output_file_name)
                + my_globals.JSON_SUFFIX
            ),
            accelerator="Ctrl+s",
        )
        menu_bar.add_command(
            label="Save As", command=self.save, accelerator="Ctrl+Shift+s"
        )
        menu_bar.add_command(
            label="Switch Theme", command=self.switch_theme, accelerator="Ctrl+t"
        )
        menu_bar.add_command(label="Exit", command=self._tk.quit, accelerator="Ctrl+q")
