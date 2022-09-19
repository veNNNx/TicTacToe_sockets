class Game:
    def __init__(self, id):
        self.p1_moved = False
        self.p2_moved = True
        self.who_started = 0
        self.ready = False
        self.id = id
        self.moves = [[], []]
        self.wins = [0,0]
        self.won_pattern = []
        self.won_player = -1
        self.game_started = False
        self.winning_pattern = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], 
                                [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

    def connected(self):
        return self.ready

    def save_move(self, player, move):
        self.game_started = True
        self.moves[player].append(move)
        if player == 0:
            self.p1_moved = True
            self.p2_moved = False
        else:
            self.p1_moved = False
            self.p2_moved = True
        
    def check_winner(self):
        p1, p2 = self.moves[0], self.moves[1]
        for pattern in self.winning_pattern:
            if str(pattern[0]) in p1 and str(pattern[1]) in p1 and str(pattern[2]) in p1:
                self.won_pattern = pattern
                self.won_player = 0
                break
            if str(pattern[0]) in p2 and str(pattern[1]) in p2 and str(pattern[2]) in p2:
                self.won_pattern = pattern
                self.won_player = 1
                break
        if len(p1) + len(p2) >= 9:
            self.won_player = 30

        return self.won_player
    
    def change_score(self):
        self.check_winner()
        if self.won_player == 0:
            self.wins[0] += 1
        elif self.won_player == 1:
            self.wins[1] += 1
        elif self.won_player == 30:
            self.wins[0] += 0.5
            self.wins[1] += 0.5
    
    def reset(self):
        self.change_score()
        self.game_started = False
        if self.who_started == 0:
            self.p1_moved = True
            self.p2_moved = False
            self.who_started = 1
        else:
            self.p1_moved = False
            self.p2_moved = True
            self.who_started = 0
        self.moves = [[], []]
        self.won_pattern = []
        self.won_player = -1