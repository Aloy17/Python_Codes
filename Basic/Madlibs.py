import time
print("Hello, this is a simple madlibs program, all you have to do is enter some words and a story will be generated using those words")

adj = input("Enter an adjective:")
sname = input("Enter a silly name:")
pnoun = input("Plural noun:")
v = input("A verb, using past tense:")
food = input("Type of food:")
b = input("A body part:")
adv = input("An adverb:")
excl = input("An exclamation:")
vpr = input("Another verb,present tense:")
animal = input("An animal:")

str = int(input("1 or 2?"))
print("Loading story")
time.sleep(1)
print(".")
time.sleep(1)
print(".")
time.sleep(1)
print(".")

story = f"""
The {adj} Adventures of Captain {sname}
Captain {sname} was known for his collection of {pnoun}. One day, he {v} to the store to buy more {food}. On his way, he tripped over his own {b} and {adv} fell into a puddle. "{excl}!" he shouted as he tried to {vpr} out of the water. Suddenly, a giant {animal} appeared and laughed at the soggy captain. It was just another typical day in the life of the legendary Captain {sname}.
"""

story2 = f"""
Once upon a time, there was a {adj} person named {sname}. They loved to collect {pnoun} 
and often {v} them in their spare time. One day, while eating {food}, {sname} had a 
brilliant idea. They decided to use their {b} to {adv} create a new invention. 

"{excl}!" they shouted, "I'll {vpr} a machine that turns everything into a {animal}!"

And so, {sname}'s adventure began, filled with {adj} surprises and lots of {pnoun}.
"""

if str == 1:
        print(story)
else:
    print(story2)