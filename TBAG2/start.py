from character import Enemy, Character, Player
from room import Room

class Game_start():
    def __init__(self):
        self.player = None
        self.rooms = {
            "Entrance": Room("Entrance","A dark entryway full of cobwebs, dust, with a flickering light."),
            "Kitchen": Room("Kitchen", "A spooky kitchen with a haunting aroma."),
            "Ballroom": Room("Ballroom", "An elegant ballroom with ghostly music."),
            "Dining Hall": Room("Dining Hall", "A large dining hall filled with cobwebs."),
            "Primary Bedroom": Room("Primary Bedroom", "A dusty bedroom with an old bed."),
            "Bathroom": Room("Bathroom", "A grimy bathroom with flickering lights."),
            "Attic": Room("Attic", "A dark attic filled with old treasures."),
            "Basement": Room("Basement", "A damp basement that smells of mildew.")
        }

    def start_game(self):
        # NPC greets the player
        print("Welcome to the Haunted House!")
        print(self.information_npc.conversation)

        # Setup the player
        player_name = self.setup_player()
        chosen_weapons = self.choose_weapons()

        # Create the Player instance
        self.player = Player(player_name, chosen_weapons)

        # Choose starting location
        starting_location = self.choose_starting_room()

        # Now the player can start the game in the chosen room
        self.game_loop(starting_location)

    @staticmethod
    def setup_player():
        player_name = input("Enter your player's name: ")
        return player_name

    @staticmethod
    def choose_weapons():
        available_weapons = ["Wooden Stake", "Flamethrower", "Silver Dagger", "Magic Wand", "Crossbow", "Iron Darts"]
        print("Choose 2 weapons, and choose wisely: ")
        for index, weapon in enumerate(available_weapons, 1):
            print(f"{index}: {weapon}")

        chosen_weapons = []

        for _ in range(2):
            choice = int(input("Enter the number of your weapon choice: ")) - 1
            if 0 <= choice < len(available_weapons):
                chosen_weapons.append(available_weapons[choice])
            else:
                print("Invalid choice. Please choose again.")
                _ -= 1  # Repeat the loop for invalid choice

        return chosen_weapons

    def information_npc(self):
        moaning_myrtle = Character("Moaning Myrtle the Friendly Ghost", "A friendly ghost that offers you advice.")
        moaning_myrtle.set_conversation(
            "Hello you! Welcome to the haunted house! "
            "I guess I'll help you; you need to defeat enemies to collect keys and find the house deed. "
            "If you manage to find the deed you'll become the new homeowner and my cute housemate, hehehe. "
            "Or.... if you die, you'll be stuck with me forever, hehehe."
        )
        return moaning_myrtle

    @staticmethod
    def choose_starting_room():
        print("Where would you like to start?")
        starting_location = ["Kitchen", "Ballroom", "Dining Hall", "Primary Bedroom", "Bathroom", "Attic", "Basement"]

        for index, room in enumerate(starting_location):
            print(f"{index + 1}: {room}")

        choice = int(input("Choose a room number: ")) - 1
        if 0 <= choice < len(starting_location):
            return starting_location[choice]
        else:
            print("Invalid choice. Defaulting to Kitchen.")
            return starting_location[0]  # Default starting room.

    def game_loop(self, starting_location):
        current_room = self.rooms[starting_location]
        print(f"You enter the {current_room.name}.")
        
        while True:
            command = input("> ").lower()
            if command == "check inventory":
                self.player.check_inventory()
            elif command == "display weapons":
                self.player.display_weapons()
            elif command.startswith("move"):
                room_name = command.split("move ")[-1].title()  # Extract room name from command
                self.move_to_room(room_name, current_room)
            else:
                print("Unknown command. Try again.")

    def move_to_room(self, room_name, current_room):
        # Check if the room exists
        if room_name in self.rooms:
            # Check if the player has the key for the room
            if self.player.has_key(room_name):
                current_room = self.rooms[room_name]
                print(f"You move to the {current_room.name}.")
            else:
                print(f"You need the key to enter the {room_name}.")
        else:
            print("That room doesn't exist.")

