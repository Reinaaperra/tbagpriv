# Class imports
from room import Room
from character import Enemy, Character, Player
from item import Item
from start import Game_start

class Game:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.room_descriptions_shown = {}

    def enter_room(self, room):
        self.current_room = room

        # Show room description only once
        if self.current_room not in self.room_descriptions_shown:
            print(self.current_room.description)
            self.room_descriptions_shown[self.current_room] = True

        self.current_room.interact_with_character()
        self.handle_player_actions()

    def handle_player_actions(self):
        inhabitant = self.current_room.get_character()

        while True:
            # Interaction display for player commands
            print("\nType the following commands, so you can:")
            print("- Search the room for items = Search")
            print("- Talk to the character = Talk")
            print("- Offer a bribe to the character if you have items = Bribe")
            print("- Fight the character = Fight")
            print("- Move = North/South/East/West/Up/Down")

            print(f"\n{self.current_room.get_description()}")
            command = input("> ").strip().lower()

            if command in ["north", "south", "east", "west", "up", "down"]:
                next_room = self.current_room.move(command, player_inventory)

                if next_room:  
                    # Check if a key is required and if the player has it
                    if next_room.get_key_required() and not next_room.can_enter(player_inventory):
                        print(f"You need the {next_room.get_key_required().get_name()} to enter this room.")
                    else:
                        self.enter_room(next_room)
                else:
                    print("You can't go that way!")


            elif command == "search":
                print("Searching for items...")
                self.current_room.search_room()
                if self.current_room.items:
                    for item in self.current_room.items:
                        print(f"Found {item.get_name()} ({item.get_category()}) - {item.get_description()}")
                        category = item.get_category().lower()
                        if category in player_inventory:
                            player_inventory[category].append(item)
                            print(f"{item.get_name()} has been added to your inventory")
                        else:
                            print(f"Warning: Category '{category}' not found in player inventory!")
                    self.current_room.items.clear()
                else:
                    print("No items found in this room!")

            elif command == "talk" and inhabitant is not None:
                inhabitant.talk()

            elif command == "fight":
                try:
                    print("Which weapon will you use?")
                    for index, weapon in enumerate(player_inventory["weapons"], start=1):
                        print(f"{index}. {weapon.get_name()} (weapons): {weapon.get_description()}")

                    weapon_choice = int(input("> ")) - 1  # Adjust for zero-indexing
                    if 0 <= weapon_choice < len(player_inventory["weapons"]):
                        selected_weapon = player_inventory["weapons"][weapon_choice]  # Select the weapon object, not the name
                        selected_weapon_name = selected_weapon.get_name()  # Get the weapon's name
                        # Proceed with the fight logic using selected_weapon_name
                        if inhabitant.fight(selected_weapon_name):
                            acquired_items = inhabitant.inventory
                            for item in acquired_items:
                                if item.get_category() == 'key':
                                    player_inventory['key'].append(item)
                                elif item.get_category() == 'loot':
                                    player_inventory['loot'].append(item)
                            item_names = ', '.join(item.get_name() for item in acquired_items)
                            print(f"You have defeated {inhabitant.name} and acquired: {item_names}!")
                            print(f"Current inventory: {player_inventory}")
                            self.current_room.set_character(None)
                        else:
                            print(f"{inhabitant.name} has defeated you. Game over.")
                            return  # End the game loop if the player loses
                    else:
                        print("Invalid choice. Please select a valid weapon number.")
                except (IndexError, ValueError):
                    print("Invalid weapon choice format, try again entering Weapon number!")

            elif command == "bribe" and inhabitant is not None:
                print("Available bribe items:")
                bribe_items = player_inventory['bribes']
                if bribe_items:
                    for item in bribe_items:
                        print(f"- {item.name} ({item.category}): {item.description}")
                else:
                    print("You have no items to bribe with.")
                    continue

                bribe_choice = input("Which item will you use to bribe? ").strip()
                for item in bribe_items:
                    if item.name == bribe_choice.lower():
                        if inhabitant.accept_bribe(item):
                            print(f"You bribed {inhabitant.name} with {item.name}!")
                            player_inventory['bribes'].remove(item) 
                            break
                else:
                    print(f"{inhabitant.name} does not want that item.")
            else:
                print("Invalid command. Please try again.")

