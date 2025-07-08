'''
# Hangman Game

# Description
-This file creates a simple hangman game
-The output would be one of the many words stored in the "words.py" file
-The player must guess all the letters of the chosen words, where each wrong word would cost a life
-The game ends when the player either guesses the word or loses all their lives

# Usage
-In the "words.py" file exists a list of words, edit those list to add words according to your choice
-Add a hint in that file as well, this will be imported to the file we're on.
-Run this script, type a single letter, the program will give you an output of whether you're correct or not
'''

import words
import time
import random

print("This is the hangman game, your partner has made 4 words, you'll have to guess one of them")
time.sleep(3)
print(f"Hint: {words.hint}")
time.sleep(1)
print("You'll have 6 attempts (lives) to guess before you lose")
print("Ready?")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

def game():
    ansr = random.choice(words.fruits)
    correct_letters = set()
    used_letters = set()
    lives = 6
    ansr_letters = list(ansr)
    
    while lives > 0:
        output = ''.join([letter if letter in correct_letters else " _ " for letter in ansr_letters])
        print(f"Your word is {output}")
        
        if output==ansr:
            print("CONGRATULATIONS!!! you've guessed the word!")
            break
        
        m = input("Guess a letter:")
        n = m.upper()
                
        if n in used_letters:
            print("You've already guessed this letter")
            continue
        
        used_letters.add(n)
        
        
        if n in ansr_letters:
            print("Good guess")
            correct_letters.add(n)
            
        else:
            lives -=1
            print(f"Wrong guess you have {lives} lives left")
        
        if lives == 0:
            print("You've run out of lives :(")
            
game()
