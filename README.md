# Homework Assignment 1

## Learning Outcomes

After completion of this assignment, you should be able to:

- Prototype in Python.

- Work with Python data structures.

- Design object-oriented structures.

## Getting Started

To complete this homework assignment, you will need Python3.8 and above and the testing framework Pytest. These should have already been setup if you did homework 0. If you did not do homework 0, now is a good time to first do homework 0 and come back here. You can use any test editor or IDE (e.g., Pycharm) to write your python code.

Read the rest of the document carefully. This document describes everything that you will need to correctly implement the homework and submit the code for testing.

The first thing you need to do is download or clone this repository to your local system. Use the following command:

`$ git clone <ssh-link>`

After you clone, you will see a directory of the form *cise337-hw1-python-basics-\<username\>*, where *username* is your GitHub username.

In this directory, you will find a file named *treasure_hunt.py*. You will write your code in this file. This file has some starter code and empty class stubs. You will have to implement the empty class stubs. At the top of the file you will find hints to fill your full name, NetID, and SBU ID. Please fill them accurately. This information will be used to collect your scores from GitHub. If you do not provide this information, your submission may not be graded. The *treasure_hunt_test.py* file has the test cases for this homework. You can use the test cases as specifications to guide your code. Your goal should be to pass all the tests. If you do so, then you are almost guaranteed to get full credit. The test file should not be modified. If you do, you will receive no credit for the homework.


## How to read the test cases

As mentioned previously, the *treasure_hunt_test.py* file contains the test cases. Each test case is a method in the class *TestTreasureHunt* prefixed with *test_*. In each of these methods, you will find assert statements that need to be true for the test to pass. These asserts compare the expected result with the result obtained by invoking certain methods or referencing certain attributes in your implementation. If a test fails, the name of the failing test will be reported with an error message. You can use the error message from the failing test to diagnose and fix your errors.

*Do not change the test file. If you do then you won't receive any credit for this homework assignment*.

## Problem Specification

In this assignment, we will develop the prototype of a game called treasure hunt. Recall that one of the use cases of scripting is that it allows us to quickly prototpe an application. This game takes place in an underground cave full of interconnected rooms. One of the rooms has treasure hidden in it. Other rooms in the cave have various hazards in them. The goal is to reach the treasure room avoiding the hazardous rooms. If a player reaches the treasure room, they win. If they encounter a hazard in their search for treasure, they die and lose the game.

A player in this game can take only two actions: move to adjacent rooms, or to
shoot arrows into nearby rooms in an attempt to kill the guard protecting the
treasure. Until the player knows where the treasure is, most of the time a player
will end up moving from room to room to understand the cave’s layout. Shown below is an example cave layout.

![cave-0](./images/cave-layout-ex.png)

Here is an example of how the game may proceed.

```
You are in room 1.
Exits go to: 2, 8, 5
-----------------------------------------
What do you want to do? (m)ove or (s)hoot? m
Where? 2
-----------------------------------------
You are in room 2.
Exits go to: 1, 10, 3
-----------------------------------------
What do you want to do? (m)ove or (s)hoot? m
Where? 10
-----------------------------------------
You are in room 10.
Exits go to: 2, 11, 9
```

After a player takes a couple of actions, they can begin to understand the topography of the cave. For example, the player knows that in this particular cave layout, one can go from room 1 to room 2 and from room 2 to room 10. This is highlighted in the above figure thru red edges.

Play continues in this fashion until the player encounters a hazard.

```
What do you want to do? (m)ove or (s)hoot? m
Where? 11
-----------------------------------------
You are in room 11.
Exits go to: 10, 8, 20
-----------------------------------------
What do you want to do? (m)ove or (s)hoot? m
Where? 20
-----------------------------------------
You are in room 20.
You feel a cold wind blowing from a nearby cavern.
Exits go to: 11, 19, 17
```

In this case, the player has managed to get close to a room with a bottomless pit,
which is detected by the presence of cold wind emanating from one of the adjacent
rooms. Since hazards are sensed indirectly, the player needs a sensing mechanism to detect the rooms with hazards. Based on the topography of the cave known so far, the
only two rooms with potential hazards are rooms 17 and 19. One of them might be
safe or both might have hazards.

At this point, the player might guess a safe room. However, that would be too
risky. The wise thing to do would be to backtrack and try another route:

```
What do you want to do? (m)ove or (s)hoot? m
Where? 11
-----------------------------------------
You are in room 11.
Exits go to: 10, 8, 20
-----------------------------------------
What do you want to do? (m)ove or (s)hoot? m
Where? 8
-----------------------------------------
You are in room 8.
You smell something terrible nearby
Exits go to: 11, 1, 7
```

