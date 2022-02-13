class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id

    def connected(self):
        return self.ready

