#Here is my player class to help display the three players in the game.
class gamePlayers:
    def __init__(self, name):
        self.name = name
        self.money = 0
    def totalMoney(self, total):
        self.money = self.money + total
    def bankrupt(self):
        self.money = 0
    def person(self):
        return (self.name, self.money)
    def getMove(self, category, obscuredPhrase, guessed):
        print(f'{self.name} has ${self.money} \n"')
        print("Category/Hint:", category)
        print("Guessed:", guesses, "\n")
        return str(input("Guess a letter or phrase: "))

#Need this to help extract a random phrase each round
import random

alphabet = 'abcdefghijklmnopqrstuvwxyz'
vowels = 'aeiou'
vowel_price = 250
winner_prizes = [10000, 15000, 20000, 25000, 50000]
phrases_dict = {'Sports': ['golf','hockey','football'],
                'Places' : ['new york city', 'atlanta', 'milwaukee'],
                'Presidents' : ['abraham lincoln', 'george washington'],
                'Foods' : ['scrambled eggs', 'greek yogurt']}

wheel = [100, 100, 150, 200, 250, 250, 300, 350, 400, 450, 500, 500, 550, 600, 650, 700, 750, 750, 800, 850, 900, 900, 'Lose Turn', 'Bankrupt']

#Gets our random wheel spin value
def spinWheel():
    return random.choice(wheel)

#Gets our random phrase and categorical hint
def getPhrase():
    category = random.choice(list(phrases_dict.keys()))
    phrase = random.choice(phrases_dict[category])
    return (category, phrase)

#This is intended to provide the guessed letters and unguessed letters of our phrase 
def guessedPhrase(phrase, guesses):
    board = ''
    for i in phrase:
        if (i in alphabet) and (i not in guesses):
            board = board + '_ '
        else:
            board = board + i
    print(board)
    
#We can get our player names, and we have set the players to 3
num_players = 3
our_players = [gamePlayers(input(f'Enter the name of player #{i+1}: ')) for i in range(num_players)]
players_list = our_players

category, phrase = getPhrase()
guesses = []
playerIndex = 0

def getPlayerMove(player, category, guesses):
    while True:
        move = player.getMove(category, guessedPhrase(phrase, guesses), guesses)
        move = move.lower()
        if len(move) == 1:
            if move not in alphabet:
                print('That is not a letter! Try again.')
                continue
            elif move in guesses: # this letter has already been guessed
                print(f'{move} has already been guessed. Try again.')
                continue
            elif move in vowels and player.money < vowel_price: # if it's a vowel, we need to be sure the player has enough money to buy it
                    print(f'Need ${vowel_price} to guess a vowel. Try again.')
                    continue
            else:
                return move
        else:
            return move

#cannot get the rounds to work
rounds = 2
while rounds > 0:
    player = our_players[playerIndex]
    wheelAmount = spinWheel()
    print('')
    print(f'{player.name} spins and it lands on {wheelAmount}')
    if wheelAmount == 'Bankrupt':
        player.bankrupt()
    elif wheelAmount == 'Lose a Turn':
        pass
    elif type(wheelAmount) is int:
        move = getPlayerMove(player, category, guesses)
        if len(move) == 1:
            guesses.append(move)
            print(f'{player.name} guesses "{move}"')
            if move in vowels:
                player.money -= vowel_price
            count = phrase.count(move)
            if count > 0:
                if count == 1:
                    print(f'There is one "{move}"')
                else:
                    print(f"There are {count} {move}'s")
                player.totalMoney(wheelAmount)
                if guessedPhrase(phrase, guesses) == phrase.lower():
                    print(f'{player.name} wins the round! The phrase was {phrase}')
                    rounds -= 1
                    break;
                continue;
            elif count == 0:
                print(f'There is no "{move}"')
        else:
            if move == phrase:
                print(f'{player.name} wins the round! The phrase was {phrase}')
                rounds -= 1
                break;
                player.totalMoney(wheelAmount)
            else:
                print(f'{move} was not the phrase')
    #This helps us cycle through our three players
    playerIndex = (playerIndex + 1) % len(players_list)



#winner enters final round...I separated the main game from the final round
#struggled with this part because I was not sure how to determine a winner with the code

def getFinalPrize():
    final_prize = random.choice(winner_prizes)
    return final_prize

final_round_given = ['R','S','T','L','N','E']
def finalGuessedPhrase(phrase, guesses):
    final_board = ''
    for i in phrase:
        if (i in alphabet) and (i not in final_round_given):
            final_board = final_board + '_ '
        elif i in final_round_given:
            final_board = final_board + i
    print(final_board)

consonants = []
for letter in alphabet:
    if letter not in vowels:
        consonants.append(letter)
selected_consonants = 0
selected_vowels = 0

def consonantSelections(player, category, guesses):
    while selected_consonants < 4:
        selection = player.getMove(category, guessedPhrase(phrase, guesses), guesses)
        selection = selection.lower()
        if selection not in alphabet:
            print('That is not a letter! Try again.')
            continue
        elif selection in guesses: # this letter has already been guessed/is in the given letters
            print(f'{move} has already been guessed. Try again.')
            continue
        elif selection in vowels: 
            print(f'Need to select consonants first. Try again.')
            continue
        else:
            return selection
            selected_consonants += 1
            break;
            
def vowelSelection(player, category, guesses):
    while selected_vowels < 1:
        selection = player.getMove(category, guessedPhrase(phrase, guesses), guesses)
        selection = selection.lower()
        if selection not in alphabet:
            print('That is not a letter! Try again.')
            continue
        elif selection in guesses: # this letter has already been guessed/is in the given letters
            print(f'{move} has already been guessed. Try again.')
            continue
        elif selection in consonants: 
            print('Need to select vowels now. Try again.')
            continue
        else:
            return selection
            selected_vowels +=1
            break;

final_guess = 0
while final_guess < 1:
    move = getPlayerMove(player, category, guesses)
    if guessedPhrase(phrase, guesses) == phrase.lower():
        print(f'{player.name} wins the round! The phrase was {phrase}')
        final_guess +=1
        print(final_prize)
        break;
    else:
        print('Sorry...Maybe next time!')
