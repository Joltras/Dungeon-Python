import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from collections import deque
import globals
import utils
from floors.floor import Floor
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
        color = globals.Color.LIGHT_GRAY.value
        hex_color = utils.rgb2hex(color[0], color[1], color[2])
        self._canvas = tk.Canvas(height=globals.FLOOR_HEIGHT * globals.ROOM_HEIGHT,
                                 width=globals.ROOM_WIDTH * globals.ROOM_WIDTH,
                                 background=hex_color)
        self._path = tk.StringVar()
        self._path.set(self._output_file_path)
        self._name = tk.StringVar()
        self._name.set(self._output_file_name)
        self._menu_bar = tk.Menu(self._tk)
        self._current_theme = "light"
        self.apply_theme()

    def apply_theme(self) -> None:
        """
        Applies the current theme to the application.
        """
        if self._current_theme == "light":
            self._tk.configure(background="light gray", highlightbackground="black")
            style = ttk.Style(self._tk)
            style.configure("TButton", background="white", foreground="black", hover="black")
            style.configure("TFrame", background="light gray", foreground="black")
            style.theme_use("default")
            self._canvas.configure(background="white", highlightbackground="black")
        else:
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
        self._floors.append(TkinterFloor(globals.FLOOR_HEIGHT, globals.FLOOR_WIDTH, canvas=self._canvas, name=globals.DEFAULT_FLOOR_NAME + globals.JSON_SUFFIX))
        self._current_floor = len(self._floors) - 1
        self._floor = self._floors[self._current_floor]
        self._floors[self._current_floor].draw(tk)
        self._name.set(self._floors[self._current_floor].name)

    def _decrease_floor(self) -> None:
        """
        Lowers the index of the current floor.
        """
        if self._current_floor > 0:
            self._current_floor -= 1
            self._floors[self._current_floor].draw(tk)
            self._floor = self._floors[self._current_floor]
            self._name.set(self._floors[self._current_floor].name)

    def _increase_floor(self) -> None:
        """
        Increases the index of the current floor.
        """
        if self._current_floor < len(self._floors) - 1:
            self._current_floor += 1
            self._floors[self._current_floor].draw(tk)
            self._floor = self._floors[self._current_floor]
            self._name.set(self._floors[self._current_floor].name)

    def _generate_and_draw_floor(self) -> None:
        """
        Cals the generate method and the draw method of the floor.
        """
        self.generate()
        self._floors[self._current_floor].draw(tk)
        self._floor = self._floors[self._current_floor]

    def open(self) -> None:
        options = {
            'defaultextension': globals.JSON_SUFFIX,
            'filetypes': [('Json', globals.JSON_SUFFIX)],
            'initialdir': self._output_file_path,
            'initialfile': self._output_file_name,
            'title': 'Open File'
        }
        path = filedialog.askopenfilename(**options)
        if len(path) > 0:
            self._output_file_path = os.path.dirname(path)
            self._output_file_name = os.path.basename(path)
            self._name.set(self._output_file_name)
            self._path.set(self._output_file_path)
            with open(path, "r") as file:
                json_string = file.read()
                self._floor = TkinterFloor.from_floor(Floor.from_json(json_string), self._canvas, self._output_file_name)
                self._floors.append(self._floor)
                self._current_floor = len(self._floors) - 1
                self._floors[self._current_floor].draw(tk)

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
                if messagebox.askyesno("File already exists", "Do you want to overwrite the file?"):
                    save_file = True
            else:
                save_file = True
            if save_file:
                # Save the file to the given path
                path = super().save(path)
                # Show dialog for saving the file
                messagebox.showinfo("Save", "File saved successfully!")

            return path
        options = {
            'defaultextension': globals.JSON_SUFFIX,
            'filetypes': [('Json', globals.JSON_SUFFIX)],
            'initialdir': self._output_file_path,
            'initialfile': self._output_file_name,
            'title': 'Datei speichern unter'
        }
        file_path = filedialog.asksaveasfilename(**options)
        if len(file_path) > 0:
            self._output_file_path = os.path.dirname(file_path)
            self._output_file_name = os.path.basename(file_path)
            self._name.set(self._output_file_name)
            self._path.set(self._output_file_path)
            self._floors[self._current_floor].name = self._name.get()
        print(file_path)

        return super().save(file_path)

    def run(self) -> None:
        """
        Sets up the ui elements and starts the main loop of the application.
        """
        self._tk.title("Dungeon Generator")
        self._tk.geometry("1200x550")
        self._tk.resizable(False, False)
        self.generate()
        self._floors[self._current_floor].draw(tk)
        self._canvas.pack(anchor=tk.NW, expand=True)
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

        # Create button frame
        button_frame = ttk.Frame(self._tk)
        button_frame.pack(pady=(0, 10))
        button_pre = ttk.Button(button_frame, text="<-", command=self._decrease_floor)
        button_pre.pack(side=tk.LEFT, padx=10)
        # Left arrow to decrease
        self._tk.bind("<Left>", lambda event: self._decrease_floor())
        button_gen = ttk.Button(button_frame, text="Generate", command=self._generate_and_draw_floor)
        button_gen.pack(side=tk.LEFT, padx=10)
        # Space to generate
        self._tk.bind("<space>", lambda event: self._generate_and_draw_floor())
        button_next = ttk.Button(button_frame, text="->", command=self._increase_floor)
        button_next.pack(side=tk.LEFT, padx=10)
        # Right arrow to increase
        self._tk.bind("<Right>", lambda event: self._increase_floor())


        # Create a menu bar
        menu_bar = tk.Menu(self._tk)
        self._tk.config(menu=menu_bar)
        menu_bar.add_command(label="Open", command=self.open, accelerator="Ctrl+o")
        menu_bar.add_command(label="Save", command=lambda: self.save(os.path.join(
            self._output_file_path, self._output_file_name) + globals.JSON_SUFFIX)
                             , accelerator="Ctrl+s")
        menu_bar.add_command(label="Save As", command=self.save, accelerator="Ctrl+Shift+s")
        menu_bar.add_command(label="Switch Theme", command=self.switch_theme, accelerator="Ctrl+t")
        menu_bar.add_command(label="Exit", command=self._tk.quit, accelerator="Ctrl+q")
        self.apply_theme()
        self._tk.mainloop()
