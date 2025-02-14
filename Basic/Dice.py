'''
# Dice Roller Game

# Description
    Uses the random module to choose between numbers 1-6 and displays the number
    Doesn't require any external modules

# Usage
    After running the file, type "y" to roll the dice
    Type "n" after the dice is rolled to stop the program
'''

import random
numbers = [1,2,3,4,5,6]
while True:
    dice = random.choice(numbers)
    ansr = (input("Roll the dice? (y/n):"))
    if ansr != "y" and ansr != "n" :
        print("Invalid choice")
    elif ansr == "n":
        print("Thanks for playing")
        break
    else:
        print(dice)
