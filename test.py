import random

def guess_the_number():
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)

    attempts = 0
    previous_guess = 100
    lower = True
    list = {0, 0, 0, 0, 0, 0}
    while True:
        try:
            # Get the player's guess
            #guess = int(input("Enter your guess: "))
            guess = guess_algorythm(previous_guess, lower)
            previous_guess = guess

            # Increment the attempts
            attempts += 1

            # Check if the guess is correct
            if guess == secret_number:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
            elif guess < secret_number:
                lower = False
                print("Too low. Try again.")
            else:
                lower = True
                print("Too high. Try again.")
            list = queue(list, guess)
            print(list)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        if attempts > 100:
            break
def queue(list, to_add):
    list_new = [len(list)]
    list_new[-1] = to_add
    for i in range(len(list)-1, 1):
        list_new[i-1] = list[i]
    return list_new

def guess_algorythm(prev_guess, lower):
    if lower:
        if prev_guess%2 == 0:
            new_guess = prev_guess/2
        else:
            new_guess = (prev_guess-1)/2 
    else:
        if prev_guess%2 == 0:
            new_guess = prev_guess + prev_guess/2
        else:
            new_guess = prev_guess + (prev_guess-1)/2        

    return new_guess

if __name__ == "__main__":
    guess_the_number()

