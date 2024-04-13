import random
import words
from termcolor import cprint
# from rich.console import Console
# console = Console()

GUESSES = []
COLORS = []
WON = 0
yellow = lambda x: cprint(x, "black", 'on_yellow')
green = lambda x: cprint(x, 'black', 'on_green')
red = lambda x: cprint(x, 'black', 'on_red')
# def green(text):
#     console.print(text, style="green")

# def yellow(text):
#     console.print(text, style="yellow")

# def red(text):
#     console.print(text, style="red")

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
    # Ask user for guess (Must be 5 letters)
    g_list = []
    for i in range(5):
        guess = str(input(f"Guess {i + 1}: ")).upper()
        if (guess == 'Q'):
            break
        guess = is_guess_valid(guess, i)
        g_list.append(guess)
        color_letters(guess, answer)
        print_table(g_list, i)
        if WON: 
            break
    cprint(f"The word was: {answer.upper()}", 'green')

# Checks if guess is 5 characters and is only letters
def is_guess_valid(guess: str, i: int) -> str:
    if len(guess) == 5:
        if guess.isalpha():
            return str(guess)
        else:
            red("Letters only!")
            new_guess = input(f'Guess {i + 1}: ')
            return is_guess_valid(new_guess, i)
    else:
        red("5 characters!")
        new_guess = input(f'Guess {i + 1}: ')
        return is_guess_valid(new_guess, i)

def color_letters(guess: str, answer: str):
    global COLORS
    word = list(guess)
    ans = list(answer)
    colors = {}
    temp = list(answer)
    for i, letter in enumerate(word):
        if letter == ans[i]: 
            colors[i] = 'green' #in the right place
            temp[i] = '_'
    i = 0
    for i, letter in enumerate(word):
        if colors.get(i) != 'green':
            if letter in temp:
                colors[i] = 'yellow'
                temp[temp.index(letter)] = '_'
            else:
                colors[i] = 'red'
    COLORS.append(colors)

def print_table(g_list: list, g_num: int):
    global GUESSES
    global WON
    global COLORS
    w = list(g_list[g_num])
    temp = '' # to build word to add to GUESSES list. 
    for letter in w:
        temp += (f'{letter}')
    GUESSES.append(temp)
    print('---------------')
    for i in range(g_num + 1):
        for c in range(len(GUESSES[i])): # print table char by char
            color = COLORS[i].get(c)
            if color == 'green':
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_green', end='')
            elif color == 'yellow':
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_yellow', end='')
            else:
                cprint(' ' + GUESSES[i][c] + ' ','white', on_color='on_red', end='')
            if (c + 1) % 5 == 0 and c > 0:
                print()
        print('---------------')
    if all(letter == 'green' for letter in COLORS[g_num].values()):
        cprint('YOU WIN!!', 'green')
        WON = 1

if __name__ == '__main__':
    main()
    
