# SSH-Type
A retro-inspired terminal-based typing speed test inspired by [monkeytype.com](https://monkeytype.com), built using Python and curses. Features real-time WPM tracking, a timer bar, amber color scheme, and detailed end-of-session stats.

---

## Features

* 30-second timed typing session
* Amber retro terminal aesthetic
* Real-time WPM counter
* Error tracking
* End screen with:

  * Final WPM
  * Total Errors
  * Accuracy (%) based on typed characters
  * Consistency (WPM standard deviation)

---

## Dependencies

* Python 3.x
* `numpy` (for WPM consistency stats)

Install with pip:

```bash
pip install numpy
```

---

## Usage

```bash
python monkeytype_terminal.py
```

> Run it in a real terminal (not in an IDE terminal emulator).

Start typing when the session begins. After 30 seconds, view your results. Type `quit` or press `Ctrl+C` to exit.

---

## Notes

* Adjust `SESSION_TIME` or `NUM_WORDS` in the script to customize the test length.
* Only works in Unix-like or Windows terminals that support the `curses` library.

---
