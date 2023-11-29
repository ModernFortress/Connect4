import random

class Connect4:
    def __init__(self, width, height):
        '''Creates a blank Connect4 board as a list of lists with given width and height'''
        self.width = width
        self.height = height
        self.board = []
        
        # Note: We take row 0 to be the top of the board
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.board += [boardRow]
        
    def __str__(self):
        '''Returns a text representation of the current state of the board in terminal output'''
        # set up the board itself
        s = ''   # the string to return
        for row in range(self.height):
            s += '|'   # add the separator character
            for col in range(self.width):
                s += self.board[row][col] + '|'
            s += '\n'
        # add the column labels under the columns
        s += '--'*self.width + '-\n'
        for col in range(self.width):
            s += ' ' + str(col % 10)
        s += '\n'
        return s

    def is_legal_move(self, col):
        '''Returns True if given column col exists and has space, otherwise returns False'''
        return (col in range(self.width)
                and self.board[0][col] == ' ')

    def add_move(self, col, player):
        ''' Places token in column col for designated player, 
            returning True if move was legal, or False otherwise '''
        # Test for legal move
        if not self.is_legal_move(col):
            return False
        # From is_legal_move method row 0 is empty
        last_empty_row = 0
        # Checks all other rows in col
        for row in range(self.height):
            # If row empty, updates last_empty_row
            if self.board[row][col] == ' ':
                last_empty_row = row
        # Modifies board list with player token
        self.board[last_empty_row][col] = player
        return True

    def del_move(self, col):
        '''Removes the top token in specified column 'col' 
            If column is empty or nonexistent, does nothing.'''
        # checks for col in the board
        if col not in range(self.width):
            return
        for row in range(self.height):
            # if location [row][col] is not empty, turn empty and exit
            if self.board[row][col] != ' ':
                self.board[row][col] = ' '
                return

    def clear(self):
        '''clears the board'''
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = ' '

    def is_full(self):
        '''Returns True if all spaces in the board are occupied, otherwise returns False '''
        for col in range(self.width):
            if self.is_legal_move(col):
                return False
        return True

    def is_win_for(self, player):
        ''' Returns True if the designated player has won, otherwise False '''
        # check for horizontal wins
        for row in range(self.height):
            for col in range(self.width - 3):
                if (self.board[row][col + 0] == player
                        and self.board[row][col + 1] == player
                        and self.board[row][col + 2] == player
                        and self.board[row][col + 3] == player):
                    return True

        # check for vertical wins
        for row in range(self.height - 3):
            for col in range(self.width):
                if (self.board[row][col] == player
                        and self.board[row + 1][col] == player
                        and self.board[row + 2][col] == player
                        and self.board[row + 3][col] == player):
                    return True

        # check for diagonal wins (positive slope)
        for row in range(self.height - 3):
            for col in range(self.width):
                if (self.board[row][col] == player
                        and self.board[row + 1][col - 1] == player
                        and self.board[row + 2][col - 2] == player
                        and self.board[row + 3][col - 3] == player):
                    return True

        # check for diagonal wins (negative slope):
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if (self.board[row][col] == player
                        and self.board[row + 1][col + 1] == player
                        and self.board[row + 2][col + 2] == player
                        and self.board[row + 3][col + 3] == player):
                    return True
        return False

    def __play_game__(self, player1, player2):
        """plays a game of connect four by calling the turn method repeatedly"""
        turns = {player1: player2, player2: player1}
        player = player1
        while not self.turn(player, player.next_move(self)):
            player = turns[player]

    def host_game(self):
        '''plays a game of connect four between two human players'''
        x_player = HumanPlayer('X')
        o_player = HumanPlayer('O')
        self.__play_game__(x_player, o_player)

    def turn(self, player, move):
        '''Plays one turn of connect4. Receives move from next_move method (from either Ai or HumanPlayer Class)
        Steps for a turn:
            1. Checks move is legal
            2. Makes move
            3. Checks for wins and ties
            4. Prints updated board
            Returns True for wins or board full'''

        while not self.is_legal_move(move):
            move = player.next_move(self)
        self.add_move(move, player.token)
        if self.is_win_for(player.token):

            print(self.__str__())
            print(player.token + ' wins!')
            return True
        if self.is_full():
            self.clear()
            print(self.__str__())
            print('Draw.')
            return True
        print(self.__str__())
        return False

    def play_game_with(self, ai_player):
        '''plays a game of connect four between a human player and an AI from the AiPlayer Class'''
        self.__play_game__(HumanPlayer('X'), ai_player)

class HumanPlayer:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f'Human Token: {self.token}'
    
    def next_move(self, game):
        return int(input('Player ' + self.token + ', please enter your move: '))

class AiPlayer:
    def __init__(self, token, tiebreaker, ply):
        """tiebreakers:
            Left: favors move closest to the left edge of the board
            Right: favors move closest to the right edge of the board
            Random: random
        """
        self.token = token
        self.tiebreaker = tiebreaker
        self.ply = ply

    def __str__(self):
        return f'AI Token: {self.token} using {self.tiebreaker}' \
                + f' tiebreaking at {self.ply} ply'
    
    def next_move(self, game):
        '''Returns best move based on current game state by doing the following:
            1. Calling _scores_for method to generate list of move scores (1 for each column)
            2. Determining highest score in list
            3. Creating list of highest score column indices
            4. Tiebreaking between highest score (best move) columns
        '''
        # generate move scores
        scores = self._scores_for(game, self.token, self.ply)
        # find best move
        best_score = max(scores)
        best_moves = []
        # create list of column indices which have the highest score
        for x in range(len(scores)):
            if scores[x] == best_score:
                best_moves.append(x)
        # tiebreakers and return best move column int
        if self.tiebreaker == 'Left':
            return best_moves[0]
        elif self.tiebreaker == 'Right':
            return best_moves[-1]
        return random.choice(best_moves)

    def _scores_for(self, game, token, ply):
        '''Returns a list of tuples (pairs of scores and column indices), using is_legal_move and is_win_for:
                100 = player wins,
                50 = play continues,
                0 = player loses
                -1 = not possible

        Plays in a column, scores resulting board, and deletes move before moving to next column'''
        scores = [0] * game.width
        for col in range(game.width):
            if game.is_legal_move(col):
                game.add_move(col, token)
                if game.is_win_for(token):
                    scores[col] = 100
                else:
                    if ply > 1:
                        op_scores = self._scores_for(game, self.other_player(token), ply - 1)
                        best_score = max(op_scores)
                        scores[col] = 100 - best_score
                    else:
                        scores[col] = 50
                game.del_move(col)
            else:
               scores[col] = -1
        return scores
    
    def other_player(self, token):
        turns = {'X': 'O', 'O': 'X'}
        return turns[token]

def main():
    b = Connect4(6, 7)
    # b.host_game()
    my_player = AiPlayer('O', 'Left', 1)
    b.play_game_with(my_player)


if __name__ == '__main__':
    main()
