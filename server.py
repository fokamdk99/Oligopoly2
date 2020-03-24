import socket
from _thread import *
import pickle
from game import Game
import random
from classes import Player

szanse = 12
kasy_spoleczne = 12
dev_game = Game(5, "dev_game", 123, 1, szanse, kasy_spoleczne) #probna gra dla jednego uzytkownika
nieruchomosci = {}
for i in range(40):
    nieruchomosci[str(i)] = [None, 0] #pierwszy argument to nazwa gracza, drugi to ilosc domkow



zielony = (0,199,20)
czerwony = (255,0,0)
niebieski = (36,178,255)
pomaranczowy = (231,68,0)
zolty = (252,242,0)
fioletowy = (120,0,94)
player_colors = [zielony, czerwony, niebieski, pomaranczowy, zolty, fioletowy]

server = "192.168.0.23"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for connection, server started")

games = [dev_game]
idCount = 0

def get_games(conn, data):
    conn.sendall(pickle.dumps(games))

def create_new_game(conn, data): #data[0] to nazwa, data[1] to haslo, data[2] to ilosc graczy
    global idCount
    global games
    idCount += 1
    game_data = data["game"]
    game = Game(idCount, game_data["nazwa"], game_data["haslo"], game_data["ilosc_graczy"])
    games.append(game)
    conn.sendall(pickle.dumps(games))

def add_player_to_game(conn, data):
    #rozwin w przyszlosci zwracane wartosci: w razie gdyby gra nie zostala znaleziona(bo juz
    # np nie istnieje) to wysylana jest informacja zwrotna z taka informacja
    gra = find_game(data["nazwa"])

    if gra > -1:
        player_number = games[gra].queue #gracz bedzie playerem nr 0, 1, 2 itd. 
        ready = games[gra].add_player()
        if ready:
            create_players(games[gra])

        context = {
            "player_number": player_number,
            "ready": ready
        }
        
        conn.sendall(pickle.dumps(context))

def ready_check(conn, data):
    gra = find_game(data["nazwa"])

    if gra > -1:
        ready = games[gra].ready
        
    conn.sendall(pickle.dumps(ready))

def remove_player_from_game(conn, data):
    gra = find_game(data["nazwa"])
    deleted = False
    
    if gra > -1:
        if games[gra].queue > 1:
            games[gra].queue -= 1
        elif games[gra].queue == 1:
            del games[gra]
            deleted = True
        
    conn.sendall(pickle.dumps(deleted))

def get_players(conn, data):
    gra = find_game(data["nazwa"])

    if gra > -1:
        players = games[gra].players
        czyj_ruch = games[gra].move
        context = {
            "players":players,
            "move":czyj_ruch
        }
        print("get_players: ruch gracza ", czyj_ruch)
        conn.sendall(pickle.dumps(context))

def update_players(conn, data):
    gra = find_game(data["game_name"])

    if gra > -1:
        player = data["player"]
        player_number = data["player_number"]
        koniec_ruchu = data["koniec_ruchu"]
        if koniec_ruchu:
            games[gra].play()
        games[gra].players[player_number] = player
        context = {
            "players": games[gra].players,
            "move":games[gra].move
        }
        print("ruch gracza: ", games[gra].move)
        conn.sendall(pickle.dumps(context))

def update_players2(conn, data):
    gra = find_game(data["game_name"])

    if gra > -1:
        players = games[gra].players
        conn.sendall(pickle.dumps(players))

def next_move(conn, data):
    gra = find_game(data["game_name"])

    if gra > -1:
        move = games[gra].play()
        conn.sendall(pickle.dumps(move))

def create_players(game):
    players = []
    colors = random.sample(range(1, game.number_of_players+1), game.number_of_players)
    for i in range(game.number_of_players):
        name = "Gracz " + str(i)
        index = colors[i]
        #k = i+1
        player = Player(i, name, player_colors[index], game.name)
        players.append(player)

    game.players = players

def find_game(nazwa):
    gra = -1

    for i in range(len(games)):
        if games[i].name == nazwa:
            gra = i

    return gra

def szansa(conn, data):
    szansa_index = dev_game.losuj_szanse()
    conn.sendall(pickle.dumps(szansa_index))

def kasa_spoleczna(conn, data):
    kasa_spoleczna_index = dev_game.losuj_kase()
    conn.sendall(pickle.dumps(kasa_spoleczna_index))

def ulica(conn, data):
    nieruchomosc_index = data["nieruchomosc"]
    beneficjent = nieruchomosci[str(i)][0]
    #znajdz beneficjenta w danej grze i dodaj mu kwote 
    #odejmij kwote kontrolowanej przez nas postaci

def get_nieruchomosci(conn,data):
    gra = find_game(data["game_name"])

    if gra > -1:
        nieruchomosci = games[gra].nieruchomosci
        conn.sendall(pickle.dumps(nieruchomosci))

def update_nieruchomosci(conn,data):
    print("wchodze w update_nieruchomosci")
    gra = find_game(data["game_name"])
    print("gra wynosi: ", gra)

    if gra > -1:
        print("nr nieruchomosci to: ", data["nieruchomosc"])
        games[gra].nieruchomosci[data["nieruchomosc"]][0] = data["gracz"]
        print("updated gracz:", games[gra].nieruchomosci[data["nieruchomosc"]][0])
        games[gra].nieruchomosci[data["nieruchomosc"]][1] = data["domki"]
        print("updated domki:", games[gra].nieruchomosci[data["nieruchomosc"]][1])
        conn.sendall(pickle.dumps("updated"))



function_dict = {
    "get_games": get_games,
    "create_new_game": create_new_game,
    "add_player_to_game": add_player_to_game,
    "ready_check": ready_check,
    "remove_player_from_game": remove_player_from_game,
    "get_players": get_players,
    "update_players": update_players,
    "update_players2": update_players2,
    "szansa":szansa,
    "kasa_spoleczna":kasa_spoleczna,
    "get_nieruchomosci":get_nieruchomosci,
    "update_nieruchomosci":update_nieruchomosci
}

def threaded_client(conn):
    conn.send(str.encode("Lacze z serwerem"))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4*2048))
            if data:
                #print("function to: ", data["function"])
                reply = data["function"]
                function_dict[reply](conn, data)
                #print("reply wynosi: ", reply)
                #conn.sendall(str.encode(reply)) #sendall nie oznacza, ze wysylam dane do wszystkich
                #uzytkownikow xddddd tylko, ze korzystam z protokolu tcp, ktory zapewnia wyslanie
                #WSZYSTKICH pakietow poprawnie
        except:
            break

    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))

#tutaj kontrolujesz to, ile osob polaczylo sie z serwerem, ile gier sie odbywa,
#kto gra z kim, ile osob gra w jednej grze

#w threaded_client otrzymujesz informacje od klientow ze zmianami, ktore wprowadzil
#gracz, oraz aktualizujesz je po stronie serwera, po czym wysylaj zaktualizowane
#zmiany do wszystkich