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