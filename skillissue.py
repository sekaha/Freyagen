import curses


def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()

    intro_text = "Welcome to the Hello World CLI. Type 'hello' to print 'Hello, World!', 'load <filename>' to load and display a file, or 'exit' to quit."
    stdscr.addstr(0, 0, intro_text)
    stdscr.refresh()

    input_window = curses.newwin(1, curses.COLS - 1, curses.LINES - 1, 1)
    input_window.addstr(0, 0, "> ")
    input_window.refresh()

    command = ""

    while True:
        c = input_window.getch()

        if c == 10:  # Enter key
            if command == "exit":
                break
            elif command.startswith("hello"):
                stdscr.addstr(2, 0, "Hello, World!")
            elif command.startswith("load"):
                filename = command[5:].strip()
                try:
                    with open(filename, "r") as file:
                        contents = file.read()
                        stdscr.addstr(3, 0, f"Contents of {filename}:\n{contents}")
                except FileNotFoundError:
                    stdscr.addstr(3, 0, f"File not found: {filename}")
                except Exception as e:
                    stdscr.addstr(3, 0, f"An error occurred: {str(e)}")
            else:
                stdscr.addstr(2, 0, f"Unknown command: {command}")
            input_window.clear()
            input_window.addstr(0, 0, "> ")
            command = ""
        else:
            command += chr(c)
            input_window.addch(c)

        stdscr.refresh()
        input_window.refresh()


curses.wrapper(main)
