# no prese     -1
# no j no k    -1
# no q         -2
# no cuori     -1
# no ultime 2  -2
# no k cuori   -6
# domino       -1 +3
# briscola     +1

class Rules:
    def __init__(self):
        self.p1_rules = "No prese - Ogni presa -1 punto"
        self.p2_rules = "No J o K - Ogni presa -1 punto"
        self.p3_rules = "No Q - Ogni presa -2 punti"
        self.p4_rules = "No carte di cuori - Ogni presa -1 punto"
        self.p5_rules = "No ultime due prese - Ogni presa -2 punti"
        self.p6_rules = "No K di cuori - Presa -6 punti"
        self.p7_rules = "Domino - Chi vince +3, chi perde -1"
        self.p8_rules = "Briscola - Ogni presa +1"

    def p1(self, qt):
        return -1 * qt

    def p2(self, qt):
        return self.p1(qt)

    def p3(self, qt):
        return -2 * qt

    def p4(self, qt):
        return self.p1(qt)

    def p5(self, qt):
        return self.p3(qt)

    def p6(self):
        return -6
        
    def p7(self):
        return {
            "winner": 3,
            "loser": -1
        }
    
    def p8(self, qt):
        return qt
