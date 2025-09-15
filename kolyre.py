"""
Kolyre - Lightweight ANSI terminal text styling and coloring for Python.

Provides the `Kolyre` class for applying ANSI escape codes for text styles, 
foreground and background colors, 256-color palette, and truecolor (24-bit RGB) support.
"""

__version__ = "1.0.0"
__author__ = "DevBytAmir"
__license__ = "MIT"

import sys
from typing import Final

class Kolyre:
    """
    ANSI terminal text styling and coloring utility.

    Includes constants for common text styles, as well as foreground and background colors. 
    Provides methods for generating 256-color and truecolor (24-bit RGB) ANSI codes. 

    The `colorize` method allows applying multiple styles at once, and `enable_ansi_support` 
    can help display ANSI codes correctly on some Windows terminals.

    Truecolor support may vary depending on the terminal.
    """
    RESET: Final[str] = "\033[0m"
    BOLD: Final[str] = "\033[1m"
    DIM: Final[str] = "\033[2m"
    ITALIC: Final[str] = "\033[3m"
    UNDERLINE: Final[str] = "\033[4m"
    REVERSED: Final[str] = "\033[7m"
    STRIKETHROUGH: Final[str] = "\033[9m"
    OVERLINE: Final[str] = "\033[53m"

    BLACK: Final[str] = "\033[30m"
    RED: Final[str] = "\033[31m"
    GREEN: Final[str] = "\033[32m"
    YELLOW: Final[str] = "\033[33m"
    BLUE: Final[str] = "\033[34m"
    MAGENTA: Final[str] = "\033[35m"
    CYAN: Final[str] = "\033[36m"
    WHITE: Final[str] = "\033[37m"
    BRIGHT_BLACK: Final[str] = "\033[90m"
    BRIGHT_RED: Final[str] = "\033[91m"
    BRIGHT_GREEN: Final[str] = "\033[92m"
    BRIGHT_YELLOW: Final[str] = "\033[93m"
    BRIGHT_BLUE: Final[str] = "\033[94m"
    BRIGHT_MAGENTA: Final[str] = "\033[95m"
    BRIGHT_CYAN: Final[str] = "\033[96m"
    BRIGHT_WHITE: Final[str] = "\033[97m"

    BG_BLACK: Final[str] = "\033[40m"
    BG_RED: Final[str] = "\033[41m"
    BG_GREEN: Final[str] = "\033[42m"
    BG_YELLOW: Final[str] = "\033[43m"
    BG_BLUE: Final[str] = "\033[44m"
    BG_MAGENTA: Final[str] = "\033[45m"
    BG_CYAN: Final[str] = "\033[46m"
    BG_WHITE: Final[str] = "\033[47m"
    BG_BRIGHT_BLACK: Final[str] = "\033[100m"
    BG_BRIGHT_RED: Final[str] = "\033[101m"
    BG_BRIGHT_GREEN: Final[str] = "\033[102m"
    BG_BRIGHT_YELLOW: Final[str] = "\033[103m"
    BG_BRIGHT_BLUE: Final[str] = "\033[104m"
    BG_BRIGHT_MAGENTA: Final[str] = "\033[105m"
    BG_BRIGHT_CYAN: Final[str] = "\033[106m"
    BG_BRIGHT_WHITE: Final[str] = "\033[107m"

    @staticmethod
    def colorize(text: str, *ansi_codes: str | tuple | list, force: bool = False) -> str:
        """
        Apply one or more ANSI codes to the given text.

        Args:
            text (str): The text to style.
            *ansi_codes (str | tuple | list): One or more ANSI codes, individually
                or nested in lists/tuples.
            force (bool, optional): Apply styling even if stdout is not a TTY.

        Returns:
            str: The styled text, reset with `Kolyre.RESET`.

        Raises:
            TypeError: If `text` is not a `str`, or if any provided ANSI code is not a `str`.
        """
        if not isinstance(text, str):
            raise TypeError(f"text must be a string, got {type(text).__name__}")
        if not ansi_codes:
            return text

        codes: list[str] = []

        def _flatten(item: str | tuple | list) -> None:
            """Recursively flatten ANSI codes into the `codes` list."""
            if isinstance(item, str):
                codes.append(item)
            elif isinstance(item, (list, tuple)):
                for c in item:
                    _flatten(c)
            else:
                raise TypeError(f"ANSI code must be a string, list, or tuple of strings, got {type(item).__name__}")

        for code in ansi_codes:
            _flatten(code)

        if not force and not sys.stdout.isatty():
            return text

        return f"{''.join(codes)}{text}{Kolyre.RESET}"

    @staticmethod
    def foreground_256(color_index: int) -> str:
        """
        Return a 256-color ANSI code for the foreground.

        Args:
            color_index (int): Value between 0 and 255 from the ANSI 256-color palette.

        Returns:
            str: ANSI escape sequence for the specified foreground color.

        Raises:
            TypeError: If `color_index` is not an integer.
            ValueError: If `color_index` is outside the range 0-255.
        """ 
        if not isinstance(color_index, int):
            raise TypeError(f"color_index must be an integer, got {type(color_index).__name__}")
        if not 0 <= color_index <= 255:
            raise ValueError(f"color_index must be between 0 and 255, got {color_index}")
        
        return f"\033[38;5;{color_index}m"

    @staticmethod
    def background_256(color_index: int) -> str:
        """
        Return a 256-color ANSI code for the background.

        Args:
            color_index (int): Value between 0 and 255 from the ANSI 256-color palette.

        Returns:
            str: ANSI escape sequence for the specified background color.

        Raises:
            TypeError: If `color_index` is not an integer.
            ValueError: If `color_index` is outside the range 0-255.
        """
        if not isinstance(color_index, int):
            raise TypeError(f"color_index must be an integer, got {type(color_index).__name__}")   
        if not 0 <= color_index <= 255:
            raise ValueError(f"color_index must be between 0 and 255, got {color_index}")
        
        return f"\033[48;5;{color_index}m"
    
    @staticmethod
    def foreground_rgb(rgb: tuple[int, int, int] | list[int] | int, green: int | None = None, blue: int | None = None) -> str:
        """
        Return a truecolor (RGB) ANSI code for the foreground.

        Args:
            rgb (tuple, list, or int): RGB values as a 3-item sequence or red value if green and blue are provided.
            green (int, optional): Green value if rgb is an int.
            blue (int, optional): Blue value if rgb is an int.

        Returns:
            str: ANSI escape sequence for the specified RGB foreground color.

        Raises:
            TypeError: If any component is not an integer.
            ValueError: If any RGB component is outside the range 0-255, or if the input is malformed.
        """
        if isinstance(rgb, (tuple, list)):
            if len(rgb) != 3:
                raise ValueError(f"RGB sequence must have exactly 3 values, got {len(rgb)}")
            red, green, blue = rgb
        elif isinstance(rgb, int) and green is not None and blue is not None:
            red = rgb
        else:
            raise ValueError("Invalid RGB input. Provide (r, g, b), [r, g, b], or three integers.")

        for name, value in zip(("red", "green", "blue"), (red, green, blue)):
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
            if not 0 <= value <= 255:
                raise ValueError(f"{name} must be between 0 and 255, got {value}")

        return f"\033[38;2;{red};{green};{blue}m"
    
    @staticmethod
    def background_rgb(rgb: tuple[int, int, int] | list[int] | int, green: int | None = None, blue: int | None = None) -> str:
        """
        Return a truecolor (RGB) ANSI code for the background.

        Args:
            rgb (tuple, list, or int): RGB values as a 3-item sequence or red value if green and blue are provided.
            green (int, optional): Green value if rgb is an int.
            blue (int, optional): Blue value if rgb is an int.

        Returns:
            str: ANSI escape sequence for the specified RGB background color.

        Raises:
            TypeError: If any component is not an integer.
            ValueError: If any RGB component is outside the range 0-255, or if the input is malformed.
        """ 
        if isinstance(rgb, (tuple, list)):
            if len(rgb) != 3:
                raise ValueError(f"RGB sequence must have exactly 3 values, got {len(rgb)}")
            red, green, blue = rgb
        elif isinstance(rgb, int) and green is not None and blue is not None:
            red = rgb
        else:
            raise ValueError("Invalid RGB input. Provide (r, g, b), [r, g, b], or three integers.")

        for name, value in zip(("red", "green", "blue"), (red, green, blue)):
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
            if not 0 <= value <= 255:
                raise ValueError(f"{name} must be between 0 and 255, got {value}")

        return f"\033[48;2;{red};{green};{blue}m"

    @staticmethod 
    def enable_ansi_support() -> bool:
        """
        Enable ANSI escape sequences on Windows terminals.

        Returns:
            bool: True if ANSI support is active or not needed; False if enabling failed.
        """
        if sys.platform != "win32":
            return True
        
        try:
            import ctypes
        except ImportError:
            return False

        try:
            STD_OUTPUT_HANDLE = -11
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

            handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            if handle in (0, -1):
                return False

            mode = ctypes.c_uint32()
            if not ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return False

            return bool(ctypes.windll.kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING))
        except (AttributeError, OSError):
            return False
        
    @staticmethod
    def demo() -> None:
        """Display a demonstration of available styles, colors, and RGB examples."""
        color_categories = {
            "Foreground Colors": [
                ("BLACK", Kolyre.BLACK), ("BRIGHT_BLACK", Kolyre.BRIGHT_BLACK),
                ("RED", Kolyre.RED), ("BRIGHT_RED", Kolyre.BRIGHT_RED),
                ("GREEN", Kolyre.GREEN), ("BRIGHT_GREEN", Kolyre.BRIGHT_GREEN),
                ("YELLOW", Kolyre.YELLOW), ("BRIGHT_YELLOW", Kolyre.BRIGHT_YELLOW),
                ("BLUE", Kolyre.BLUE), ("BRIGHT_BLUE", Kolyre.BRIGHT_BLUE),
                ("MAGENTA", Kolyre.MAGENTA), ("BRIGHT_MAGENTA", Kolyre.BRIGHT_MAGENTA),
                ("CYAN", Kolyre.CYAN), ("BRIGHT_CYAN", Kolyre.BRIGHT_CYAN),
                ("WHITE", Kolyre.WHITE), ("BRIGHT_WHITE", Kolyre.BRIGHT_WHITE),
            ],
            "Background Colors": [
                ("BG_BLACK", Kolyre.BG_BLACK), ("BG_BRIGHT_BLACK", Kolyre.BG_BRIGHT_BLACK),
                ("BG_RED", Kolyre.BG_RED), ("BG_BRIGHT_RED", Kolyre.BG_BRIGHT_RED),
                ("BG_GREEN", Kolyre.BG_GREEN), ("BG_BRIGHT_GREEN", Kolyre.BG_BRIGHT_GREEN),
                ("BG_YELLOW", Kolyre.BG_YELLOW), ("BG_BRIGHT_YELLOW", Kolyre.BG_BRIGHT_YELLOW),
                ("BG_BLUE", Kolyre.BG_BLUE), ("BG_BRIGHT_BLUE", Kolyre.BG_BRIGHT_BLUE),
                ("BG_MAGENTA", Kolyre.BG_MAGENTA), ("BG_BRIGHT_MAGENTA", Kolyre.BG_BRIGHT_MAGENTA),
                ("BG_CYAN", Kolyre.BG_CYAN), ("BG_BRIGHT_CYAN", Kolyre.BG_BRIGHT_CYAN),
                ("BG_WHITE", Kolyre.BG_WHITE), ("BG_BRIGHT_WHITE", Kolyre.BG_BRIGHT_WHITE),
            ],
            "Text Styles": [
                ("BOLD", Kolyre.BOLD), ("DIM", Kolyre.DIM), ("ITALIC", Kolyre.ITALIC),
                ("UNDERLINE", Kolyre.UNDERLINE), ("REVERSED", Kolyre.REVERSED),
                ("STRIKETHROUGH", Kolyre.STRIKETHROUGH), ("OVERLINE", Kolyre.OVERLINE),
            ],
        }

        def print_named(items_per_row: int = 2) -> None:
            """
            Print named text styles, foreground colors, and background colors.

            Args:
                items_per_row (int): Number of items per row.
            """
            for category_name, items in color_categories.items():
                max_len = max(len(name) for name, _ in items) + 2
                heading = Kolyre.colorize(f"======= {category_name} =======", Kolyre.BOLD, Kolyre.UNDERLINE, Kolyre.CYAN)
                print(f"\n{heading}\n")
                for i in range(0, len(items), items_per_row):
                    row = items[i:i + items_per_row]
                    print(" ".join(f"{code}{name:<{max_len}}{Kolyre.RESET}" for name, code in row))
                
        def print_256(foreground: bool = True, count: int = 32, per_row: int = 16) -> None:
            """
            Display a 256-color ANSI palette for foreground or background colors.

            Args:
                foreground (bool): True to display foreground colors, False for background.
                count (int): Number of colors to display.
                per_row (int): Number of color blocks per row.
            """
            title = "Foreground" if foreground else "Background"
            heading = Kolyre.colorize(f"======= 256-Color Palette ({title}) =======", Kolyre.BOLD, Kolyre.UNDERLINE, Kolyre.CYAN)
            print(f"\n{heading}\n")
            for i in range(count):
                code = Kolyre.foreground_256(i) if foreground else Kolyre.background_256(i)
                end = "\n" if (i + 1) % per_row == 0 else " "
                print(f"{code}{i:>3}{Kolyre.RESET}", end=end)
            if count % per_row != 0:
                print()

        def print_rgb(foreground: bool = True, step: int = 51, block_fg: str = "ABC", block_bg: str = "ABC", per_row: int = 25) -> None:
            """
            Display an RGB color gradient using ANSI codes.

            Args:
                foreground (bool): True for foreground colors, False for background.
                step (int): Increment for R, G, B values.
                block_fg (str): Characters to represent foreground color blocks.
                block_bg (str): Characters to represent background color blocks.
                per_row (int): Number of blocks per row.
            """
            title = "Foreground" if foreground else "Background"
            heading = Kolyre.colorize(f"======= RGB Gradient ({title}) =======", Kolyre.BOLD, Kolyre.UNDERLINE, Kolyre.CYAN)
            print(f"\n{heading}\n")
            count = 0
            for r in range(0, 256, step):
                for g in range(0, 256, step):
                    for b in range(0, 256, step):
                        if foreground:
                            code = Kolyre.foreground_rgb(r, g, b)
                            block = block_fg
                        else:
                            code = Kolyre.background_rgb(r, g, b)
                            block = block_bg

                        print(f"{code}{block}{Kolyre.RESET}", end=" ")
                        count += 1
                        if count % per_row == 0:
                            print()
            if count % per_row != 0:
                print()

        print_named(items_per_row=2)
        print_256(foreground=True)
        print_256(foreground=False)
        print_rgb(foreground=True)
        print_rgb(foreground=False)
    
if __name__ == "__main__":
    try:
        print("Starting Kolyre demo...\n")
        if Kolyre.enable_ansi_support():
            print("ANSI support enabled (or not required on this platform).")
            Kolyre.demo()
        else:
            print("Failed to enable ANSI support. Colors may not display correctly.")
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")