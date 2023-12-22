import curses


def main(stdscr):
    menu = "edit"
    stdscr.clear()
    curses.curs_set(1)  # Show cursor
    stdscr.refresh()

    text = [
        "q w e r t  y u i o p [ ] \\",
        "a s d f g  h j k l ; '",
        "z x c v b  n m , . /",
    ]

    y_pos = 0
    x_pos = 0

    while True:
        stdscr.clear()
        key = stdscr.getch()

        if menu == "main":
            stdscr.addstr(0, 0, "Type e to edit, l to load")

            stdscr.move(y_pos, x_pos)
            stdscr.refresh()

            if key == ord("e"):
                menu = "edit"
        elif menu == "edit":
            for i, line in enumerate(text):
                stdscr.addstr(i, 0, line)

            stdscr.move(y_pos, x_pos)
            stdscr.refresh()

            current_line = list(text[y_pos])

            if key == curses.KEY_EXIT:
                menu == "main"
            elif key == curses.KEY_RIGHT:
                if x_pos < len(text[y_pos]):
                    x_pos += 1

                while current_line[x_pos] == " ":
                    x_pos += 1
            elif key == curses.KEY_LEFT:
                if x_pos > 0:
                    x_pos -= 1

                    while current_line[x_pos] == " ":
                        x_pos -= 1
            elif key == curses.KEY_DOWN:
                if y_pos < len(text) - 1:
                    y_pos += 1
                    x_pos = min(x_pos, len(text[y_pos]))
            elif key == curses.KEY_UP:
                if y_pos > 0:
                    y_pos -= 1
                    x_pos = min(x_pos, len(text[y_pos]))
            else:
                # Insert 'c' at the current position if it's an 'x'
                current_line[x_pos] = chr(key)
                text[y_pos] = "".join(current_line)


if __name__ == "__main__":
    curses.wrapper(main)

r . c d g  j h b o u
l i s m t  k y n a e
x , w q z  f v p ; /

h r c d g  j b u o .
y l s m t  k n e a i
v x w q z  f p / ; ,