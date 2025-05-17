from data_struct import Library
from console import str_to_func


def main():
    library = Library()
    print("Library system initialized. Type 'help' for commands.")
    while True:
        try:
            command = input("> ").strip()
            if command.lower() == "exit":
                print("Goodbye!")
                break
            str_to_func(command, library)
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
