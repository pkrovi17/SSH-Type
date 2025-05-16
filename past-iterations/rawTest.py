import curses
import random
import time

WORDS = ["banana", "monkey", "jungle", "keyboard", "speed", "typing", "python", "swing", "tree", "leaf", "jump", "grip", "hang", "code", "linux", "shell", "space", "focus"]
NUM_WORDS = 50

def draw_text(stdscr, target_words, current_input, word_index, errors, wpm_val, elapsed, cursor_pos, cursor_visible):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x, y = 0, 0
    char_index = 0
    flat_target = ' '.join(target_words)
    flat_input = ''.join(current_input)

    for i, word in enumerate(target_words):
        highlight = curses.color_pair(3) if i == word_index else curses.A_NORMAL
        for j, char in enumerate(word):
            if x >= width:
                y += 1
                x = 0
            color = highlight
            if char_index < len(flat_input):
                typed_char = flat_input[char_index]
                if typed_char == char:
                    color |= curses.color_pair(1)
                else:
                    color |= curses.color_pair(2)
            if char_index == cursor_pos and cursor_visible:
                color |= curses.A_REVERSE
            stdscr.attron(color)
            stdscr.addch(y, x, char)
            stdscr.attroff(color)
            x += 1
            char_index += 1
        if x < width:
            color = highlight
            if char_index < len(flat_input):
                typed_char = flat_input[char_index]
                if typed_char == ' ':
                    color |= curses.color_pair(1)
                else:
                    color |= curses.color_pair(2)
            if char_index == cursor_pos and cursor_visible:
                color |= curses.A_REVERSE
            stdscr.attron(color)
            stdscr.addch(y, x, ' ')
            stdscr.attroff(color)
            x += 1
            char_index += 1

    stdscr.addstr(y + 2, 0, f"Errors: {errors}")
    stdscr.addstr(y + 3, 0, f"WPM: {wpm_val}")
    stdscr.addstr(y + 4, 0, f"Time: {int(elapsed)}s")
    stdscr.refresh()

def calculate_wpm(correct_chars, elapsed):
    return round((correct_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0

def monkeytype(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(16)

    # Amber theme colors
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)     # correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)        # incorrect
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)     # highlight

    target_words = random.choices(WORDS, k=NUM_WORDS)
    current_input = []
    errors = 0
    word_index = 0
    started = False
    start_time = None

    blink_interval = 0.5
    last_blink = time.time()
    cursor_visible = True

    while True:
        if not started:
            stdscr.clear()
            stdscr.addstr(0, 0, "Monkeytype TUI – Press any key to start typing!")
            stdscr.refresh()
            stdscr.getch()
            start_time = time.time()
            started = True

        # Fake blinking
        if time.time() - last_blink >= blink_interval:
            cursor_visible = not cursor_visible
            last_blink = time.time()

        now = time.time()
        elapsed = max(now - start_time, 0)
        typed = ''.join(current_input)
        flat_target = ' '.join(target_words)

        correct_chars = sum(1 for i in range(min(len(typed), len(flat_target))) if typed[i] == flat_target[i])
        errors = sum(1 for i in range(len(typed)) if i < len(flat_target) and typed[i] != flat_target[i])
        wpm_val = calculate_wpm(correct_chars, elapsed)
        word_index = typed.count(' ')
        cursor_pos = len(current_input)

        draw_text(stdscr, target_words, current_input, word_index, errors, wpm_val, elapsed, cursor_pos, cursor_visible)

        try:
            key = stdscr.getch()
        except:
            key = -1

        if key == -1:
            continue
        if key in (curses.KEY_BACKSPACE, 127):
            if current_input:
                current_input.pop()
        elif key == 27:  # ESC
            break
        elif key in (10, 13):  # Enter
            break
        elif 32 <= key <= 126:
            current_input.append(chr(key))

        if typed == flat_target or len(typed) >= len(flat_target):
            break

    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(0, 0, f"Finished! Final WPM: {wpm_val}")
    stdscr.addstr(1, 0, f"Errors: {errors}")
    stdscr.addstr(2, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(monkeytype)
