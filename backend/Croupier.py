import json
import random

from Player import Player

class Croupier:
    def __init__(self):
        self.cards = [
            "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "HA",
            "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", "DA",
            "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK", "SA",
            "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK", "CA"
        ]
        
    def shuffle(self, times):
        for i in range(0, times):
            random.shuffle(self.cards)
            random.shuffle(self.cards)
            random.shuffle(self.cards)

    def deal(self):
        players={
            "first": [],
            "second": [],
            "third": [],
            "fourth": []
        }
        players_names = list(players.keys())
        for i in range (0, len(self.cards)):
            players[players_names[0]].append(self.cards[i])
            players_names.append(players_names[0])
            players_names.pop(0)
        
        return players


if __name__ == "__main__" :
    croupier = Croupier()
    croupier.shuffle(100)
    deck = croupier.deal()


    players = {
        "first": Player(deck["first"]),
        "second": Player(deck["second"]),
        "third": Player(deck["third"]),
        "fourth": Player(deck["fourth"])
    }
    players["first"].sort()
    players["second"].sort()
    players["third"].sort()
    players["fourth"].sort()

    print(json.dumps({
        "first": ", ".join(players["first"].cards),
        "second": ", ".join(players["second"].cards),
        "third": ", ".join(players["third"].cards),
        "fourth": ", ".join(players["fourth"].cards)
    }, indent=4))