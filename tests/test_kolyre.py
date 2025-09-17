import sys
import types
import builtins
import pytest

from kolyre import Kolyre


def test_constants_have_expected_values():
    """Verify ANSI escape code constants are defined correctly."""
    assert Kolyre.RESET == "\033[0m"
    assert Kolyre.BOLD == "\033[1m"
    assert Kolyre.DIM == "\033[2m"
    assert Kolyre.ITALIC == "\033[3m"
    assert Kolyre.UNDERLINE == "\033[4m"
    assert Kolyre.REVERSED == "\033[7m"
    assert Kolyre.STRIKETHROUGH == "\033[9m"
    assert Kolyre.OVERLINE == "\033[53m"
    assert Kolyre.RED == "\033[31m"
    assert Kolyre.BRIGHT_BLUE == "\033[94m"
    assert Kolyre.BG_YELLOW == "\033[43m"
    assert Kolyre.BG_BRIGHT_WHITE == "\033[107m"

def test_foreground_256_valid_inputs():
    """Foreground 256-color codes should map correctly for valid inputs."""
    assert Kolyre.foreground_256(0) == "\033[38;5;0m"
    assert Kolyre.foreground_256(255) == "\033[38;5;255m"
    assert Kolyre.foreground_256(42) == "\033[38;5;42m"

def test_foreground_256_invalid_inputs():
    """Foreground 256-color should raise on invalid input."""
    with pytest.raises(TypeError):
        Kolyre.foreground_256("red")
    with pytest.raises(ValueError):
        Kolyre.foreground_256(-1)
    with pytest.raises(ValueError):
        Kolyre.foreground_256(256)

def test_background_256_valid_inputs():
    """Background 256-color codes should map correctly for valid inputs."""
    assert Kolyre.background_256(0) == "\033[48;5;0m"
    assert Kolyre.background_256(255) == "\033[48;5;255m"
    assert Kolyre.background_256(100) == "\033[48;5;100m"

def test_background_256_invalid_inputs():
    """Background 256-color should raise on invalid input."""
    with pytest.raises(TypeError):
        Kolyre.background_256("blue")
    with pytest.raises(ValueError):
        Kolyre.background_256(-10)
    with pytest.raises(ValueError):
        Kolyre.background_256(999)

def test_foreground_rgb_with_tuple_or_list():
    """Foreground RGB should accept tuple and list values."""
    assert Kolyre.foreground_rgb((1, 2, 3)) == "\033[38;2;1;2;3m"
    assert Kolyre.foreground_rgb([255, 128, 0]) == "\033[38;2;255;128;0m"

def test_foreground_rgb_with_integers():
    """Foreground RGB should accept three integer arguments."""
    assert Kolyre.foreground_rgb(10, 20, 30) == "\033[38;2;10;20;30m"

def test_foreground_rgb_invalid_inputs():
    """Foreground RGB should raise on invalid inputs."""
    with pytest.raises(ValueError):
        Kolyre.foreground_rgb((1, 2))
    with pytest.raises(TypeError):
        Kolyre.foreground_rgb((1, "2", 3))
    with pytest.raises(ValueError):
        Kolyre.foreground_rgb((1, 2, 300))
    with pytest.raises(ValueError):
        Kolyre.foreground_rgb(10)

def test_background_rgb_with_tuple_or_list():
    """Background RGB should accept tuple and list values."""
    assert Kolyre.background_rgb((11, 22, 33)) == "\033[48;2;11;22;33m"
    assert Kolyre.background_rgb([200, 100, 50]) == "\033[48;2;200;100;50m"

def test_background_rgb_with_integers():
    """Background RGB should accept three integer arguments."""
    assert Kolyre.background_rgb(100, 150, 200) == "\033[48;2;100;150;200m"

