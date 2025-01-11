import random
from time import sleep
print("Hello, this is a simple number guessing game")
sleep(2)
print("Provide me a range of numbers and I'll try to guess!")
sleep(2)

n1  = int(input("Please enter the first number:"))
n2  = int(input("Please enter the second number:"))
sleep(1)
print(f"Now pick a number between {n1} and {n2}")
sleep(2)
print("I shall now guess it, If I'm right , type y, else type n")
numbers = [i for i in range(n1,n2+1)]

while True:
    print("thinking")
    sleep(1)
    print(".")
    sleep(1)
    print(".")
    number = random.choice(numbers)
    print(f"Is your number {number}?")
    ansr = input()
    if ansr == "y":
        print("I win, thank you for playing")
        break
    elif ansr == "n":
        numbers.remove(number)
        print("I'll try again")
    else:
        print("Invalid choice")
