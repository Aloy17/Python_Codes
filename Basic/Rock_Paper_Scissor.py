import random
from time import sleep

print("This is a simple rock paper scissors game")
sleep(1)
print("When I say 'GO' you must type r for rock, s for scissors or p for paper")

while True:
    win = {"r":"s","s":"p","p":"r"}
    answers = ["r","p","s"]
    comp = random.choice(answers)
    print("3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)

    print("GO")
    user = input("rock paper scissors:")

    print(f"Your choice {user}")
    sleep(1)
    print(f"Computer choice {comp}")


    if user not in answers:
        print("Invalid choice")
    elif user == comp:
        print("Draw")
        sleep(1)
    elif win[user] == comp:
        print("You win")
        sleep(1)
    else:
        print("You lose")
        sleep(1)

    n = input("Play again? (y/n):")
    if n == "n":
        break