Changing directions worked! On entering room 8, the terrible smell suggests that
the guard protecting the treasure is nearby. Spending years in the cave has given
the guard a peculiar stench. Luckily, the player has already visited rooms 1 and 11.
Hence, the only other adjacent room 7 must contain the treasure:

```
What do you want to do? (m)ove or (s)hoot? s
Where? 7
-----------------------------------------
YOU KILLED THE GUARD! GOOD JOB, BUDDY!!!
```

The game ends there. At this point the player’s map would look like:

![cave-1](./images/cave-layout-ex-1.png)

The player could have encountered other hazards in a room such as giant bats,
which would have moved the player to a random room. Since such factors are
randomized, every time this game is played a new cave map would be encountered.

### Implementation Details

You need to implement this game by defining methods in the following classes:

- A *Room* class to manage hazards and connections between rooms.
- A *Cave* class to navigate the topography of the cave.
- A *Player* class to handle the player's moves and senses.

#### Modeling A Room

The *Room* class must have the following attributes:

- *number*. A unique number to identify the room.
- *hazards*. A list of hazards the room may contain.
- *neighbors*. A list of neighbors adjacent to the room in the cave.

The *Room* class must have the following methods:

- *add(hazard)* for adding a hazard to the list of hazards in the room.
- *has(hazard)* to check if a hazard is in the room. It should return *True* if the hazard is in the room and *False* otherwise.
- *remove(hazard)* for removing an existing hazard from the room. Removing a non-existent hazard should result in a *ValueError* exception.
- *empty()* for checking if the room has hazards. Should return *True* if room has no hazards and *False* otherwise.
- *safe()* for checking if the room is safe. A room is deemed safe if it has no hazards and none of its neighbors have hazards. Should return *True* if a room is safe and *False* otherwise.
- *connect(other_room)* for connecting rooms in a cave. This method should connect this room to *other_room* and vice-versa. The method must use the *neighbors* attribute to make the connection.
- *exits()* for identifying the rooms to this room in the cave. The method should return a list of numbers indicating the all the adjacent rooms. Should return empty list if the room has no adjacent rooms.
- *neighbor(number)* for getting a room adjacent to this room is the cave. The method should return a room with room number *number* adjacent to this room. Should return *None* if no room with *number* is adjacent to this room.
- *random_neighbor()* for getting a random room adjacent to this room in the cave. The method should return a random room from the list of rooms adjacent to this room. If the room has no neighbors, then the method should raise an *IndexError*. You may use the *random* module for this operation.

A *Room class* stub has been provided for you in *treasure_hunt.py*. Your job is to complete the class definition based on the requirements outlined above.

#### Modeling The Cave

Although this game can be played with any arbitrary cave layout, we will make
things simpler to better focus on designing the steps of the game. Hence, we will
assume a dodecahedron cave layout. In this layout, a room is placed at each vertex,
and the edges form the connections between rooms. We can visualize the layout as
follows:

![dodeca](./images/dodeca.png)

The *Cave* class must have the following attributes:

- *edges* a list of lists [x,y], where x and y are room numbers. For the purpose of simplicity, you can assume that the cave has room numbers 1 to 20 (inclusive).
- *rooms* a dictionary with room number N as key and Room(N) as the corresponding value.

Further, the layout of the cave should be initialized with the rooms connected to its neighbors when an instance of class *Cave* is initialized.

The *Cave* class must have the following methods:

- *add_hazard(hazard, count)* should add a *hazard* to multiple rooms in the cave indicated by *count*. You can select the rooms in the cave randomly or using a heuristic. For example, if *count* is 3, then the *hazard* should be added to 3 unique rooms in the cave.
- *random_room()* should return a random room in the cave. You can use the *random* module in Python.
- *room_with(hazard)* should return the first room in the cave with the *hazard*. Should return *None* if no room with the *hazard* exists in the cave.
- *move(hazard, frm, to)* should move the *hazard* from room indicated by *frm* to another room in the cave indicated by *to*. If the *hazard* does not exist in the *frm* room, then raise a *ValueError*. After the operation, the *hazard* should be in the *to* room and not in the *frm* room.
- *room(number)* should return a room in the cave with the room number *number*. Raise a *KeyError* is no room with that number exists in the cave.
- *entrance()* should return a room in the cave that is safe. Recall that a room is safe if it has no hazards and none of its neighbors have an hazards.

A *Cave class* stub has been provided for you in *treasure_hunt.py*. Your job is to complete the class definition based on the requirements outlined above.

#### Modeling A Player

