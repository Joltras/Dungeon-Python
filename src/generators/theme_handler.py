"""
Module to handle the theme of the application.
"""

from tkinter import Tk, Canvas, ttk


class ThemeHandler:
    """
    Class to handle the theme of the application.
    """

    def __init__(self, tk: Tk, canvas: Canvas) -> None:
        """
        Creates a new theme handler.
        @param tk: Root of the application
        @param canvas: Canvas of the application
        """
        self._tk = tk
        self._canvas = canvas
        self._current_theme = "light"
        self.apply_theme()

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

    def apply_theme(self) -> None:
        """
        Applies the current theme to the application.
        """
        if self._current_theme == "light":
            self._set_light_theme()
        else:
            self._set_dark_theme()
