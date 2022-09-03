from Generator import Generator
import sys
import secrets

HELP_MESSAGE = """Creates a dungeon floor and saves it to a json file.
Options:
    -h, --help: Prints this message.
    -s, --seed: Sets the seed for the random number generator.
    -o, --output: Sets the output file name, default is output.json.
    -u, --ui: Enables the UI, default is disabled."""

def main(seed: str, output: str, ui: bool):
    generator = Generator(seed, output, ui)
    if ui:
        generator.run()
    else:
        generator.generate()
        generator.save()
        print("Floor saved to " + output)


if __name__ == '__main__':
    seed: str = ""
    output: str = ""
    show_ui: bool = False
    i: int = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-s" or sys.argv[i] == "--seed":
            if i + 1 < len(sys.argv):
                seed = sys.argv[i + 1]
                i += 1
        elif sys.argv[i] == "-u" or sys.argv[i] == "--ui":
            show_ui = True
            i += 1
        elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print(HELP_MESSAGE)
            exit(0)
        elif sys.argv[i] == "-o" or sys.argv[i] == "--output":
            if i + 1 < len(sys.argv):
                output = sys.argv[i + 1]
                i += 1
        i += 1

    if seed == "":
        seed = secrets.token_hex(16)
    if output == "":
        output = "output.json"

    main(seed, output, show_ui)
