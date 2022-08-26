from flask import Flask, redirect, request, jsonify
import waitress
import uuid
import traceback
import sys
from datetime import datetime
from GameRoom import GameRoom


version = "0.0.1"


def delete_old_rooms ():
    for room in rooms.keys():
        if rooms[room].game.completed and rooms[room].created_at + (60 * 10) < datetime.now().timestamp():
            del rooms[room]
    

if __name__ == "__main__":
    print("King - Card Game %s" % (version))
    rooms = {}

    if "--demo" in sys.argv:
        rooms["magic"] = GameRoom("magic")
        rooms["magic"].add_player("Player1")
        rooms["magic"].add_player("Player2")
        rooms["magic"].add_player("Player3")
        rooms["magic"].add_player("Player4")
        rooms["magic"].start_game()

    app = Flask("King")
    # URLs
    new_gameroom_url = "/api/v1/gamerooms/new"
    is_room_ready_url = "/api/v1/gamerooms/<room_id>/ready"
    add_player_url = "/api/v1/gamerooms/<room_id>/player/<player_name>"
    start_game_url = "/api/v1/gamerooms/<room_id>/start"
    get_phase_url = "/api/v1/gamerooms/<room_id>/phase"
    get_cards_url = "/api/v1/gamerooms/<room_id>/player/<player_name>/cards"
    get_usable_cards_url = "/api/v1/gamerooms/<room_id>/player/<player_name>/cards/usable"
    get_middle_url = "/api/v1/gamerooms/<room_id>/middle"
    who_is_playing_url = "/api/v1/gamerooms/<room_id>/playing"
    who_is_declaring_url = "/api/v1/gamerooms/<room_id>/declaring"
    get_briscola_url = "/api/v1/gamerooms/<room_id>/briscola"
    obliged_to_declare_url = "/api/v1/gamerooms/<room_id>/obliged_to_declare"
    player_turn_timeout_url = "/api/v1/gamerooms/<room_id>/timeout"
    get_picks_url = "/api/v1/gamerooms/<room_id>/picks"
    discard_url = "/api/v1/gamerooms/<room_id>/player/<player_name>/discard/<card>"
    declare_url = "/api/v1/gamerooms/<room_id>/player/<player_name>/declare/<suit>"
    get_game_info_url = "/api/v1/gamerooms/<room_id>/player/<player_name>/info"
    
    @app.route(new_gameroom_url, methods=["post"])
    def new_gameroom():
        print(request.url)
        gameroom_id=uuid.uuid4()
        rooms[str(gameroom_id)] = GameRoom(str(gameroom_id))
        return redirect("http://local.king.uk/play/?room="+str(gameroom_id), code=302)

    @app.route(is_room_ready_url)
    def is_room_ready(room_id):
        # print(request.url)
        try:
            room = rooms[room_id]
            if not room.ready:
                return "Not ready", 204
                

            return "Ok"
        except:
            traceback.print_exc()
            return "Bad Request", 400

    
    @app.route(add_player_url, methods=["post"])
    def add_player(room_id, player_name):
        # print(request.url)
        try:
            room = rooms[room_id]
            if room.player_known(player_name):
                return "Ok"
                
            room.add_player(player_name)
            return "Ok"
        except:
            return "Bad Request", 400

    @app.route(start_game_url, methods=["post"])
    def start(room_id):
        # print(request.url)
        try:
            rooms[room_id].start_game()
            return "Ok"
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(get_phase_url)
    def get_phase(room_id):
        # print(request.url)
        try:
            phase = rooms[room_id].get_current_phase()
            return {"phase": phase}
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(get_cards_url)
    def get_cards(room_id, player_name):
        # print(request.url)
        try:
            cards = rooms[room_id].get_player_cards(player_name)
            return jsonify({"cards":cards})
        except:
            return "Bad Request", 400

    @app.route(get_usable_cards_url)
    def get_usable_cards(room_id, player_name):
        # print(request.url)
        try:
            cards = rooms[room_id].get_player_usable_cards(player_name)
            return jsonify({"cards":cards})
        except:
            return "Bad Request", 400

    @app.route(get_middle_url)
    def get_middle(room_id):
        # print(request.url)
        try:
            middle = rooms[room_id].get_middle()
            return jsonify({"middle":middle})
        except:
            return "Bad Request", 400

    @app.route(who_is_playing_url)
    def who_is_playing(room_id):
        # print(request.url)
        try:
            playing = rooms[room_id].get_playing()
            return jsonify({"playing":playing})
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(who_is_declaring_url)
    def who_is_declaring(room_id):
        # print(request.url)
        try:
            declaring = rooms[room_id].get_declaring()
            return jsonify(declaring)
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(get_briscola_url)
    def get_briscola(room_id):
        # print(request.url)
        try:
            briscola = rooms[room_id].get_briscola()
            return jsonify({"briscola":briscola})
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(obliged_to_declare_url)
    def obliged_to_declare(room_id):
        # print(request.url)
        try:
            obliged = rooms[room_id].must_player_declare()
            return jsonify({"obliged":obliged})
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(player_turn_timeout_url)
    def get_playing_timeout(room_id):
        # print(request.url)
        try:
            timeout = rooms[room_id].get_timeout()
            return jsonify({"timeout":timeout})
        except:
            traceback.print_exc()
            return "Bad Request", 400
        
    @app.route(get_picks_url)
    def get_picks(room_id):
        # print(request.url)
        try:
            picks = rooms[room_id].get_picks_count()
            return jsonify({"picks":picks})
        except:
            traceback.print_exc()
            return "Bad Request", 400

    @app.route(discard_url, methods=["post"])
    def discard_card(room_id, player_name, card):
        print(request.url)
        try:
            rooms[room_id].discard(player_name, card)
            return "Ok"
        except:
            return "Bad Request", 400
            
    @app.route(declare_url, methods=["post"])
    def declare_suit(room_id, player_name, suit):
        print(request.url)
        try:
            rooms[room_id].declare(player_name, suit)
            return "Ok"
        except:
            return "Bad Request", 400



    @app.route(get_game_info_url)
    def get_game_info(room_id, player_name):
        # print(request.url)
        try:
            info = rooms[room_id].get_info(player_name)
            return jsonify(info)
        except Exception as e:
            traceback.print_exc()
            return "Bad Request", 400
    

    # app.run(port=9988)
    waitress.serve(app, host="127.0.0.1", port=9988)

    