import random
import words
from termcolor import cprint

# Globals to help printing in colors easier 
yellow = lambda x: cprint(x, "black", 'on_yellow')
green = lambda x: cprint(x, 'black', 'on_green')
red = lambda x: cprint(x, 'black', 'on_red')

# Choose a word from a file of over 5000 words: https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt
def get_word() -> str:
    return random.choice(words.word_list)

# Checks if guess is 5 characters and is only letters
def is_guess_valid(guess: str, i: int) -> str:
    if guess == 'Q':
        return guess
    if len(guess) == 5 and guess.isalpha():
        return str(guess) # Valid guess
    else:
        red("5 Letters only!")
        new_guess = input(f'Guess {i + 1} / 5: ').upper()
        return is_guess_valid(new_guess, i)

def color_letters(guess: str, answer: str):
    colors = {}
    temp = list(answer)
    # First go through and look for greens, and edit temp list of letters from answer
    
    for i, letter in enumerate(guess):
        if letter == answer[i]: # If letter is in the right place, make it green
            colors[i] = 'green'
            temp[i] = '_' # In the temp list, replace the letter
    i = 0 # Reset i for the next loop, because I like using i
    # 2nd time through, if corresponding index isn't green
    for i, letter in enumerate(guess):
        if colors.get(i) != 'green':
            if letter in temp: # This means it is in the word but not at the correct spot, and doesn't check greens
                colors[i] = 'yellow' # Make it yellow
                temp[temp.index(letter)] = '_' # Replace that letter with '_'
            else:
                colors[i] = 'red' # The letter is not in the word, make it red
    return colors

def print_table(g_list: list, colors_list: list): 
    # Print the table with guesses and their corresponding colors
    print('---------------')
    for i in range(len(g_list)):
        for c in range(len(g_list[i])):
            color = colors_list[i].get(c)
            if color == 'green':
                cprint(' ' + g_list[i][c] + ' ','white', on_color='on_green', end='')
            elif color == 'yellow':
                cprint(' ' + g_list[i][c] + ' ','white', on_color='on_yellow', end='')
            else:
                cprint(' ' + g_list[i][c] + ' ','white', on_color='on_red', end='')
            if (c + 1) % 5 == 0 and c > 0:
                print() # Newline after each guess prints
        print('---------------')
    
    # Check if the user won
    if all(letter == 'green' for letter in colors_list[-1].values()):
        return True
    else:
        return False

# Begin the game
def main():
    cprint('Welcome to FAKE WORDLE', 'cyan')
    cprint('Submit "q" to quit', 'light_blue')
    # Select the random word: 
    answer = get_word().upper()
    g_list = []
    colors_list = []
    won = False
    
    for i in range(5): # 5 guesses! 
        # Ask user for guess (Must be 5 letters)
        guess = str(input(f"Guess {i + 1} / 5: ")).upper()
        valid_guess = is_guess_valid(guess, i)
        # Check if user wants to quit
        if (valid_guess == 'Q'): 
            break
        g_list.append(valid_guess) # Add all guesses to a list
        
        # Create the colors dictionary
        colors = color_letters(valid_guess, answer)
        colors_list.append(colors)
        # Print the table, check if the user won
        won = print_table(g_list, colors_list)
        
        if won:
            cprint('YOU WIN!!', 'green')
            break
        
    cprint(f"The word was: {answer.upper()}", 'green') # After win or quit, show the word. 

if __name__ == '__main__':
    main()
    
