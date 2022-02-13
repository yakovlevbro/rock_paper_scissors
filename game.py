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
        if "Б" in actions and "К" in actions and 'Н' not in actions:
            winner = 'Б'
        elif "Б" in actions and "Н" in actions and 'К' not in actions:
            winner = 'Н'
        elif "К" in actions and "Н" in actions and 'Б' not in actions:
            winner = 'К'
        else:
            return winner
        return [key for key, value in enumerate(actions) if value == winner]

    def reset_went(self):
        self.p1_went = False
        self.p2_went = False
        self.p3_went = False

