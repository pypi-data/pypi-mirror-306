import argparse
import curses
import os
from typing import List
from context_curse.thing import Thing


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Thank you for checking out Context Curse...\n a CLI tool for managing files and directories before feeding them into a LLM with a limited context window.")
    parser.add_argument('-e', '--extensions', type=str,
                        help='Comma-separated extensions to keep (e.g., "py,txt").')
    parser.add_argument('-i', '--input', type=str,
                        help='Path to text file with input preferences.')
    parser.add_argument('-o', '--output', type=str,
                        help='Path to output text file for saving selections.')
    return parser.parse_args()


def load_input_preferences(input_path: str) -> List[str]:
    '''should be a file with a list of paths to keep, one per line.'''
    with open(input_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]


def curses_app(stdscr: 'curses.window', root: Thing, output_path: str):
    curses.curs_set(0)
    selected_index = 0
    expanded_dirs = set()  # Track which directories are expanded
    page_size = 10

    def get_visible_things() -> List[Thing]:
        """Get a list of visible things based on the expanded state."""
        visible = []

        def add_visible_children(thing: Thing, depth: int):
            visible.append((thing, depth))
            if thing.get_path() in expanded_dirs and thing.is_directory():
                for child in thing.get_children():
                    add_visible_children(child, depth + 1)

        add_visible_children(root, 0)
        return visible

    def render():
        stdscr.clear()

        # Add tool description and commands at the top
        tool_description = (
            "#####################\n"
            "Context Curse - Manage your files and directories before feeding into an LLM\n"
            "  Commands:\n"
            "    ↑/↓: Navigate\n"
            "    Enter: Select/Deselect\n"
            "    Space: Expand/Collapse\n"
            "    s: Save selections\n"
            "    q: Quit\n"
            "  Legend:\n"
            "    >: Selected\n"
            "    \\: Directory\n"
            "    Green: Kept\n"
            "    Yellow: Mixed\n"
            "    White: Not kept\n"
            "#####################\n"
        )

        # Draw tool description in cyan/blue
        stdscr.attron(curses.color_pair(7))  # Cyan/Blue color pair
        stdscr.addstr(0, 0, tool_description)
        stdscr.attroff(curses.color_pair(7))

        things_to_display: List[Thing] = get_visible_things()
        num_items = len(things_to_display)

        # Determine the range of items to display
        start_index = max(0, selected_index - page_size // 2)
        end_index = min(num_items, start_index + page_size)

        # Calculate the index offset for the top indicator
        tool_description_lines = len(tool_description.split('\n'))
        indicator_line_index = tool_description_lines

        # Add scroll indicators if needed
        if num_items > page_size:
            # Add "..." at the top if there are items above the visible range
            if start_index > 0:
                stdscr.addstr(indicator_line_index, 0,
                              "...", curses.color_pair(7))
            # Add "..." at the bottom if there are items below the visible range
            if end_index < num_items:
                stdscr.addstr(curses.LINES - 1, 0, "...", curses.color_pair(7))

        # Display the visible items
        for idx, (thing, depth) in enumerate(things_to_display[start_index:end_index]):
            display_idx = idx + indicator_line_index + \
                (1 if start_index > 0 else 0)

            # Highlight the selected item
            if idx + start_index == selected_index:
                mark = ">"
            else:
                mark = ""

            if thing.is_directory():
                suffix = "\\"
            else:
                suffix = ""

            if thing.get_keep() and thing.get_children_keep():
                c = 2
            elif thing.get_keep() is None:
                c = 3
            else:
                c = 1

            color_pair = curses.color_pair(c)
            stdscr.attron(color_pair)
            # Add indentation based on the depth
            stdscr.addstr(
                display_idx, 0, f"{mark}{'    ' * depth}{thing.get_path()}{suffix}")
            stdscr.attroff(color_pair)

        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Kept
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Mixed
    # Selected, not kept
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_GREEN,
                     curses.COLOR_WHITE)  # Selected, kept
    curses.init_pair(6, curses.COLOR_YELLOW,
                     curses.COLOR_WHITE)  # Selected, mixed
    # Cyan/Blue for tool_description
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def confirm_action(action: str) -> bool:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Are you sure you want to {action}? (y/n)")
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == ord('y'):
                return True
            elif key == ord('n'):
                return False

    while True:
        things_to_display: List[Thing] = get_visible_things()
        num_items = len(things_to_display)
        # Ensure start_index and end_index are valid
        start_index = max(0, selected_index - page_size // 2)
        end_index = min(num_items, start_index + page_size)

        try:
            render()
        except curses.error:
            pass

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if selected_index > 0:
                selected_index -= 1
                if selected_index < start_index:
                    start_index = max(0, selected_index - page_size // 2)
                    end_index = min(num_items, start_index + page_size)
        elif key == curses.KEY_DOWN:
            if selected_index < len(things_to_display) - 1:
                selected_index += 1
                if selected_index >= end_index:
                    end_index = min(num_items, selected_index + 1)
                    start_index = max(0, end_index - page_size)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Access Thing object
            selected_thing: Thing = things_to_display[selected_index][0]
            selected_thing.set_keep(not selected_thing.get_keep())
        elif key == ord('s'):
            if confirm_action("save"):
                save_selections(root, output_path)
                generate_massive_file(
                    output_path, output_path.replace(".txt", "_massive.txt"))
        elif key == ord('q') or key == ord('Q'):
            if confirm_action("quit"):
                break
        elif key == ord(' '):  # Space bar toggles expansion/collapse
            # Access Thing object
            selected_thing = things_to_display[selected_index][0]
            if selected_thing.is_directory():
                if selected_thing.get_path() in expanded_dirs:
                    expanded_dirs.remove(selected_thing.get_path())
                else:
                    expanded_dirs.add(selected_thing.get_path())
        try:
            render()
        except curses.error:
            pass


def save_selections(root: Thing, output_path: str):
    # Clear the file if root
    if root.get_parent() is None:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('')

    for i, thing in enumerate(root.get_children()):
        if thing.get_keep():
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(f"{thing.get_path()}\n")
        if thing.get_children():
            save_selections(thing, output_path)


def apply_input_preferences(root: Thing, input_preferences: List[str]):
    """
    Apply the input preferences to the Thing tree, setting the keep status
    based on whether the path is in the input preferences.
    """

    def update_keep_status(thing: Thing):
        # Set keep status based on whether this thing's path is in input_preferences
        path = thing.get_path()
        if path in input_preferences:
            thing.set_keep(True)
        else:
            thing.set_keep(False)

        # Recursively update children
        for child in thing.get_children():
            update_keep_status(child)

    # Start from the root and update the entire tree
    update_keep_status(root)


def generate_massive_file(input_file_path: str, output_file_path: str):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Write a header for the paths list
        output_file.write("# paths\n")

        # Read each path from the input file
        for path in input_file:
            path = path.strip()  # Remove any leading/trailing whitespace

            if os.path.isdir(path):
                # If it's a directory, just comment its path
                output_file.write(f"# {path}\n")
            elif os.path.isfile(path):
                # If it's a file, include its contents
                output_file.write(f"\n# {path}\n")
                with open(path, 'r', encoding='utf-8') as content_file:
                    output_file.write(content_file.read())
                output_file.write("\n")
            else:
                pass
                # Handle case where the path does not exist
                # output_file.write(f"# {path} (Path does not exist)\n")


def main():
    args: argparse.Namespace = parse_arguments()

    # Parse extensions
    file_ext = args.extensions.split(',') if args.extensions else []

    if args.input:
        input_preferences = load_input_preferences(args.input)
    else:
        input_preferences = []

    root_thing = Thing('.', file_types=file_ext, ignore=[])

    # Apply input preferences before starting the curses app
    apply_input_preferences(root_thing, input_preferences)

    output_path = args.output if args.output else 'context_curse.txt'

    curses.wrapper(curses_app, root_thing, output_path)

if __name__ == "__main__":
    main()
