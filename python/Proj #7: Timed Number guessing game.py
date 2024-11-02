import random
import time

def game():
    hint_used = False
    for i in range(5):
        number_to_guess = random.randint(1, 100) 
        guess = None

        start_time = time.time()
        while guess != number_to_guess:
            guess = int(input("Guess a number between 1 and 100: "))
            if guess < number_to_guess:
                print("Too low!")
            elif guess > number_to_guess:
                print("Too high!")

            # Give a hint if the user has previously asked for it
            if hint_used:
                if number_to_guess <= 50:
                    print("Hint: The number is 50 or less.")
                else:
                    print("Hint: The number is more than 50.")
            
            # Offer a hint if not used yet
            elif not hint_used:
                hint = input("Do you want a hint? Y/N: ").upper()
                if hint == 'Y':
                    hint_used = True
                    if number_to_guess <= 50:
                        print("Hint: The number is 50 or less.")
                    else:
                        print("Hint: The number is more than 50.")
                    start_time += 10  # Reduce remaining time by 10 seconds

            # Check if 30 seconds have passed
            if time.time() - start_time > 30:
                print("Sorry, you've run out of time.")
                return

        print("Congratulations! You've guessed the number.")

game()
