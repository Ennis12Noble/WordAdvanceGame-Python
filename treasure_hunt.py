############ Xiaoling Xie ############
########### 114185864 ############
########### xiaolxie ############
import random
from enum import Enum

# Defines possible hazards in the game.
class Hazard(Enum):
    guard = "Guard"
    pit = "Pit"
    bats = "Bats"


# Defines possible actions a player can take.
class Action(Enum):
    move = "move"
    shoot = "shoot"
    stay = "stay"
    startle_guard = "startle_guard"


class Cave:
    def __init__(self):
        self.edges = [[1, 2], [2, 10], [10, 11], [11, 8], [8, 1], [1, 5], [2, 3], [9, 10], [20, 11], [7, 8], [5, 4],
                      [4, 3], [3, 12], [12, 9], [9, 19], [19, 20], [20, 17], [17, 7], [7, 6], [6, 5], [4, 14], [12, 13],
                      [18, 19], [16, 17], [15, 6], [14, 13], [13, 18], [18, 16], [16, 15], [15, 14]]
        rooms = {}
        for i in range(1,21):
            rooms[i] = Room(i)  # a dictionary with room number N as key and Room(N) as the corresponding value.

        ll = [[0] * 21 for _ in range(21)]
        for i in self.edges:
            ll[i[0]][i[1]] = 1
            ll[i[1]][i[0]] = 1

        for i in range(1,21):
            for j in range(1, 21):
                if ll[j][i] == 1:
                    rooms[j].neighbors.append(rooms[i])
                    rooms[i].neighbors.append(rooms[j])
        for i in range(1,21):
            rooms[i].neighbors = list(set(rooms[i].neighbors))

        # copyEdges = self.edges
        # for j in range(20):
        #     for i in copyEdges:
        #         if j in i and len(i)>1:
        #             i.remove(j)
        #             rooms[j-1].neighbors.append(rooms[i[0]-1])
        #             rooms[i[0]-1].neighbors.append(rooms[j-1])

        self.rooms = rooms

    def add_hazard(self, thing, count):
        for i in random.sample(range(1,21),count):
            self.rooms[i].add(thing)

    def random_room(self):
        return self.rooms[random.choice(range(1,21))]

    def room_with(self, thing):
        for i in range(1,21):
            if not self.rooms[i].empty():
                return self.rooms[i]

    def move(self, thing, frm, to):
        if not frm.empty():
            frm.remove(thing)
            to.add(thing)
        else:
            raise ValueError


    def room(self, number):
        if self.rooms[number]:
            return self.rooms[number]
        else:
            raise KeyError

    def entrance(self):
        for i in range(1,21):
            if self.rooms[i].safe():
                return self.rooms[i]


class Room:
    def __init__(self, number):
        self.number = number # A unique number to identify the room
        self.hazards = []   # A list of hazards the room may contain.
        self.neighbors = []

    def has(self, thing):
        return thing in self.hazards    # check if a hazard is in the room. It should return True if the hazard is in the room and False otherwise

    def add(self, thing):
        self.hazards.append(thing)  # add a hazard to the list of hazards in the room.

    def remove(self, thing):
        if thing in self.hazards:
            self.hazards.remove(thing)  # remove an existing hazard from the room.
        else:
            raise ValueError


    def empty(self):    # check if the room has hazards. Should return True if room has no hazards and False otherwise.
        if self.hazards:
            return False
        else:
            return True

    def safe(self): # check if the room is safe. Should return True if a room is safe and False otherwise.
        for i in self.neighbors:
            if i.empty() == False:
                return False
        if self.empty() == False:
            return False
        else:
            return True

    def connect(self, other_room):
        self.neighbors.append(other_room)
        other_room.neighbors.append(self)

    def exits(self):
        numbers = []
        if self.neighbors:
            for i in self.neighbors:
                numbers.append(i.number)
        return numbers

    def neighbor(self, number):
        for i in self.neighbors:
            if i.number == number:
                return i
        return None

    def random_neighbor(self):
        if self.neighbors:
            return random.choice(self.neighbors)
        else:
            raise IndexError


class Player:
    def __init__(self):
        self.senses = dict()
        self.encounters = dict()
        self.actions = dict()
        # self.room = Room(1)

    def sense(self, thing, callback):
        self.senses[thing] = callback

    def encounter(self, thing, callback):
        self.encounters[thing] = callback

    def action(self, thing, callback):
        self.actions[thing] = callback

    def enter(self, room):
        self.room = room
        if not room.empty():
            for k in self.encounters:
                if k in self.room.hazards:
                    self.encounters[k]()
                    return
            # for i in room.hazards:
            #     self.encounters[i]()
            #     return

    def explore_room(self):
        for i in self.room.neighbors:
            if not i.empty():
                for j in i.hazards:
                    self.senses[j]()

    def act(self, action, destination):
        self.actions[action](destination)



class Narrator:
    def __init__(self):
        self.ending_message = None

    def say(self, message):
        print(message)

    def ask(self, question):
        return input(question)

    def tell_story(self, story):
        while not self.ending_message:
            story()
        self.say("-----------------------------------------")
        self.say(self.ending_message)

    def finish_story(self, message):
        self.ending_message = message


class Console:
    def __init__(self, player, narrator):
        self.player = player
        self.narrator = narrator

    def show_room_description(self):
        self.narrator.say("-----------------------------------------")
        self.narrator.say("You are in room #" + str(self.player.room.number))
        self.player.explore_room()
        self.narrator.say("Exits go to: " + ",".join([str(x) for x in self.player.room.exits()]))

    def ask_player_to_act(self):
        actions = {"m": Action.move, "s": Action.shoot}
        self.accepting_player_input(
            lambda command, room_number: self.player.act(actions[command], self.player.room.neighbor(room_number)))

    def accepting_player_input(self, act):
        self.narrator.say("-----------------------------------------")
        command = self.narrator.ask("What do you want to do? (m)ove or (s)hoot?")
        if command not in ["m", "s"]:
            self.narrator.say("INVALID ACTION! TRY AGAIN!")
            return
        try:
            dest = int(self.narrator.ask("Where?"))
            if dest not in self.player.room.exits():
                self.narrator.say("INVALID ACTION! TRY AGAIN!")
                return
        except ValueError:
            self.narrator.say("INVALID ACTION! TRY AGAIN!")
            return
        act(command, dest)
