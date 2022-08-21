from Rules import Rules
from cards_lib import get_value
import random
from uuid import uuid4

rules = Rules()
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.picks = []
        self.points = 0
        self.winner = False
        self.dealing = False
        self.playing = False
        self.shoud_declare = False
        self.must_declare = False
        self.declared = False
        self.usable_hand = []
        self.id = None
        self.uuid = uuid4()
        
    def do_i_have_figures(self, game):
        if game != "p8":
            return True
        have_figure = False
        for card in self.cards:
            if "A" in card or "J" in card or "Q" in card or "K" in card:
                have_figure = True

        return have_figure
    
    def usable(self, game, suit, open=None):
        if game == "domino":
            usable_cards = []
            for card in self.cards:
                card_value = get_value(card)
                card_suite = card[0]
                for st in open:
                    if card_suite == st and card_value == 7:
                        usable_cards.append(card)
                    for cd in open[st]:
                        cd_value = get_value(cd)
                        cd_suite = cd[0]
                        if card_suite == cd_suite and (card_value == cd_value+1 or card_value == cd_value-1):
                            usable_cards.append(card)
            self.usable_hand = usable_cards
            return
        if not suit:
            self.usable_hand = self.cards
            if (game == "p4" or game == "p6") and len(self.cards)>5:
                usable_cards = [card for card in self.cards if "H"  not in card]
                self.usable_hand = usable_cards
            return
        usable_cards = [card for card in self.cards if suit in card]
        if self.playing and (game == "p4" or game == "p6") and len(self.cards)>5:
            usable_cards = [card for card in usable_cards if "H"  not in card]
        if len(usable_cards) == 0:
            self.usable_hand = self.cards
            return
        self.usable_hand = usable_cards
        return

    def discard(self, card, first = False):
        idx = None
        if card == None:
            try:
                self.usable_hand[0]
            except:
                print(self.usable_hand)
                self.discarded=None
                return
            card=self.usable_hand[0]

        try:
            idx = self.cards.index(card)
            self.cards.pop(idx)
        except:
            pass
        self.discarded = card
        return card
            

    def start(self, cards, dealing = False, opener = False):
        self.cards = cards
        self.picks = []
        self.winner = False
        self.dealing = dealing
        self.playing = opener
        self.sort()

    def sort(self):
        list.sort(self.cards)

    def pick(self, pick):
        if pick == None:
            return
        self.picks.append(pick)

    def count(self, round):
        
        if round == "p1":
            self.points += rules.p1(len(self.picks))
            return 

        if round == "p5":
            last_twos = [pick for pick in self.picks if pick["last_two"]]
            self.points += rules.p5(len(last_twos))
            return

        if round == "p7":
            points = rules.p7()
            if self.winner == True:
                self.points += points["winner"]
            else:
                self.points += points["loser"]
            return

        if round == "p8":
            self.points += rules.p8(len(self.picks))
            return
        
        count = 0
        for pick in self.picks:
            if round == "p2":
                for card in pick["cards"]:
                    if "J" in card or "K" in card:
                        count += 1
            if round == "p3":
                for card in pick["cards"]:
                    if "Q" in card:
                        count += 1
            if round == "p4":
                for card in pick["cards"]:
                    if "H" in card:
                        count += 1
            if round == "p6":
                try:
                    pick["cards"].index("HK")
                    self.points += rules.p6()
                    return
                except:
                    pass
        if round == "p2":
            self.points += rules.p2(count)
        if round == "p3":
            self.points += rules.p3(count)
        if round == "p4":    
            self.points += rules.p4(count)

    def declare(self, suit=None):
        if suit=="":
            self.declared=False
            return None

        suits = ["H","S","C","D"]
        did_declare = False
        try:
            suits.index(suit)
            did_declare = True
        except:
            pass

        if not did_declare:
            if self.must_declare:
                self.declared = True
                return self.cards[0][0]
            self.must_declare = True
            self.declared = True
            return None
        
        self.declared = True
        return suit
            
if __name__ == "__main__":

    p = Player("Marco")
    p.pick({"cards":["H1", "S7", "H4", "H3"], "last_two": True})
    p.count("p1")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p2")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HQ", "S7", "S3", "S2"], "last_two": False})
    p.count("p3")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p4")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": True})
    p.count("p5")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p6")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.winner = True
    p.count("p7")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p8")
    p.start(None)
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p8")
    p.start(None)
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.pick({"cards": ["HK", "H7", "H3", "H2"], "last_two": False})
    p.pick({"cards": ["HJ", "S7", "S3", "S2"], "last_two": False})
    p.count("p8")
    p.start(None)
    p.pick(None)
    p.count("p8")
    p.start(None)

    print(p.name, p.points)

    p.start(["C5", "C6", "C8", "CK", "CQ", "D1", "D2", "D8", "H3", "H5", "H6", "S9", "SK"])
    print(p.cards)
    print(p.usable("H"))
    p.discard("H3")
    print(p.cards)

    p.start(["C5", "C6", "C8", "CK", "CQ", "D1", "D2", "D8", "H3", "H5", "H6"])
    print(p.usable("S"))

    p.start(["C5", "C6", "C8", "CK", "CQ", "D1", "D2", "D8", "H3", "H5", "H6", "S9", "SK"])
    print(p.usable("domino",open=["C7","D7","S8"]))