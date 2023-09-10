"""
Anton Rajko
___________
9/10/2023
Assignment 1
"""

import math
import time
import random

#base player class
class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

#human player, inherited from 'Player' class
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    #gets square input from player
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input("X's turn. Input move (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves(): #checks if square is taken or out of bounds
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val #returns player's square choice

#computer player using the minimax algo, inherited from 'Player' class
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) #at the beginning, computer picks a random spot as the first move
        else:
            square = self.minimax(game, self.letter)['position'] #use the minimax algo to get the next move
        return square

    def minimax(self, state, player):
        max_player = self.letter #user
        other_player = 'O' if player == 'X' else 'X' #computer

        # first check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)} #check if user or computer won
        elif not state.empty_squares():
            return {'position': None, 'score': 0} #nobody won / draw

        if player == max_player:
            best = {'position': None, 'score': -math.inf} #intitialize score of negative infinity if current player is max player
        else:
            best = {'position': None, 'score': math.inf} #initializes score of positive infinity if current player is computer
        for possible_move in state.available_moves(): #loops through each available option
            state.make_move(possible_move, player) 
            sim_score = self.minimax(state, other_player) #updated with the calculated score

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move #position is set to best available move

            #best is updated to sim_score if it is the better than the current move
            if player == max_player: 
                if sim_score['score'] > best['score']:
                    best = sim_score 
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]
    
    print("\nWelcome to our tic tac toe game! \nThis app uses the minimax algorithm to make accurate moves against the user\n")

    #prints the board as 3 groups of 3 spaces
    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')


    #prints the numbers in the board, so the user knows what number to select
    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    #checks if move can be made by checking if selected square is empty, then returns True if it is
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    #keeps track of who is the winner, if there is a winner
    def winner(self, square, letter):
        row_ind = math.floor(square / 3) #check the row
        row = self.board[row_ind*3:(row_ind+1)*3] #get the row using row index
        if all([s == letter for s in row]): #checking for 3 in a row aka winner
            return True
        col_ind = square % 3 #check the column
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]): #checking for 3 in a column aka winner
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] # \ diagonal, checks if every letter in it is the same letter
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]] # / diagonal, checks if every letter in it is the same letter
            if all([s == letter for s in diagonal2]):
                return True
        return False

    #checks if there are empty squares on the board
    def empty_squares(self):
        return ' ' in self.board

    #checks how many empty squares there are
    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

replay = 'y' #replay variable, as long as user inputs 'y' after a game, the game will replay

def play(game, x_player, o_player, print_game=True, replay='n'):

    if print_game:
        game.print_board_nums()

    letter = 'O'
    while game.empty_squares():
        if letter == 'X':
            square = o_player.get_move(game) #gets move from computer
        else:
            square = x_player.get_move(game) #gets move from user
        if game.make_move(square, letter):

            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board() #reprints the board after a box is selected
                print('')

            if game.current_winner: #checks if game has been won
                if print_game:
                    print(letter + ' wins!')
                    replay = input("Would you like to play again? (y/n) ")  # Ask for replay input

                return letter, replay #returns the letter that won, and the replay value

            letter = 'O' if letter == 'X' else 'X' #swaps letters / swaps players

        time.sleep(.8)

    if print_game:
        print('It\'s a tie!')

    return None, replay  

if __name__ == '__main__':
    while replay == 'y':  
        x_player = SmartComputerPlayer('X')
        o_player = HumanPlayer('O')
        t = TicTacToe()
        winner, replay = play(t, x_player, o_player, print_game=True, replay='y')