def main():
    # Asks for the player's name
    player_name = Game_start.setup_player()
    print(f"Welcome to the Haunted House, {player_name}!")

    chosen_weapons = Game_start.choose_weapons()
    starting_location = Game_start.choose_starting_room()

    global player_inventory
    player_inventory = {
        "weapons": chosen_weapons,
        "key": [], 
        "tool": [],
        "loot": [],
        "bribes": []
    }

    # Room instances created
    entrance = Room("Entrance","A dark entryway full of cobwebs, dust, with a flickering light.")
    kitchen = Room("Kitchen", "A dank and dirty room buzzing with flies.")
    ballroom = Room("Ballroom", "A vast room with a shiny wooden floor.")
    dining_hall = Room("Dining Hall", "A large room with ornate golden decorations.")
    primary_bedroom = Room("Primary Bedroom", "A bedroom decorated like it's stuck in Victorian times, with a pungent stench.")
    bathroom = Room("Bathroom","A large bathroom with a leaking sink, clogged toilet, and carpet on the floor.")
    attic = Room("Attic", "Cramped attic, with floorboards missing and a bat flying around.")
    basement = Room("Basement", "Massive space with another flickering light, broken oil lamp, and a stale mattress in the corner.")

    # Set keys required for each room
    kitchen_key = Item(item_name= "Key to Kitchen", item_category="key", item_description="Unlocks the Kitchen")
    bathroom_key = Item(item_name="Key to Bathroom", item_category="key", item_description="Unlocks the Bathroom door")
    ballroom_key = Item(item_name="Key to Ballroom", item_category="key", item_description="Unlocks the Ballroom")
    dining_hall_key = Item(item_name="Key to Dining Hall", item_category="key", item_description="Unlocks the Dining Hall")
    bedroom_key = Item(item_name="Key to Primary Bedroom", item_category="key", item_description="Unlocks the Primary Bedroom")
    attic_key = Item(item_name="Key to Attic", item_category="key", item_description="Unlocks the Attic")
    basement_key = Item(item_name="Key to Basement", item_category="key", item_description="Unlocks the Basement")

    player_inventory["key"].append(kitchen_key)
    player_inventory["key"].append(bathroom_key)
    player_inventory["key"].append(ballroom_key)
    player_inventory["key"].append(dining_hall_key)
    player_inventory["key"].append(bedroom_key)
    player_inventory["key"].append(attic_key)
    player_inventory["key"].append(basement_key)

    # Set keys required for each room
    kitchen.set_key_required(kitchen_key)
    ballroom.set_key_required(ballroom_key)
    dining_hall.set_key_required(dining_hall_key)
    primary_bedroom.set_key_required(bedroom_key)
    bathroom.set_key_required(bathroom_key)
    attic.set_key_required(attic_key)
    basement.set_key_required(basement_key)


    # Link rooms together
    kitchen.link_room(ballroom, "south")
    kitchen.link_room(dining_hall, "east")
    dining_hall.link_room(kitchen, "west")
    dining_hall.link_room(primary_bedroom, "south")
    primary_bedroom.link_room(dining_hall, "north")
    primary_bedroom.link_room(ballroom, "west")
    primary_bedroom.link_room(attic, "up")
    ballroom.link_room(kitchen, "north")
    ballroom.link_room(primary_bedroom, "east")
    ballroom.link_room(basement, "down")
    attic.link_room(primary_bedroom, "down")
    basement.link_room(ballroom, "up")

    # Set the starting room
    current_room = entrance  
    if starting_location == "Kitchen":
        current_room = kitchen
    elif starting_location == "Ballroom":
        current_room = ballroom
    elif starting_location == "Dining Hall":
        current_room = dining_hall
    elif starting_location == "Primary Bedroom":
        current_room = primary_bedroom
    elif starting_location == "Bathroom":
        current_room = bathroom
    elif starting_location == "Attic":
        current_room = attic
    elif starting_location == "Basement":
        current_room = basement

    # Items in the game
    sleep_potion = Item("Sleep Potion", "tool", "Special Potion that puts Enemies to sleep!")
    wooden_stake = Item("Wooden Stake", "weapons", "Long Wooden Spike")
    flamethrower = Item("Flamethrower", "weapons", "Shoots fire from long distance.")
    crossbow = Item("Crossbow","weapons", "Made out of special material")
    magic_immortality_ring = Item("Magic Immortality Ring", "loot", "Live forever if you wear the ring, unless you get killed or take it off!")
    pig_brain = Item("Pig Brain", "bribes", "Big Juicy Pig Brain!")
    blood_vial = Item("Blood Vial", "bribes", "Deep Red Healthy Blood.")
    magicwand = Item("Magic Wand", "weapons", "The spell will come to you when needed")
    silverdagger = Item("Silver Dagger", "weapons", "Aim well")
    irondarts = Item("Iron Darts", "weapons", "More useful than you would think!")

    # Adding items to rooms
    kitchen.add_item(sleep_potion)
    kitchen.add_item(crossbow)
    ballroom.add_item(flamethrower)
    ballroom.add_item(silverdagger)
    dining_hall.add_item(wooden_stake)
    dining_hall.add_item(magicwand)
    dining_hall.add_item(irondarts)
    bathroom.add_item(pig_brain)
    attic.add_item(blood_vial)

    # Creation of enemies
    limbless_larry = Enemy("Limbless Larry", "A smelly zombie", inventory=[bedroom_key])
    roaslie = Enemy("Rosalie", "An unhinged fledgling!", inventory=[ballroom_key])
    casper = Enemy("Casper the Ghost", "Not the friendly type, but a hungry spirit", inventory=[dining_hall_key])
    belatrix = Enemy("Belatrix", "A deranged witch with a cackle", inventory=[attic_key])
    frankenstein = Enemy("Frankenstein", "A terrifying creature", inventory=[basement_key])
    gary = Enemy("Gary the Goblin", "A 6ft hideous, nosepicking cretin",inventory=[bathroom_key])

    # Assigning enemies to rooms
    kitchen.set_character(roaslie)
    ballroom.set_character(casper)
    dining_hall.set_character(limbless_larry)
    primary_bedroom.set_character(belatrix)
    basement.set_character(frankenstein)
    attic.set_character(gary)

    # Set weaknesses
    limbless_larry.set_weakness("Flamethrower")
    roaslie.set_weakness("Wooden Stake")
    casper.set_weakness("Crossbow")
    belatrix.set_weakness("Magic Wand")
    frankenstein.set_weakness("Silver Dagger")
    gary.set_weakness("Iron Darts")

    # Adding Loot
    roaslie.add_to_inventory(magic_immortality_ring)

    # Starting the game loop
    game = Game(current_room)
    game.enter_room(current_room)

if __name__ == "__main__":
    main()