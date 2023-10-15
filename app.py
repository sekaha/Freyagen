import curses


class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu = "intro"
        self.valid_chars = [
            ord(k) for k in "qwertyuiop[]\\asdf=-`1234567890ghjkl;'zxcvbnm,./"
        ]

        # loaded in from file in theory
        self.previous_text = [
            "q w e r t  y u i o p [ ] \\",
            "a s d f g  h j k l ; '",
            "z x c v b  n m , . / ",
        ]

        # coloring to show changes
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.run()

    def add_text(self, x, y, s, col=0):
        try:
            self.stdscr.addstr(x, y, s, col)
        except curses.error as e:
            assert ("Your terminal is too small for curses to operate", e)

    def run(self):
        curses.curs_set(1)  # Show cursor

        while True:
            if self.menu == "intro":
                self.intro()
            elif self.menu == "help":
                self.help_menu()
            elif self.menu == "edit":
                self.edit_menu()

    def intro(self):
        self.stdscr.clear()

        commands = {
            # "load <filename>": "loads a keyboard layout",
            "(l)ist": "lists all keyboard layouts saved",
            "(e)dit <layout>": "allows you to edit a keyboard layout",
            "(m)ake <layout>": "<layout> defaults to qwerty if not specified, loads a template and makes a new layout",
            "(g)enerate <layout>": "given a starting template attempts to generate a new layout",
            "(a)nalyze <layout>": "analyzes the given layout",
        }

        # To print the help_text with aligned hyphens, you can use the following code:
        max_length = max(len(key) for key in commands.keys())

        help_text = "You can use the first letter of every command as shorthand. \n"
        help_text += "-" * self.stdscr.getmaxyx()[1]  # + "\n"
        help_text += "\n".join(
            [
                f"{key.ljust(max_length)} - {value}"
                for key, value in sorted(commands.items(), key=lambda x: x[0])
            ]
        )

        intro_text = "Welcome to FreyaBoardApp uwu.\n\n" + help_text
        self.add_text(0, 0, intro_text)
        self.stdscr.refresh()

        input_window = curses.newwin(1, curses.COLS - 1, curses.LINES - 1, 1)
        input_window.addstr(0, 0, "> ")
        input_window.refresh()

        cmd = ""

        while True:
            key = input_window.getch()

            if key == 10:  # Enter
                if cmd in ["help", "h"]:
                    self.menu = "help"
                    break
                if cmd in ("make", "m"):
                    self.menu = "edit"
                    break
            elif key == 127:  # Backspace
                if cmd:  # Check if the command is not empty
                    cmd = cmd[:-1]
                    # Overwrite with a space
                    input_window.addch(0, len("> ") + len(cmd), " ")
                    input_window.move(0, len("> ") + len(cmd))  # Move the cursor back
            else:
                cmd += chr(key)
                input_window.addch(key)

        input_window.addstr(0, 0, "> " + cmd)  # Reprint the full command
        input_window.refresh()

    def help_menu(self):

        self.stdscr.clear()
        commands = {
            # "load <filename>": "loads a keyboard layout",
            "(l)ist": "lists all keyboard layouts saved",
            "(e)dit <layout>": "allows you to edit a keyboard layout",
            "(m)ake <layout>": "template defaults to qwerty if not specified, loads a template and makes a new layout",
            "(g)enerate <layout>": "given a starting template attempts to generate a new layout",
        }

        # To print the help_text with aligned hyphens, you can use the following code:
        max_length = max(len(key) for key in commands.keys())

        help_text = "You can use the first letter of every command as shorthand. \n"
        help_text += "-" * self.stdscr.getmaxyx()[1]  # + "\n"
        help_text += "\n".join(
            [f"{key.ljust(max_length)} - {value}" for key, value in commands.items()]
        )

        self.add_text(0, 0, help_text)
        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()

            if key == 27:  # escape key
                self.stdscr.clear()
                self.menu = "intro"
                break

    def edit_menu(self):
        self.stdscr.clear()

        text = [
            "q w e r t  y u i o p [ ] \\",
            "a s d f g  h j k l ; '",
            "z x c v b  n m , . / ",
        ]

        y_pos = 0
        x_pos = 0

        def shift_up():
            nonlocal y_pos, x_pos

            if y_pos > 0:
                y_pos -= 1
                x_pos = min(x_pos, len(text[y_pos]) - 1)

        def shift_down():
            nonlocal y_pos, x_pos

            if y_pos < (len(text) - 1):
                y_pos += 1
                x_pos = min(x_pos, len(text[y_pos]) - 1)

        def shift_right():
            nonlocal x_pos

            if x_pos < (len(text[y_pos]) - 1):
                x_pos += 1
            else:
                if y_pos < len(text) - 1:
                    x_pos = 0

                shift_down()

        def shift_left():
            nonlocal x_pos

            if x_pos > 0:
                x_pos -= 1
            else:
                if y_pos > 0:
                    x_pos = len(text[y_pos - 1]) - 1

                shift_up()
            self.stdscr.clear()

        while True:
            # Draw text to show how it has changed from loaded input
            for y, line in enumerate(text):
                for x, char in enumerate(line):
                    col = curses.color_pair(2)

                    if char == self.previous_text[y][x]:
                        col = curses.color_pair(1)

                    self.add_text(y, x, char, col)

            self.stdscr.move(y_pos, x_pos)
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == 27:  # escape key
                self.menu = "intro"
                break
            elif key == curses.KEY_BACKSPACE:
                shift_left()

                while text[y_pos][x_pos] == " ":
                    shift_left()

                # Insert 'c' at the current position if it's an 'x'
                current_line = list(text[y_pos])
                current_line[x_pos] = self.previous_text[y_pos][x_pos]
                text[y_pos] = "".join(current_line)
            elif key == curses.KEY_RIGHT or key == ord(" "):
                shift_right()

                while text[y_pos][x_pos] == " ":
                    shift_right()

                    if y_pos == len(text) - 1 and x_pos == len(text[len(text) - 1]) - 1:
                        break
            elif key == curses.KEY_LEFT:
                shift_left()

                while text[y_pos][x_pos] == " ":
                    shift_left()
            elif key == curses.KEY_DOWN:
                shift_down()
            elif key == curses.KEY_UP:
                shift_up()
            elif key in self.valid_chars:
                if not (
                    y_pos == len(text) - 1 and x_pos == len(text[len(text) - 1]) - 1
                ):
                    current_line = list(text[y_pos])
                    current_line[x_pos] = chr(key)
                    text[y_pos] = "".join(current_line)

                    shift_right()

                    while text[y_pos][x_pos] == " ":
                        shift_right()

                        if (
                            y_pos == len(text) - 1
                            and x_pos == len(text[len(text) - 1]) - 1
                        ):
                            break


if __name__ == "__main__":
    curses.wrapper(App)
