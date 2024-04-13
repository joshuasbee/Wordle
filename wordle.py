import random
import words
from termcolor import cprint

GUESSES = []
COLORS = []
WON = 0
# Globals to help printing in colors easier 
yellow = lambda x: cprint(x, "black", 'on_yellow')
green = lambda x: cprint(x, 'black', 'on_green')
red = lambda x: cprint(x, 'black', 'on_red')

# Choose a word from a file of over 5000 words: https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt
def get_word() -> str:
    return random.choice(words.word_list)

# Begin the game
def main():
    global WON
    cprint('Welcome to FAKE WORDLE', 'cyan')
    cprint('Submit "q" to quit', 'light_blue')
    # Select the random word: 
    answer = get_word().upper()
    g_list = []
    for i in range(5): # For 5 guesses
        guess = str(input(f"Guess {i + 1} / 5: ")).upper() # Ask user for guess (Must be 5 letters)
        if (guess == 'Q'):
            break # Ends the game
        guess = is_guess_valid(guess, i)
        g_list.append(guess) # To allow the printing of previous guesses along with newest guess
        color_letters(guess, answer) # Create the coloring dictionary
        print_table(g_list, i) # Print it to the console
        if WON: 
            break
    cprint(f"The word was: {answer.upper()}", 'green') # After win or quit, show the word. 

# Checks if guess is 5 characters and is only letters
def is_guess_valid(guess: str, i: int) -> str:
    if len(guess) == 5:
        if guess.isalpha():
            return str(guess) # good guess, 5 characters, and only letters. 
        else:
            red("Letters only!")
            new_guess = input(f'Guess {i + 1} / 5: ') # New guess needed
            return is_guess_valid(new_guess, i) # Recursive call, check if its good again. 
    else:
        red("5 characters!")
        new_guess = input(f'Guess {i + 1} / 5: ') # Need a new guess, 
        return is_guess_valid(new_guess, i) # Recursive call, check if new guess is valid.

def color_letters(guess: str, answer: str):
    global COLORS
    word = list(guess)
    ans = list(answer)
    colors = {}
    temp = list(answer)
    # First go through and look for greens, and edit temp list of letters from answer
    for i, letter in enumerate(word):
        if letter == ans[i]: # If letter is in the right place, make it green
            colors[i] = 'green'
            temp[i] = '_' # In the temp list, replace the letter
    i = 0 # Reset i for the next loop, because I like using i
    # 2nd time through, if corresponding index isn't green
    for i, letter in enumerate(word):
        if colors.get(i) != 'green':
            if letter in temp: # This means it is in the word but not at the exact same spot, and doesn't check greens
                colors[i] = 'yellow' # Make it yellow
                temp[temp.index(letter)] = '_' # Replace that letter with '_'
            else:
                colors[i] = 'red' # The letter is not in the word, make it red
    COLORS.append(colors) # add the new color dictionary to a list of dictionaries, to allow printing old guesses

def print_table(g_list: list, g_num: int): # g_num represents which number guess the user is on
    global GUESSES
    global WON
    global COLORS
    word = list(g_list[g_num])
    temp = '' # to build word to add to GUESSES list. 
    for letter in word:
        temp += (f'{letter}') # Build the word from the corresponding guess in the guess list (g_list)
    GUESSES.append(temp) # Add it to the list of guesses
    print('---------------')
    for i in range(g_num + 1): # This loop is to print each previous guess
        for c in range(len(GUESSES[i])): # This loop prints each guess in the corresponding color. 
            color = COLORS[i].get(c)
            if color == 'green':
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_green', end='')
            elif color == 'yellow':
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_yellow', end='')
            else:
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_red', end='')
            if (c + 1) % 5 == 0 and c > 0:
                print() # After printing the entire word, print a newline
        print('---------------')
    if all(letter == 'green' for letter in COLORS[g_num].values()): # If the letters are all green, you got the word
        cprint('YOU WIN!!', 'green')
        WON = 1 # Flag to exit loop in main()

if __name__ == '__main__':
    main()
    
