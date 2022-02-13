class Game:
    def __init__(self, id):
        self.p1_went = False
        self.p2_went = False
        self.p3_went = False
        self.ready = False
        self.moves = [None, None, None]
        self.id = id

    def connected(self):
        return self.ready

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_went = True
        elif player == 1:
            self.p2_went = True
        else:
            self.p3_went = True

    def all_went(self):
        return self.p1_went and self.p2_went and self.p3_went

    def reset_went(self):
        self.p1_went = False
        self.p2_went = False
        self.p3_went = False

