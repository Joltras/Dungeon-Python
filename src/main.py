import os.path
from datetime import datetime

from generators.Generator import Generator
from generators.PygameGenerator import PygameGenerator
import sys
import secrets
import Globals

HELP_MESSAGE = """Creates a dungeon floor and saves it to a json file.
Options:
    -h, --help: Prints this message.
    -s, --seed: Sets the seed for the random number generator.
    -o, --output: Sets the output file name, default is output.json.
    -u, --ui: Enables the UI, default is disabled.
    -f --floor: Sets the id for the floor, default is 0. (Must be 0 or greater)
    """


def main(seed: str, output: str, ui: bool, floor_id):
    output_folder = os.path.join(Globals.APPLICATION_PATH, "generation")
    output  = os.path.join(output_folder, output)


    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        print("No output folder found. Creating specific folder")

    if ui:
        generator = PygameGenerator(seed, output, floor_id)
        generator.run()
    else:
        generator = Generator(seed, output, floor_id)
        generator.generate()
        generator.save()
        print("Floor saved to " + output)


if __name__ == '__main__':
    seed: str = ""
    output: str = ""
    show_ui: bool = False
    floor_id: int = 0
    i: int = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-s" or sys.argv[i] == "--seed":
            if i + 1 < len(sys.argv):
                seed = sys.argv[i + 1]
                i += 1
        elif sys.argv[i] == "-u" or sys.argv[i] == "--ui":
            show_ui = True
        elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print(HELP_MESSAGE)
            exit(0)
        elif sys.argv[i] == "-o" or sys.argv[i] == "--output":
            if i + 1 < len(sys.argv):
                output = sys.argv[i + 1]
                i += 1
        elif sys.argv[i] == "-f" or sys.argv[i] == "--floor":
            if i + 1 < len(sys.argv):
                try:
                    floor_id = int(sys.argv[i + 1])
                    i += 1
                    if floor_id < 0:
                        print("The floor id must be greater than 0!")
                        exit(-1)
                except ValueError:
                    print(sys.argv[i + 1] + " is not a valid number!")
                    exit(-1)
        else:
            print(sys.argv[i] + " is not a valid argument!")
            exit(-1)
        i += 1

    if seed == "":
        seed = secrets.token_hex(16)
    if output == "":
        time = str(datetime.now().microsecond)
        output = time + ".json"
    if not output.endswith(".json"):
        output += ".json"

    main(seed, output, show_ui, floor_id)
