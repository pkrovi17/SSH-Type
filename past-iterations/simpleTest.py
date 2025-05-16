import curses
import random
import time

WORDS = ["banana", "monkey", "jungle", "keyboard", "speed", "typing", "python", "swing", "tree", "leaf", "jump", "grip", "hang", "code", "linux", "shell", "space", "focus"]
NUM_WORDS = 30

def draw_text(stdscr, target_words, current_input, word_index, errors):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    x, y = 0, 0
    char_index = 0
    flat_input = ''.join(current_input)

    for i, word in enumerate(target_words):
        highlight = curses.color_pair(3) if i == word_index else curses.A_NORMAL
        for j, char in enumerate(word):
            if x >= width:
                y += 1
                x = 0
            if char_index < len(flat_input):
                typed_char = flat_input[char_index]
                if typed_char == char:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)
                stdscr.attron(color | highlight)
                stdscr.addch(y, x, typed_char)
                stdscr.attroff(color | highlight)
            else:
                stdscr.attron(highlight)
                stdscr.addch(y, x, char)
                stdscr.attroff(highlight)
            x += 1
            char_index += 1
        if x < width:
            stdscr.addch(y, x, ' ')
            x += 1
            char_index += 1

    stdscr.addstr(y + 2, 0, f"Errors: {errors}")
    stdscr.refresh()

def wpm(char_count, elapsed):
    return round((char_count / 5) / (elapsed / 60))

def monkeytype(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(16)  # ~60fps

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # incorrect
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW) # highlight

    target_words = random.choices(WORDS, k=NUM_WORDS)
    current_input = []
    errors = 0
    word_index = 0
    started = False

    while True:
        if not started:
            stdscr.clear()
            stdscr.addstr(0, 0, "Monkeytype TUI – Press any key to start typing!")
            stdscr.refresh()
            stdscr.getch()
            start_time = time.time()
            started = True

        flat_target = ' '.join(target_words)
        draw_text(stdscr, target_words, current_input, word_index, errors)

        try:
            key = stdscr.getch()
        except:
            key = -1

        if key == -1:
            continue  # no input

        if key in (curses.KEY_BACKSPACE, 127):
            if current_input:
                current_input.pop()
        elif key == 27:  # ESC
            break
        elif key in (10, 13):  # Enter
            break
        elif 32 <= key <= 126:
            current_input.append(chr(key))

        typed = ''.join(current_input)
        errors = sum(1 for i in range(len(typed)) if i < len(flat_target) and typed[i] != flat_target[i])

        word_index = typed.count(' ')

        if typed == flat_target or len(typed) >= len(flat_target):
            break

    elapsed = max(time.time() - start_time, 1)
    stdscr.clear()
    stdscr.addstr(0, 0, f"Done! WPM: {wpm(len(flat_target) - errors, elapsed)}")
    stdscr.addstr(1, 0, f"Errors: {errors}")
    stdscr.addstr(2, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(monkeytype)
