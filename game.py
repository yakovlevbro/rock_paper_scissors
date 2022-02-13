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

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        p3 = self.moves[2].upper()[0]

        actions = [p1, p2, p3]
        winner = -1
        if "P" in actions and "R" in actions and 'S' not in actions:
            winner = 'P'
        elif "P" in actions and "S" in actions and 'R' not in actions:
            winner = 'S'
        elif "R" in actions and "S" in actions and 'P' not in actions:
            winner = 'R'
        else:
            return winner
        return [key for key, value in enumerate(actions) if value == winner]

    def reset_went(self):
        self.p1_went = False
        self.p2_went = False
        self.p3_went = False

