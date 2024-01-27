class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def GetPlayerMove(self, playerNum):
        return self.moves[playerNum]
    
    def Play(self, playerNum, move):
        self.moves[playerNum] = move
        if playerNum == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def Connected(self):
        return self.ready
    
    def IsBothWent(self):
        return self.p1Went and self.p2Went
    
    def Winner(self):
        p1Move = self.moves[0].upper()[0]
        p2Move = self.moves[1].upper()[0]

        winner = -1
        if p1Move == "R" and p2Move == "S":
            winner = 0
        elif p1Move == "S" and p2Move == "R":
            winner = 1
        elif p1Move == "P" and p2Move == "R":
            winner = 0
        elif p1Move == "R" and p2Move == "P":
            winner = 1
        elif p1Move == "S" and p2Move == "P":
            winner = 0
        elif p1Move == "P" and p2Move == "S":
            winner = 1
        
        return winner
    
    def ResetWent(self):
        self.p1Went = False
        self.p2Went = False




