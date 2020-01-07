class TTT5:
    def __init__(self):
        self.board = [0] * 25
        self.player = 1
        self.played = 0

    def check_status(self):
        self.played = 0
        c_board = []
        for i, location in enumerate(self.board):
            if location:
                c_board.append(location)
                self.played += 1
            else:
                c_board.append(-100)
        if self.played <= 5:
            return 'played'
        win_condition = 4 if self.player == 1 else -4
        if self.board[0]:
            if ((c_board[0] + c_board[1] + c_board[2] + c_board[3]) == win_condition or
                (c_board[0] + c_board[5] + c_board[10] + c_board[15]) == win_condition or
                (c_board[0] + c_board[6] + c_board[12] + c_board[18]) == win_condition):
                return 'win'

        if self.board[1]:
            if ((c_board[1] + c_board[2] + c_board[3] + c_board[4]) == win_condition or
                (c_board[1] + c_board[6] + c_board[11] + c_board[16]) == win_condition or
                (c_board[1] + c_board[7] + c_board[13] + c_board[19]) == win_condition):
                return 'win'

        if self.board[2]:
            if (c_board[2] + c_board[7] + c_board[12] + c_board[17]) == win_condition:
                return 'win'

        if self.board[3]:
            if ((c_board[3] + c_board[8] + c_board[13] + c_board[18]) == win_condition or
                (c_board[3] + c_board[7] + c_board[11] + c_board[15]) == win_condition):
                return 'win'

        if self.board[4]:
            if ((c_board[4] + c_board[9] + c_board[14] + c_board[19]) == win_condition or
                (c_board[4] + c_board[8] + c_board[12] + c_board[16]) == win_condition):
                return 'win'

        if self.board[5]:
            if ((c_board[5] + c_board[6] + c_board[7] + c_board[8]) == win_condition or
                (c_board[5] + c_board[10] + c_board[15] + c_board[20]) == win_condition or
                (c_board[5] + c_board[11] + c_board[17] + c_board[23]) == win_condition):
                return 'win'

        if self.board[6]:
            if ((c_board[6] + c_board[7] + c_board[8] + c_board[9]) == win_condition or
                (c_board[6] + c_board[11] + c_board[16] + c_board[21]) == win_condition or
                (c_board[6] + c_board[12] + c_board[18] + c_board[24]) == win_condition):
                return 'win'

        if self.board[7]:
            if (c_board[7] + c_board[12] + c_board[17] + c_board[22]) == win_condition:
                return 'win'

        if self.board[8]:
            if ((c_board[8] + c_board[13] + c_board[18] + c_board[23]) == win_condition or
                (c_board[8] + c_board[12] + c_board[16] + c_board[20]) == win_condition):
                return 'win'

        if self.board[9]:
            if ((c_board[9] + c_board[14] + c_board[19] + c_board[24]) == win_condition or
                (c_board[9] + c_board[13] + c_board[17] + c_board[21]) == win_condition):
                return 'win'

        if self.board[10]:
            if (c_board[10] + c_board[11] + c_board[12] + c_board[13]) == win_condition:
                return 'win'

        if self.board[11]:
            if (c_board[11] + c_board[12] + c_board[13] + c_board[14]) == win_condition:
                return 'win'

        if self.board[15]:
            if (c_board[15] + c_board[16] + c_board[17] + c_board[18]) == win_condition:
                return 'win'

        if self.board[16]:
            if (c_board[16] + c_board[17] + c_board[18] + c_board[19]) == win_condition:
                return 'win'

        if self.board[20]:
            if (c_board[20] + c_board[21] + c_board[22] + c_board[23]) == win_condition:
                return 'win'

        if self.board[21]:
            if (c_board[21] + c_board[22] + c_board[23] + c_board[24]) == win_condition:
                return 'win'

        # if ((c_board[0] + c_board[1] + c_board[2] + c_board[3]) == win_condition or
        #         (c_board[1] + c_board[2] + c_board[3] + c_board[4]) == win_condition or
        #         (c_board[5] + c_board[6] + c_board[7] + c_board[8]) == win_condition or
        #         (c_board[6] + c_board[7] + c_board[8] + c_board[9]) == win_condition or
        #         (c_board[10] + c_board[11] + c_board[12] + c_board[13]) == win_condition or
        #         (c_board[11] + c_board[12] + c_board[13] + c_board[14]) == win_condition or
        #         (c_board[15] + c_board[16] + c_board[17] + c_board[18]) == win_condition or
        #         (c_board[16] + c_board[17] + c_board[18] + c_board[19]) == win_condition or
        #         (c_board[20] + c_board[21] + c_board[22] + c_board[23]) == win_condition or
        #         (c_board[21] + c_board[22] + c_board[23] + c_board[24]) == win_condition or
        #         (c_board[0] + c_board[5] + c_board[10] + c_board[15]) == win_condition or
        #         (c_board[5] + c_board[10] + c_board[15] + c_board[20]) == win_condition or
        #         (c_board[1] + c_board[6] + c_board[11] + c_board[16]) == win_condition or
        #         (c_board[6] + c_board[11] + c_board[16] + c_board[21]) == win_condition or
        #         (c_board[2] + c_board[7] + c_board[12] + c_board[17]) == win_condition or
        #         (c_board[7] + c_board[12] + c_board[17] + c_board[22]) == win_condition or
        #         (c_board[3] + c_board[8] + c_board[13] + c_board[18]) == win_condition or
        #         (c_board[8] + c_board[13] + c_board[18] + c_board[23]) == win_condition or
        #         (c_board[4] + c_board[9] + c_board[14] + c_board[19]) == win_condition or
        #         (c_board[9] + c_board[14] + c_board[19] + c_board[24]) == win_condition or
        #         (c_board[0] + c_board[6] + c_board[12] + c_board[18]) == win_condition or
        #         (c_board[6] + c_board[12] + c_board[18] + c_board[24]) == win_condition or
        #         (c_board[4] + c_board[8] + c_board[12] + c_board[16]) == win_condition or
        #         (c_board[8] + c_board[12] + c_board[16] + c_board[20]) == win_condition or
        #         (c_board[1] + c_board[7] + c_board[13] + c_board[19]) == win_condition or
        #         (c_board[3] + c_board[7] + c_board[11] + c_board[15]) == win_condition or
        #         (c_board[5] + c_board[11] + c_board[17] + c_board[23]) == win_condition or
        #         (c_board[9] + c_board[13] + c_board[17] + c_board[21]) == win_condition):
        #     return 'win'
        if self.played >= len(self.board):
            return 'draw'
        else:
            return 'played'

    def play(self, location):
        action = -1 if self.player == 1 else 1
        if location < 0 or location > len(self.board)-1 or self.board[location]:
            return 'invalid'
        self.board[location] = action
        self.player = 1 if self.player == 2 else 2
        return self.check_status()

    def print_board(self):
        p_board = []
        for location in self.board:
            if location:
                if location == -1:
                    location = 'o'
                if location == 1:
                    location = 'x'
                p_board.append(location)
            else:
                p_board.append('.')

        print(f'{p_board[0]} {p_board[1]} {p_board[2]} {p_board[3]} {p_board[4]}\n'
              f'{p_board[5]} {p_board[6]} {p_board[7]} {p_board[8]} {p_board[9]}\n'
              f'{p_board[10]} {p_board[11]} {p_board[12]} {p_board[13]} {p_board[14]}\n'
              f'{p_board[15]} {p_board[16]} {p_board[17]} {p_board[18]} {p_board[19]}\n'
              f'{p_board[20]} {p_board[21]} {p_board[22]} {p_board[23]} {p_board[24]}\n')


