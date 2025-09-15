# Kolyre

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-cross--platform-607D8B?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-4CAF50?style=for-the-badge)

**Kolyre** is a lightweight Python library for **ANSI terminal text styling and coloring**, supporting text styles, standard and extended colors, and 24-bit RGB (truecolor) output.

## Features

- **Text Styles:** Bold, Dim, Italic, Underline, Reversed, Strikethrough, Overline
- **Colors:** Standard 16 colors + bright variants for foreground and background
- **256-Color Palette:** Extended ANSI palette (0–255)
- **Truecolor (RGB) Support:** 24-bit RGB for precise coloring
- **Cross-Platform:** Works on Linux, macOS, and Windows
- **Single File:** No dependencies; place `kolyre.py` in your project directory

## Installation

Download and include `kolyre.py` in your project:

- **Via GitHub:**
  Either clone the repository:
  ```bash
  git clone https://github.com/DevBytAmir/kolyre.git
  cd kolyre
  ```
  Or download `kolyre.py` directly from [GitHub](https://github.com/DevBytAmir/kolyre).
  Then place `kolyre.py` in your project directory.

No setup or external dependencies are required.

## Quick Start

```python
from kolyre import Kolyre

# Store ANSI codes in variables
red = Kolyre.RED
bold = Kolyre.BOLD

# Use variables or codes directly
print(f"{red}Hello World{Kolyre.RESET}")
print(f"{bold}{Kolyre.CYAN}Bold and Cyan{Kolyre.RESET}")
print(f"{Kolyre.BG_WHITE}Text with white background{Kolyre.RESET}")

# Using the colorize method
print(Kolyre.colorize("Bold, Yellow, and Underlined", Kolyre.BOLD, Kolyre.YELLOW, Kolyre.UNDERLINE))

# 256-color example
fg_index = 128
print(f"{Kolyre.foreground_256(fg_index)}Hello 256-color{Kolyre.RESET}")

# Truecolor (RGB) example using a variable
rgb_color = (255, 100, 50)
print(f"{Kolyre.foreground_rgb(rgb_color)}Hello RGB{Kolyre.RESET}")

# Truecolor example parameter by parameter
print(f"{Kolyre.foreground_rgb(50, 200, 150)}Hello RGB{Kolyre.RESET}")
```

## Demo

Run the demo to display all available text styles and colors:

1. Open a terminal or command prompt.
2. Navigate to the directory containing `kolyre.py`.
3. Execute the script:
    ```bash
    python kolyre.py
    ```

## Notes

- Truecolor (RGB) support may vary depending on your terminal.
- On Windows, calling `Kolyre.enable_ansi_support()` is sometimes necessary to display colors correctly.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
