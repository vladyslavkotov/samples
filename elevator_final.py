import time,os,random

'''
A simple elevator simulation. It is a "Lift" problem on Codewars, just animated. Run from a console to get the best animation.
'''

os.system('cls')

top_floor = 10
height = range(1, top_floor + 1)
max_load = 5
inside = []
load = len(inside)
outside = {x: [] for x in reversed(height)}  # create empty list for each floor
left = {x: [] for x in reversed(height)}

current_floor = random.randint(1, top_floor)
sleep=1.5
direction=0 #this should change depending on destination
destination_up=0
destination_down=0

def display():
    for x in reversed(height):
        if x == current_floor:
            print(f"{x : <3} {str(left[x]) : <25}  {str(inside) : <20} {str(outside[x]) : >20}")
        else:
            print(f"{x : <3} {str(left[x]) : <25}   {str(outside[x]) : >40}")
    print(f'position {current_floor} load {load} direction {direction} destinations {destination_up}/{destination_down}')
    print('_____________________________________')
    time.sleep(sleep)
    os.system('cls')

for floor in height:
    people = random.randint(2, 3)
    batch = []
    for x in range(people):
        floor_range = [y for y in height if y != floor]  # any floor except current floor choice range
        exit = random.choice(floor_range)
        batch.append(exit)
    outside[floor] = batch

display()

while True:

    display()
    for x in inside[:]:
        if x == current_floor:
            left[current_floor].append(x)
            inside.remove(x)
            load -= 1

    display()

    if direction==0: #we do not know where we going. starting point
        if outside[current_floor]:
            inside.append(outside[current_floor][0])
            outside[current_floor].pop(0)
            load+=1
            if inside[0]<current_floor:
                direction=-1
                display()
            else:
                direction = 1
                display()
        else:
            direction = random.choice([1, -1])
    #if it spawned on empty floor, how does it decide where to go?

    if direction !=0: #we are already going somewhere, keep going until it reaches destination
        if outside[current_floor]:
            for x in outside[current_floor][:]:
                if direction == 1 and load<max_load:
                    if x > current_floor:
                        inside.append(x)
                        outside[current_floor].remove(x)
                        load += 1
                elif direction==-1 and load<max_load:
                    if x < current_floor:
                        inside.append(x)
                        outside[current_floor].remove(x)
                        load += 1

    display()

    non_empty_floors=[x for x,y in outside.items() if y]

    destination_up=max(non_empty_floors+inside)
    destination_down = min(non_empty_floors+inside)

    if direction == 1:
        if current_floor<destination_up: #we need 2nd condition to make sure it doesnt go past max floor with ppl
            current_floor += 1
        elif current_floor>=destination_up:
            direction =-1 #we can change dir right away, do not wait for 1st guy to come in and determine.
            #it's highest point already, nowhere to go but turn around

    elif direction == -1:
        if current_floor>destination_down:
            current_floor -= 1
        elif current_floor<=destination_down:
            direction =1


