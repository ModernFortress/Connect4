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
        '''Returns a text representation of the current state of the board
            in terminal output'''
        
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
        # Exits immediately if col outside board
        if col not in range(self.width):
            return False
        # Returns if given (now verified existing) column has space
        return self.board[0][col] == ' '

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
        '''Removes the top token in specified column col 
            If column is empty or nonexistent, does nothing.'''
        # checks move is legal, if not legal, exit
        if not self.is_legal_move(col):
            return
        for row in range(self.width):
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
        ''' Returns True if all spaces in the board are occupied, otherwise returns False '''
        for col in range(self.width):
            if self.is_legal_move(col):
                return False
        return True

    def is_win_for(self, player):
        ''' Returns True if the designated player has won, otherwise False '''
        # check for horizontal wins
        for row in range(self.height):
            for col in range(self.width - 3):
                if self.board[row][col] == player and \
                   self.board[row][col+1] == player and \
                   self.board[row][col+2] == player and \
                   self.board[row][col+3] == player:
                    return True

        # check for vertical wins
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.board[row][col] == player and \
                   self.board[row + 1][col] == player and \
                   self.board[row + 2][col] == player and \
                   self.board[row + 3][col] == player:
                    return True

        # check for diagonal wins (positive slope)
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.board[row][col] == player and \
                   self.board[row + 1][col - 1] == player and \
                   self.board[row + 2][col - 2] == player and \
                   self.board[row + 3][col - 3] == player:
                    return True

        # check for diagonal wins (negative slope):
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.board[row][col] == player and \
                   self.board[row + 1][col + 1] == player and \
                   self.board[row + 2][col + 2] == player and \
                   self.board[row + 3][col + 3] == player:
                    return True
        return False

    def host_game(self):
        ''' plays a game of connect four by calling the turn method repeatedly'''
        count = 0
        while True:
            if self.turn(count):
                break
            count += 1

    def turn(self, count):
        '''Plays one turn of connect4. Steps for a turn:
            1. Asks for move
            2. Checks move is legal
            3. Makes move
            4. Checks for wins and ties
            5. Prints updated board'''
        player = count % 2
        if player == 0:
            move = int(input('Player X, please enter your move: '))
        else:
            move = int(input('Player O, please enter your move: '))
        while not self.is_legal_move(move):
            move = int(input('That move is not possible. Please pick another move: '))
        if player == 0:
            player = 'X'
        else:
            player = 'O'
        self.add_move(move, player)
        if self.is_win_for(player):
            self.clear()
            print(self.__str__())
            print(player + ' wins!')
            return True
        if self.is_full():
            self.clear()
            print(self.__str__())
            print('You tied!')
            return True
        print(self.__str__())
        return False

def main():
    b = Connect4(7, 6)
    print(b)
    b.host_game()

if __name__ == '__main__':
    main()
