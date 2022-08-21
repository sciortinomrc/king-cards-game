import json
from Croupier import Croupier
from Player import Player
from Rules import Rules
from cards_lib import get_value
import time
from datetime import datetime

class Game:
    def __init__(self):
        self.middle = []
        self.middle_discarder = []
        self.briscola = None
        #"p1", "p2", "p3", "p4", "p5", "p6", "p7",  "p8", "p8", "p8",
        
        self.phases = [ "p1", "p2", "p3", "p4", "p5", "p6", "p7",  "p8", "p8", "p8", "p8"]
        self.current_phase = None
        self.rules = Rules()
        self.players = {}
        self.playing = None
        self.declaring = None
        self.current_timeout = None
        self.turn_timer = 45
        self.complete = False


    def start(self, players_names):

        self.declare_players(players_names)
        dealer = 0
        print("Game will start in 5 seconds")

        for phase in self.phases:
            print(self.get_phase_rules(phase))
            table = self.set_table(phase, dealer)
            dealer = table["dealer"]
            playing_order = table["playing_order"]
            
            self.wait_declare_if_last_phase(phase, playing_order)
            print(self.players[playing_order[0]].name + " Starts")
            
            self.do_play_phase(phase, playing_order)

            dealer+=1

            print(self.players["first"].name+"\t", self.players["second"].name+"\t", self.players["third"].name+"\t", self.players["fourth"].name+"\t")
            print(str(self.players["first"].points)+"\t", str(self.players["second"].points)+"\t", str(self.players["third"].points)+"\t", str(self.players["fourth"].points)+"\t")
            print()
        self.complete = True

    def set_table(self, phase, dealer):
        dealer=self.shuffle_and_distribute(phase, dealer)
        self.set_middle(phase)
        self.set_current_phase(phase)
        playing_order = self.determine_playing_order()
        return {"dealer": dealer, "playing_order": playing_order}

    def get_leading_suit(self):
        return self.middle[0][0]
    
    def who_picks(self):
        picking = self.middle[0]
        index_picking = self.middle_discarder[0]
        picking_value =  get_value(picking)
        leading_suit = picking[0]

        if leading_suit in self.middle[1] and  get_value(self.middle[1]) > picking_value:
            picking = self.middle[1]
            index_picking = self.middle_discarder[1]
            picking_value = get_value(picking)
        
        if self.briscola and picking[0] == self.briscola:
            leading_suit = self.briscola

        if leading_suit in self.middle[2] and  get_value(self.middle[2]) > picking_value:
            picking = self.middle[2]
            index_picking = self.middle_discarder[2]
            picking_value = get_value(picking)
        
        if self.briscola and picking[0] == self.briscola:
            leading_suit = self.briscola
        
        if leading_suit in self.middle[3] and  get_value(self.middle[3]) > picking_value:
            picking = self.middle[3]
            index_picking = self.middle_discarder[3]
            picking_value = get_value(picking)
        

        return index_picking

    def get_player_info(self, name):
        for player_k in list(self.players.keys()):
            if self.players[player_k].name == name:
                return self.players[player_k]
        
        return None

    def turn_timeout(self, player):
        end = datetime.now().timestamp() + self.turn_timer
        self.current_timeout = 0
        player.discarded = None
        while datetime.now().timestamp() < end:
            if player.discarded != None:
                break
            time.sleep(1)
            self.current_timeout+=1
        

        if not player.discarded:
            player.discard(None)
        
        
        print(player.name + " discarded "+str(player.discarded ))
        self.current_timeout = -1

    def declaring_turn_timeout(self, player):
        self.declaring=player
        player.declared = False
        time.sleep(3)
        end = datetime.now().timestamp() + self.turn_timer
        self.current_timeout = 0
        while datetime.now().timestamp() < end:
            print(player.name, player.declared, self.briscola)
            if player.declared:
                break
            time.sleep(1)
            self.current_timeout +=1
        if (datetime.now().timestamp() >= end and not player.declared):
            print("Declaring timeout expired. Will declare")
            self.briscola = player.declare()

        self.current_timeout =-1

        print("Briscola = %s" % self.briscola)
        if not self.briscola:
            return
        else:
            print(player.name +" declared")
            raise

    def get_player_cards(self, player_name):
        player = self.get_player_info(player_name)
        return player.cards

    def get_player_usable_cards(self, player_name):
        player = self.get_player_info(player_name)
        return player.usable_hand

    def get_phase_rules(self, phase):
        return self.rules.__dict__[phase+"_rules"]

    def get_current_phase(self):
        return self.current_phase

    def who_is_playing(self):
        if self.playing:
            return self.playing.uuid
        return None

    def who_is_declaring(self):
        if self.declaring:
            return self.declaring
        return None

    def is_declaring_player_obliged(self):
        if self.declaring == None:
            return None
        return self.declaring.must_declare

    def get_briscola(self):
        return self.briscola

    def discard_player_card(self, player, card):
        player = self.get_player_info(player)
        player.discard(card)

    def declare_player_briscola(self, player, suit):
        player = self.get_player_info(player)
        self.briscola = player.declare(suit)
        

    def get_picks_count(self):
        return [
            {
                "uuid": self.players["first"].uuid,
                "name": self.players["first"].name,
                "picks": self.players["first"].picks
            },
            {
                "uuid": self.players["second"].uuid,
                "name": self.players["second"].name,
                "picks": self.players["second"].picks
            },
            {
                "uuid": self.players["third"].uuid,
                "name": self.players["third"].name,
                "picks": self.players["third"].picks
            },
            {
                "uuid": self.players["fourth"].uuid,
                "name": self.players["fourth"].name,
                "picks": self.players["fourth"].picks
            }
        ]

    def determine_playing_order(self):
        playing_order=list(self.players.keys())
        i=0
        while True:
            player = playing_order[i]
            self.playing = self.players[player]
            if not self.players[player].playing:
                playing_order.pop(i)
                playing_order.append(player)
                i-=1
            else:
                break
            i+=1
        return playing_order

    def declare_players(self, players_names):
        self.players = {
            "first": Player(players_names[0]),
            "second": Player(players_names[1]),
            "third": Player(players_names[2]),
            "fourth": Player(players_names[3])
        }

        self.players["first"].id="first"
        self.players["second"].id="second"
        self.players["third"].id="third"
        self.players["fourth"].id="fourth"

    def shuffle_and_distribute(self, phase, dealer):
        croupier = Croupier()
        self.current_phase={
            "id": None,
            "message": "Il croupier sta mescolando le carte"
        }
        time.sleep(5)
        
        ok_to_play = False

        while not ok_to_play:
            ok_to_play = True
            croupier.shuffle(100)
            deck = croupier.deal()

            if dealer==4:
                dealer = 0

            self.players["first"].start(deck["first"], dealer==0, dealer==3)
            self.players["second"].start(deck["second"], dealer==1, dealer==0)
            self.players["third"].start(deck["third"], dealer==2, dealer==1)
            self.players["fourth"].start(deck["fourth"], dealer==3, dealer==2)

            self.set_current_dealer()

            for player in list(self.players.keys()):
                if self.players[player].do_i_have_figures(phase):
                    continue
                ok_to_play = False
        return dealer

    def set_current_dealer(self):
        for player in self.players.keys():
            if self.players[player].dealing:
                self.dealer = self.players[player].name

    def set_current_phase(self, phase):
        time.sleep(5)
        self.current_phase = { 
            "id": phase,
            "message": self.get_phase_rules(phase)
        }

    def set_middle(self, phase):
        if phase != "p7":
            self.middle=[]
            self.middle_discarder=[]
        else:
            self.middle={
                "H": [],
                "S": [],
                "D": [],
                "C": []
            }

    def wait_declare_if_last_phase(self, phase, playing_order):
        i = 0
        if phase == "p8":
            while True:
                print("Player %s will declare" % (playing_order[i]))
                try:
                    self.declaring_turn_timeout(self.players[playing_order[i]])
                    i+=1
                    if i>3:
                        i=0
                except:
                    break
            self.declaring = None
            print("Declared %s" % self.briscola)


    def play_phase_if_p7(self, phase, playing_order):
        if phase != "p7":
            return False
        done = False
        for i in range(0, 4):

            self.playing = self.players[playing_order[i]]
            self.playing.usable("domino", None, self.middle)
            if len(self.playing.usable_hand) > 0:
                self.turn_timeout(self.playing)
                self.middle[self.playing.discarded[0]].append(self.playing.discarded)
                if "A" in self.playing.discarded and len(self.playing.usable_hand) > 0:
                    self.turn_timeout(self.playing)
                    self.middle[self.playing.discarded[0]].append(self.playing.discarded)
            if len(self.players[playing_order[i]].cards)==0:
                self.players[playing_order[i]].winner=True
                done=True
                break

        return done

    def play_phase_if_not_p7(self, phase, picked_cards):
        if phase == "p7":
            return False

        playing_order = self.determine_playing_order()
        
        for i in range(0,4):
            leading_suit = None
            if len(self.middle):
                leading_suit = self.middle[0][0]
            self.playing = self.players[playing_order[i]]
            self.playing.usable(phase, leading_suit)
            self.turn_timeout(self.playing)
            self.middle.append(self.playing.discarded)
            self.middle_discarder.append(playing_order[i])
            self.playing=None


        time.sleep(5)

        picker = self.who_picks()
        pick = {"cards": self.middle, "last_two": len(self.players[playing_order[0]].cards)<=1}
        picked_cards+=self.middle
        self.players[picker].pick(pick)
        for p in playing_order:
            self.players[p].playing=False
        self.players[picker].playing=True
        self.playing = self.players[picker]
        self.middle=[]
        self.middle_discarder=[]

        if phase=="p2":
            countJs = [card for card in picked_cards if "J" in card]
            countKs = [card for card in picked_cards if "K" in card]
            if countJs == 4 and countKs == 4:
                return True
        
        if phase=="p4":
            countQs = [card for card in picked_cards if "Q" in card]
            if countQs == 4:
                return True

        if phase == "p5":
            countHs = [card for card in picked_cards if "H" in card]
            if countHs == 13:
                return True
        
        if phase == "p6":
            try:
                picked_cards.index("HK")
                return True
            except:
                pass
        return False

    def do_play_phase(self, phase, playing_order):
        picked_cards = []
        while len(self.players[playing_order[0]].cards)>0:
            
            done = self.play_phase_if_not_p7(phase, picked_cards)
            if done:
                break
            
            done = self.play_phase_if_p7(phase, playing_order)
            if done:
                break
        self.count_phase_points(phase)


    def count_phase_points(self, phase):
        self.players["first"].count(phase)
        self.players["second"].count(phase)
        self.players["third"].count(phase)
        self.players["fourth"].count(phase)

    def get_players(self):
        players_names = []
        for player in self.players:
            players_names.append({"name" :self.players[player].name, "uuid": self.players[player].uuid, "points": self.players[player].points})
        return players_names

    def get_current_info(self, player):
        info = {}
        try:
            info["phase"] = self.current_phase
        except:
            info["phase"] = {
                "id": None,
                "message": "Phase not ready"
            }
            pass
        
        try:
            info["player_info"] = self.get_player_info(player).__dict__
        except:
            info["player_info"] = None
            pass
        try:
            info["turn_cards"] = self.get_player_usable_cards(player)
        except:
            info["turn_cards"] = []
            pass
        
        
        try:
            info["dealer"] = self.current_dealer
        except:
            info["dealer"] = None
            pass

        
        try:
            info["who_picks"] = self.who_picks()
        except:
            info["who_picks"] = None
            pass
        try:
            info["briscola"] = self.briscola
        except:
            pass
        try:
            info["players"] = self.get_players()
        except:
            info["players"] = []
            pass
        

        if self.current_timeout == None:
            info["timer"] = 0
        else:
            info["timer"] = self.current_timeout
        
        info["complete"] = self.complete
        info["middle"] = self.middle
        info["playing"] = self.who_is_playing()

        try:
            declaring_player = self.who_is_declaring()
            info["declaring"] = {"player": declaring_player.uuid, "must_declare": declaring_player.must_declare}
        except Exception:
            info["declaring"] = None

        return info

if __name__ == "__main__":
    game = Game()
    game.turn_timer=10
    game.start(["marco","gaia","toti","elisa"])