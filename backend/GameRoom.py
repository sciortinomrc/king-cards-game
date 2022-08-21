from Game import Game
from threading import Thread
from datetime import datetime
class GameRoom:
    def __init__(self, id):
        self.players = []
        self.ready = False
        self.id = id
        self.game = None
        self.created_at = datetime.now().timestamp()
        print("Created Game Room %s" % (self.id))

    def add_player(self, player):
        if len(self.players)==4:
            raise "Room is full"

        self.players.append(player)
        print("Added player: %s" %( player ))
        if len(self.players) == 4:
            self.ready = True

    def player_known(self, player):
        try:
            self.players.index(player)
            return True
        except:
            return False


    def start_game(self):
        if self.game:
            return
        self.game = Game()
        self.game.turn_timer=10
        t = Thread(target= self.game.start, args=(self.players, ))
        t.start()

    def get_player_cards(self, player):
        cards = self.game.get_player_cards(player)
        return cards
    
    def get_player_usable_cards(self, player):
        cards = self.game.get_player_usable_cards(player)
        return cards

    def get_middle(self):
        return self.game.middle

    def get_playing(self):
        playing = self.game.who_is_playing()
        return playing

    def get_declaring(self):
        declaring = self.game.who_is_declaring()
        must_declare = self.must_player_declare()
        return {"declaring": declaring, "must_declare": must_declare}

    def get_briscola(self):
        briscola = self.game.get_briscola()
        return briscola

    def must_player_declare(self):
        return self.game.is_declaring_player_obliged()
    
    def get_timeout(self):
        timeout = self.game.current_timeout
        return timeout

    def get_current_phase(self):
        try:
            phase = self.game.current_phase
            return phase
        except:
            return None

    def discard(self, player, card):
        self.game.discard_player_card(player, card)

    def declare(self, player, suit):
        self.game.declare_player_briscola(player, suit)

    def get_picks_count(self):
        return self.game.get_picks_count()

    def get_info(self, player):
        return self.game.get_current_info(player)