Most events in this treasure hunt game are triggered by conditions based on the
player’s location. For example, imagine that the player is in Room 1 and the
neighboring rooms are rooms 2,3, and 4. Also, room 2 has the guard, room 3 has
bats, and room 4 is empty. With this setup, the player would sense the nearby
hazards, resulting in the following:

```
You are in room 1.
You hear a rustling sound nearby
You smell something terrible nearby
Exits go to: 2, 3, 4
```

In this example, the player’s possible outcomes would be as follows:

- The player will encounter the guard upon moving to room 2.
- The player will encounter bats upon moving to room 3.
- The player will not encounter any hazards in room 4.
- The player can shoot into room to kill the guard and access the treasure.
- The player will miss by shooting into rooms 3 or 4.    

By now, you must have realized that the player’s events can be easily generalized
into the following:
- The player can sense hazards.
- The player can encounter hazards.
- The player can perform actions on neighboring rooms such move to a neighboring room or shoot an arrow into the next room.

With these requirements, we can now model the Player class as an event-driven
object that handles each event type or requirement listed above. The only state it
explicitly needs to maintain is a reference to the room currently being explored; everything else can be managed externally via callback methods.

To model the event-driven behavior of a Player class, we will first define the following attributes in the *Player* class:

- The *senses* dictionary where the key is a hazard and the callback is a method that will be executed when the player senses a hazard.
- The *encounters* dictionary where the key is a hazard and the callback is a method that will be executed when the player encounters a hazard.
- The *actions* dictionary where the key is a player action and the callback is a method that will be executed when the player performs that action (e.g., move to a neighboring room).
- The *room* attribute the record the room the player is currently in.

Next, we will define the following methods in the *Player* class to model the event-driven behavior of  player:

- *sense(hazard, callback)* should record the callback method associated with the hazard in *senses*. This method/event is triggered when a player senses a hazard in a neighboring room.
- *encounter(hazard, callback)* should record the callback method associated with the hazard in *encounters*. This method/event is triggered when a player encounters a hazard in the room that the player enters.
- *action(act, callback)* should record the callback method associated with the player's act in *actions*. This method/event is triggered when a player performs an action (such as shoot an arrow to a room).
- *enter(room)* should change the player's current room to the room the player is entering indicated by the *room* argument. If a player encounters a hazard in this room, then return the result of encountering the hazard from the method.
- *explore_room()* should allow a player to explore the neighbors of the current room. If the player senses a hazard in a neighboring room, it should invoke the callback method associated with the hazard.
- *act(action, destination)* should allow a player to perform an action on a destination room. An action is generally move to a *destination* room or shoot an arrow at a *destination* room.

A *Player class* stub has been provided for you in *treasure_hunt.py*. Your job is to complete the class definition based on the requirements outlined above.

#### Playing The Game

To help you imagine the game, this repository contains some starter code in *run_treasure_hunt.py* and the classes *Narrator* and *Console* in *treasure_hunt.py*. On running the *run_treasure_hunt/py* script, a player enters the cave as specified in line 61 in *run_treasure_hunt.py*. Next, the script calls the *play* function from the *Narator* class's *tell_story()* method as shown in line 69 of *run_treasure_hunt.py*. If you correctly implement the *Cave*, *Room*, and *Player* classes, you should be able to run the game from *run_treasure_hunt.py*.

## Submitting Code to GitHub

You can submit code to your GitHub repository as many times as you want till the deadline. After the deadline, any code you try to submit will be rejected. To submit a file to the remote repository, you first need to add it to the local git repository in your system, that is, directory where you cloned the remote repository initially. Use following commands from your terminal:

`$ cd /path/to/cise337-hw1-python-basic-<username>` (skip if you are already in this directory)

`$ git add treasure_hunt.py`

To submit your work to the remote GitHub repository, you will need to commit the file (with a message) and push the file to the repository. Use the following commands:

`$ git commit -m "<your-custom-message>"`

`$ git push`

Every time you push code to the GitHub remote repository, the test cases in the *test* file will run and you will see either a green tick or a red cross in your repository just like you saw with homework0. Green tick indicates all tests passed. Red cross indicates some tests failed. Click on the red cross and open up the report to view which tests failed. Diagnose and fix the failed tests and push to the remote repository again. Repeat till all tests pass or you run out of time!

## Running Test Cases Locally

It may be convenient to run the test cases locally before pushing to the remote repository. To run a test locally use the following command:

`$ pytest treasure_hunt_test.py`

This command assumes that you are in the local repository directory and pytest is installed. If you do not have the right setup it is most likely because you did not do homework 0 correctly. So, do homework 0 first and then come back here!
