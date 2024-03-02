# Python Dungeon Generator
This is a simple dungeon generator.
It uses a simple algorithm to generate a random dungeon. 
The algorithm is based of the generator from the game "The Binding of Isaac"
which is described in this [article](https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/).

## Usage
The dungeon generator can be used with an ui or without.
The ui is a simple pygame window which shows the generated dungeon.
It also can be used as a rest endpoint.

## Generated Dungeon
The dungeon gets generated as a json file.
The json file contains the following information:
- The seed the dungeon was generated with
- Width and height of the dungeon
- The floor layout
  - A list of all rooms
  - Each room contains the following information
    - The room id
    - The room type
    - x and y position
    - a list of all door positions

### Room Types
- 0: Normal Room
- 1: Dead End
- 2: Item Room
- 3: Shop
- 4: Start Room
- 5: Teleport Room