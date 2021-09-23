from treasure_hunt import *

cave = Cave()
cave.add_hazard(Hazard.guard, 1)
cave.add_hazard(Hazard.pit, 3)
cave.add_hazard(Hazard.bats, 3)

player = Player()
narrator = Narrator()
console = Console(player, narrator)

# add sense events

player.sense(Hazard.bats, lambda: narrator.say("You hear a rustling sound nearby"))
player.sense(Hazard.guard, lambda: narrator.say("You smell something terrible nearby"))
player.sense(Hazard.pit, lambda: narrator.say("You feel a cold wind blowing from a nearby cavern."))

# add encounter events

player.encounter(Hazard.guard, lambda: player.act(Action.startle_guard, player.room))
player.encounter(Hazard.pit, lambda: narrator.finish_story("You fell into a bottomless pit. Enjoy the ride!"))


def encounter_bats():
    narrator.say("Giant bats whisk you away to a new cavern!")
    old_room = player.room
    new_room = cave.random_room()
    player.enter(new_room)
    cave.move(Hazard.bats, old_room, new_room)


player.encounter(Hazard.bats, encounter_bats)

# add action events

player.action(Action.move, lambda destination: player.enter(destination))


def shoot(dest):
    if dest.has(Hazard.guard):
        narrator.finish_story("YOU KILLED THE GUARD! GOOD JOB, BUDDY!!!")
    else:
        narrator.say("Your arrow missed!")
        player.act(Action.startle_guard, cave.room_with(Hazard.guard))


player.action(Action.shoot, shoot)


def startle_guard(old_guard_room):
    if random.choice([Action.stay, Action.shoot]) == Action.move:
        new_guard_room = old_guard_room.random_neighbor()
        cave.move(Hazard.guard, old_guard_room, new_guard_room)
        narrator.say("You heard a rumbling in a nearby cavern.")


player.action(Action.startle_guard, startle_guard)

# kick off event loop

player.enter(cave.entrance())


def play():
    console.show_room_description()
    console.ask_player_to_act()


narrator.tell_story(play)