def test_background_rgb_invalid_inputs():
    """Background RGB should raise on invalid inputs."""
    with pytest.raises(ValueError):
        Kolyre.background_rgb([1, 2])
    with pytest.raises(TypeError):
        Kolyre.background_rgb((1, None, 3))
    with pytest.raises(ValueError):
        Kolyre.background_rgb((1, 2, 999))
    with pytest.raises(ValueError):
        Kolyre.background_rgb(128)

def test_colorize_applies_styles_when_tty(monkeypatch):
    """Colorize should wrap text with codes when stdout is a TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    result = Kolyre.colorize("hello", Kolyre.BOLD, Kolyre.RED)
    assert result == f"{Kolyre.BOLD}{Kolyre.RED}hello{Kolyre.RESET}"

def test_colorize_force_applies_styles(monkeypatch):
    """Colorize should apply styles with force=True even if not TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    result = Kolyre.colorize("world", Kolyre.BOLD, Kolyre.GREEN, force=True)
    assert result == f"{Kolyre.BOLD}{Kolyre.GREEN}world{Kolyre.RESET}"

def test_colorize_returns_plain_when_not_tty(monkeypatch):
    """Colorize should return plain text if not TTY and not forced."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    result = Kolyre.colorize("plain", Kolyre.BOLD, Kolyre.GREEN)
    assert result == "plain"

def test_colorize_type_errors(monkeypatch):
    """Colorize should raise TypeError on invalid argument types."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    with pytest.raises(TypeError):
        Kolyre.colorize(123, Kolyre.RED)
    with pytest.raises(TypeError):
        Kolyre.colorize("ok", 42)

def test_colorize_with_single_list(monkeypatch):
    """Colorize should handle a single list of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = [Kolyre.RED, Kolyre.BOLD]
    result = Kolyre.colorize("list", codes)
    assert result == f"{Kolyre.RED}{Kolyre.BOLD}list{Kolyre.RESET}"

def test_colorize_with_tuple(monkeypatch):
    """Colorize should handle a tuple of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = (Kolyre.GREEN, Kolyre.UNDERLINE)
    result = Kolyre.colorize("tuple", codes)
    assert result == f"{Kolyre.GREEN}{Kolyre.UNDERLINE}tuple{Kolyre.RESET}"

def test_colorize_with_multiple_lists(monkeypatch):
    """Colorize should flatten and apply multiple lists of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes1 = [Kolyre.RED]
    codes2 = [Kolyre.BOLD]
    result = Kolyre.colorize("lists", codes1, codes2)
    assert result == f"{Kolyre.RED}{Kolyre.BOLD}lists{Kolyre.RESET}"

def test_colorize_with_mixed_list_and_string(monkeypatch):
    """Colorize should handle mixed list and string codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = [Kolyre.RED]
    result = Kolyre.colorize("mixed", codes, Kolyre.BOLD)
    assert result == f"{Kolyre.RED}{Kolyre.BOLD}mixed{Kolyre.RESET}"

def test_enable_ansi_support_non_windows(monkeypatch):
    """On non-Windows platforms, ANSI support should always be enabled."""
    monkeypatch.setattr(sys, "platform", "linux")
    assert Kolyre.enable_ansi_support() is True

def test_enable_ansi_support_windows_without_ctypes(monkeypatch):
    """On Windows without ctypes, ANSI support should not be enabled."""
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(
        builtins,
        "__import__",
        lambda name, *args: (_ for _ in ()).throw(ImportError())
        if name == "ctypes"
        else __import__(name, *args),
    )
    assert Kolyre.enable_ansi_support() is False

def test_enable_ansi_support_windows_with_ctypes(monkeypatch):
    """On Windows with ctypes available, enable_ansi_support should run gracefully."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        def GetStdHandle(self, _):
            return -1

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32())
    )
    original_ctypes = sys.modules.get("ctypes")
    sys.modules["ctypes"] = dummy_ctypes
    try:
        assert Kolyre.enable_ansi_support() is False
    finally:
        if original_ctypes is not None:
            sys.modules["ctypes"] = original_ctypes
        else:
            del sys.modules["ctypes"]
