# reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

import os
from getpass import getpass
from typing import Iterable, NoReturn, final, overload

from colorama import just_fix_windows_console

_ESCAPE = "\033"
_is_windows = os.name == "nt"

just_fix_windows_console()


@final
class Foreground:
    """Foreground colors, as per some spec I don't know anything about."""

    BLACK = f"{_ESCAPE}[30m"
    RED = f"{_ESCAPE}[31m"
    GREEN = f"{_ESCAPE}[32m"
    YELLOW = f"{_ESCAPE}[33m"
    BLUE = f"{_ESCAPE}[34m"
    MAGENTA = f"{_ESCAPE}[35m"
    CYAN = f"{_ESCAPE}[36m"
    WHITE = f"{_ESCAPE}[37m"

    @staticmethod
    def make_rgb(r: int, g: int, b: int) -> str:
        """
        Creates a True Color Escape Code Sequence for the foreground color using the RGB values provided.
        Note that this functionality is not supported by all terminals.

        ### Args:
            r (int): red channel
            g (int): green channel
            b (int): blue channel

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[38;2;{r};{g};{b}m"

    @staticmethod
    def make(code: int) -> str:
        return f"{_ESCAPE}[{code}m"


@final
class Background:
    """Background colors, as per some spec someone very smart wrote."""

    BLACK = f"{_ESCAPE}[40m"
    RED = f"{_ESCAPE}[41m"
    GREEN = f"{_ESCAPE}[42m"
    YELLOW = f"{_ESCAPE}[43m"
    BLUE = f"{_ESCAPE}[44m"
    MAGENTA = f"{_ESCAPE}[45m"
    CYAN = f"{_ESCAPE}[46m"
    WHITE = f"{_ESCAPE}[47m"

    @staticmethod
    def make_rgb(r: int, g: int, b: int) -> str:
        """
        Creates a True Color Escape Code Sequence for the background color using the RGB values provided.
        Note that this functionality is not supported by all terminals.

        ### Args:
            r (int): red channel
            g (int): green channel
            b (int): blue channel

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[48;2;{r};{g};{b}m"

    @staticmethod
    def make(code: int) -> str:
        """
        Creates an Escape Code Sequence for the background color using the ANSI Code provided.

        ### Args:
            code (int): code

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{code}m"


@final
class Modifier:
    """Modifiers, as per some spec. No clue which tho."""

    RESET = f"{_ESCAPE}[0m"
    BOLD = f"{_ESCAPE}[1m"
    DIM = f"{_ESCAPE}[2m"
    FAINT = f"{_ESCAPE}[2m"
    ITALIC = f"{_ESCAPE}[3m"
    UNDERLINE = f"{_ESCAPE}[4m"
    BLINK = f"{_ESCAPE}[5m"
    REVERSE = f"{_ESCAPE}[7m"
    INVERSE = f"{_ESCAPE}[7m"
    HIDDEN = f"{_ESCAPE}[8m"
    INVISIBLE = f"{_ESCAPE}[8m"
    STRIKETHROUGH = f"{_ESCAPE}[9m"


class Console:
    """A simple class to make console output easier and more consistent!"""

    @overload
    def __init__(
        self,
        *,
        prompt_color: str,
        input_color: str,
        arrow_color: str,
        error_color: str,
        hint_color: str,
        panic_color: str,
    ) -> None: ...

    @overload
    def __init__(self, **kwargs: str) -> None: ...

    def __init__(self, **kwargs: str) -> None:
        self._prompt_color: str = kwargs.get("prompt_color", Foreground.CYAN)
        self._input_color: str = kwargs.get("input_color", Modifier.RESET)
        self._arrow_color: str = kwargs.get(
            "arrow_color", Foreground.GREEN + Modifier.BOLD
        )
        self._error_color: str = kwargs.get("error_color", Foreground.RED)
        self._hint_color: str = kwargs.get("hint_color", Foreground.YELLOW)
        self._panic_color: str = kwargs.get(
            "panic_color", Foreground.RED + Modifier.BOLD
        )

    def print(
        self,
        text: str,
        color: str = Modifier.RESET,
        /,
        *,
        end: str = "\n",
        flush: bool = False,
        sep: str = " ",
        newline: bool = True,
    ) -> None:
        print(
            f"{color}{text}{Modifier.RESET}",
            end=end if newline else " ",
            flush=flush,
            sep=sep,
        )

    def input(
        self,
        prompt: str,
        /,
        *,
        invalid_values: list[str] | None = None,
        ensure_not_empty: bool = True,
        is_password: bool = False,
    ) -> str:
        self.print(prompt, self._prompt_color)
        self.print(">>", self._arrow_color, newline=False, flush=True)

        res = (getpass if is_password else input)("").strip()

        if res == "cls" or res == "clear":
            self.clear()
            return self.input(prompt)

        if res == "exit":
            exit(0)

        invalid_values = invalid_values or []

        if ensure_not_empty:
            invalid_values.append("")

        if res in invalid_values:
            self.error("Invalid value. Try again.")
            return self.input(prompt, invalid_values=invalid_values)

        return res

    def options(
        self,
        prompt: str,
        /,
        *,
        options: list[str] | None = None,
        capitalize: bool = True,
    ) -> str:
        options = options or ["yes", "no"]

        if self._has_repetitions(opt[0].lower() for opt in options):
            raise ValueError(
                "Options can't have two options whose first letter is the same."
            )

        kv_options = {option[0].lower(): option for option in options}

        while True:
            option = self.input(
                f'{prompt} {self._format_iter(f"[{opt[0].upper() if capitalize else opt[0]}]{opt[1:].lower()}" for opt in options)}'
            ).lower()[0]

            if option in kv_options.keys():
                self.erase_lines()
                self.action(f"Chosen option: {kv_options[option]}", Foreground.MAGENTA)
                return option

            self.error(
                "Invalid option.",
                hint=f"Choose one among the following options: {self._format_iter(kv_options.keys(), upper=True)}",
            )

    def action(self, text: str, color: str = Modifier.RESET, /) -> None:
        self.print(">>", self._arrow_color, newline=False)
        self.print(text, color)

    def error(self, error: Exception | str, /, *, hint: str = "") -> None:
        self.print(str(error), self._error_color)
        _ = hint and self.print(hint, self._hint_color)

    def panic(self, error: str, /, *, hint: str = "", code: int = -1) -> NoReturn:
        self.error(error, hint=hint)
        self.enter_to_continue()
        exit(code)

    def enter_to_continue(self, text: str = "Press enter to continue...") -> None:
        self.input(text, ensure_not_empty=False, is_password=True)
        self.erase_lines(2)

    def clear(self):
        os.system("cls" if _is_windows else "clear")

    def erase_lines(self, count: int = 1, /) -> None:
        cursor_up_one = f"{_ESCAPE}[1A"
        erase_line = f"{_ESCAPE}[2K"

        for _ in range(count):
            print(cursor_up_one + erase_line, end="", flush=True)

    def _format_iter(self, iter: Iterable[str], upper: bool = False) -> str:
        _iter = (txt.upper() if upper else txt for txt in iter)
        return self._reverse_replace(", ".join(_iter), ", ", " or ") + "."

    def _reverse_replace(self, text: str, old: str, new: str) -> str:
        return new.join(text.rsplit(old, 1))

    def _has_repetitions(self, iter: Iterable[str]) -> bool:
        return len(lst := list(iter)) != len(set(lst))
