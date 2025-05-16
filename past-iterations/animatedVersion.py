import curses
import random
import time
import numpy as np

WORDS = [
    "banana", "monkey", "jungle", "keyboard", "speed", "typing", "python",
    "swing", "tree", "leaf", "jump", "grip", "hang", "code", "linux", "shell",
    "space", "focus"
]
NUM_WORDS = 50
SESSION_TIME = 30  # seconds for the typing session

def draw_text(stdscr, target_words, current_input, errors, wpm_val, elapsed, cursor_pos, cursor_visible, time_left_ratio):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x, y = 0, 1  # leave row 0 for timer bar
    char_index = 0
    flat_target = ' '.join(target_words)
    flat_input = ''.join(current_input)

    # Timer bar
    bar_width = int(width * time_left_ratio)
    stdscr.addstr(0, 0, " " * bar_width, curses.color_pair(4))

    for word in target_words:
        for char in word:
            if x >= width:
                y += 1
                x = 0
            color = curses.A_NORMAL
            if char_index < len(flat_input):
                typed_char = flat_input[char_index]
                if typed_char == char:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)
            if char_index == cursor_pos and cursor_visible:
                color |= curses.A_REVERSE
            stdscr.attron(color)
            stdscr.addch(y, x, char)
            stdscr.attroff(color)
            x += 1
            char_index += 1
        if x < width:
            color = curses.A_NORMAL
            if char_index < len(flat_input):
                if flat_input[char_index] == ' ':
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)
            if char_index == cursor_pos and cursor_visible:
                color |= curses.A_REVERSE
            stdscr.attron(color)
            stdscr.addch(y, x, ' ')
            stdscr.attroff(color)
            x += 1
            char_index += 1

    stdscr.addstr(y + 2, 0, f"Errors: {errors}")
    stdscr.addstr(y + 3, 0, f"WPM: {wpm_val}")
    stdscr.addstr(y + 4, 0, f"Time: {int(elapsed)}s / {SESSION_TIME}s")
    stdscr.refresh()

def calculate_wpm(correct_chars, elapsed):
    return round((correct_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0

def monkeytype(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(16)

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

    target_words = random.choices(WORDS, k=NUM_WORDS)
    current_input = []
    errors = 0
    started = False
    start_time = None
    cursor_visible = True
    blink_interval = 0.5
    last_blink = time.time()
    wpm_history = []

    while True:
        if not started:
            stdscr.clear()
            stdscr.addstr(0, 0, "Monkeytype TUI – Press any key to start a timed session (30s)...")
            stdscr.refresh()
            stdscr.getch()
            start_time = time.time()
            started = True

        now = time.time()
        elapsed = now - start_time
        time_left = SESSION_TIME - elapsed
        if time_left <= 0:
            break

        if now - last_blink >= blink_interval:
            cursor_visible = not cursor_visible
            last_blink = now

        typed = ''.join(current_input)
        flat_target = ' '.join(target_words)

        correct_chars = sum(1 for i in range(min(len(typed), len(flat_target))) if typed[i] == flat_target[i])
        errors = sum(1 for i in range(len(typed)) if i < len(flat_target) and typed[i] != flat_target[i])
        wpm_val = calculate_wpm(correct_chars, elapsed)
        wpm_history.append(wpm_val)
        cursor_pos = len(current_input)
        time_ratio = max(0, min(1, time_left / SESSION_TIME))

        draw_text(stdscr, target_words, current_input, errors, wpm_val, elapsed, cursor_pos, cursor_visible, time_ratio)

        key = stdscr.getch()
        if key in (curses.KEY_BACKSPACE, 127):
            if current_input:
                current_input.pop()
        elif key == 27:
            break
        elif key in (10, 13):
            continue
        elif 32 <= key <= 126:
            current_input.append(chr(key))

    # End screen
    accuracy = round(((len(current_input) - errors) / max(len(current_input), 1)) * 100, 2)
    consistency = round(np.std(wpm_history), 2)
    typed_exit = ""

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Time's up! Final WPM: {wpm_val}")
        stdscr.addstr(1, 0, f"Errors: {errors}")
        stdscr.addstr(2, 0, f"Accuracy: {accuracy}%")
        stdscr.addstr(3, 0, f"Consistency (std dev): ±{consistency} WPM")
        stdscr.addstr(5, 0, 'Type "quit" to exit or press Ctrl+C')
        stdscr.addstr(7, 0, f"> {typed_exit}")
        stdscr.refresh()

        try:
            ch = stdscr.getch()
            if ch in (curses.KEY_BACKSPACE, 127):
                typed_exit = typed_exit[:-1]
            elif 32 <= ch <= 126:
                typed_exit += chr(ch)
            if typed_exit.strip().lower() == "quit":
                break
        except KeyboardInterrupt:
            break

curses.wrapper(monkeytype)
