import socket
from _thread import *
import pickle
from game import Game
import random
from classes import Player

nazwy_nieruchomosci = ["start",
"konopacka",
"kasa spoleczna",
"stalowa",
"podatek dochodowy",
"dworzec zachodni",
"radzyminska",
"szansa",
"jagiellonska",
"targowa",
"w wiezieniu/odwiedzajacy",
"plowiecka",
"elektrownia",
"marsa",
"grochowska",
"dworzec gdanski",
"obozowa",
"kasa spoleczna",
"gorczewska",
"wolska",
"bezplatny parking",
"mickiewicza",
"szansa",
"slowackiego",
"plac wilsona",
"dworzec wschodni",
"swietokrzyska",
"krakowskie przedmiescie",
"wodociagi",
"nowy swiat",
"idz do wiezienia",
"plac trzech krzyzy",
"marszalkowska",
"kasa spoleczna",
"aleje jerozolimskie",
"dworzec centralny",
"szansa",
"belwederska",
"domiar podatkowy",
"aleje ujazdowskie"]

szanse = 12
kasy_spoleczne = 12
print("przed dev_game")
dev_game = Game(5, "dev_game", 123, 1, szanse, kasy_spoleczne) #probna gra dla jednego uzytkownika
print("pod dev_game")
gracz1 = Player(1, "Stas", (255,0,0), "gierka")
print("po graczu")
dev_game.players.append(gracz1)
print("gracze z dev_game to: ", dev_game.players)
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

#games = [dev_game]
games = []
idCount = 0

def get_games(conn, data):
    conn.sendall(pickle.dumps(games))

def create_new_game(conn, data): #data[0] to nazwa, data[1] to haslo, data[2] to ilosc graczy
    print("create_new_game funkcja")
    global idCount
    global games
    idCount += 1
    game_data = data["game"]
    print("przed stworzeniem gry")
    print("nazwa: ", game_data["nazwa"])
    print("haslo: ", game_data["haslo"])
    print("ilosc_graczy: ", game_data["ilosc_graczy"])
    print("kasy_spoleczne: ", kasy_spoleczne)
    game = Game(idCount, game_data["nazwa"], game_data["haslo"], game_data["ilosc_graczy"], szanse, kasy_spoleczne)
    print("po stworzeniu gry")
    games.append(game)
    print("po append")
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
    #print("get_players funkcja")
    gra = find_game(data["game_name"])
    #print("gra wynosi: ", gra)
    if gra > -1:
        players = games[gra].players
        #print("player 1 w tej grze to: ", players[1].name)
        #print("player 0 w tej grze to: ", players[0].name)
        czyj_ruch = games[gra].move
        #print("czyj ruch: ", czyj_ruch)
        context = {
            "players":players,
            "move":czyj_ruch
        }
        #print("get_players: ruch gracza ", czyj_ruch)
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
    #print("update_players")
    gra = find_game(data["game_name"])
    #print("gra to: ", gra)
    if gra > -1:
        #print("w warunku")
        #print("gracze to: ", games[gra].players)
        #print("data name to: ", data["name"])
        player = [player for player in games[gra].players if player.name == data["name"]]
        #if player is None:
            #print("Brak playera")
            #print("player to: ", player.name)
        if player is not None:
            player = player[0]
            #print("updateuje")
            #print("player to: ", player)
            #print("money: ", data["money"])
            #print("money playera: ", player.money)
            #print("pos playera: ", player.pos)
            player.money = data["money"]
            #print("pos: ", data["pos"])
            player.pos = data["pos"]
            #print("x: ", data["x"])
            player.x = data["x"]
            #print("y: ", data["y"])
            player.y = data["y"]
            #print("interested: ", data["interested"])
            player.interested = data["interested"]
            #print("movement: ", data["movement"])
            player.movement = data["movement"]
            #print("wait: ", data["wait"])
            player.wait = data["wait"]
            #print("po update")

        players = games[gra].players
        context = {
            "player": player,
            "players": players
        }
        #print("stworzony context")

        conn.sendall(pickle.dumps(context))

def next_move(conn, data):
    #print("next_move funkcja")
    #print("nazwa gry: ", data["game_name"])
    gra = find_game(data["game_name"])
    #print("gra wynosi: ", gra)
    if gra > -1:
        #print("w warunku")
        move = games[gra].play()
        print("move wynosi: ", move)
        conn.sendall(pickle.dumps(move))

def create_players(game):
    players = []
    colors = random.sample(range(1, game.number_of_players+1), game.number_of_players)
    for i in range(game.number_of_players):
        name = "Gracz " + str(i)
        index = colors[i]
        #k = i+1
        print("create_players: nazwa gry to: ", game.name)
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

def przeslij_oferte(conn, data):
    print("przeslij_oferte funkcja")
    gra = find_game(data["game_name"])
    print("gra wynosi: ", gra)
    
    if gra > -1:
        otrzymujacy_oferte = [gracz for gracz in games[gra].players if gracz.name == data["do_kogo"]]
        print("otrzymujacy oferte to: ", otrzymujacy_oferte)
        if otrzymujacy_oferte is not None:
            print("w warunku")
            #otrzymujacy_oferte = otrzymujacy_oferte[0]
            #wersja debug!!!
            otrzymujacy_oferte = games[gra].players[0]
            #wersja debug!!!
            print("nowy otrzymujacy to: ", otrzymujacy_oferte)
            #oferta to: lista z nieruchomosciami, ktore oferujacy chce kupic, lista rzeczy, ktore
            #chce sprzedac oraz nazwa gracza, ktory jest oferujacym
            print("kupno to: ", data["kupno"])
            print("sprzedaz to: ", data["sprzedaz"])
            print("negocjowana kwota to: ", data["negocjowana_kwota"])
            print("oferujacy to: ", data["oferujacy"])
            oferta = [data["kupno"], data["sprzedaz"], data["negocjowana_kwota"], data["oferujacy"]]
            otrzymujacy_oferte.oferty.append(oferta)
            print("dodane")

        conn.sendall(pickle.dumps("wyslane"))

def update_oferty(conn, data):
    print("update_oferty funkcja")
    gra = find_game(data["game_name"])

    if gra > -1:
        print("w warunku")
        print("gra to: ", gra)
        print("player to: ", data["player"])
        player = find_player(gra, data["player"])
        if player is not None:
            print("oferty to: ", data["oferty"])
            player.oferty = data["oferty"]
            conn.sendall(pickle.dumps("update_oferty"))

def change_owners(conn, data):
    print("change_owners funkcja")
    gra = find_game(data["game_name"])

    if gra > -1:
        print("w warunku")
        player = find_player(gra, data["player"])
        print("player to: ", player)
        oferta = player.oferty[data["nr_oferty"]]
        print("oferta to: ", oferta)
        #kupno: zmieniamy wlasciciela z 'do kogo' na 'oferujacy'
        for i in range(len(oferta[0])):
            index = [index for index, elem in enumerate(nazwy_nieruchomosci) if nazwy_nieruchomosci[index] == oferta[0][i]]
            index = index[0]
            games[gra].nieruchomosci[index][0] = oferta[3]

        print("po kupnie")

        #sprzedaz zmieniamy wlasciciela z 'oferujacy' na 'do kogo'
        for i in range(len(oferta[1])):
            index = [index for index, elem in enumerate(nazwy_nieruchomosci) if nazwy_nieruchomosci[index] == oferta[1][i]]
            index = index[0]
            games[gra].nieruchomosci[index][0] = player.name

        print("po sprzedazy")

        player.money += int(oferta[2])

        print("po dodaniu pieniedzy")

        conn.sendall(pickle.dumps("Changed owners"))

def find_player(index, name):
    print("find_player funkcja")
    player = [player for player in games[index].players if player.name == name]
    print("player to: ", player)
    if len(player) != 0:
        player = player[0]
        return player
    return None



function_dict = {
    "get_games": get_games,
    "create_new_game": create_new_game,
    "add_player_to_game": add_player_to_game,
    "ready_check": ready_check,
    "remove_player_from_game": remove_player_from_game,
    "get_players": get_players,
    "next_move":next_move,
    "update_players": update_players,
    "update_players2": update_players2,
    "szansa":szansa,
    "kasa_spoleczna":kasa_spoleczna,
    "get_nieruchomosci":get_nieruchomosci,
    "update_nieruchomosci":update_nieruchomosci,
    "przeslij_oferte":przeslij_oferte,
    "update_oferty": update_oferty,
    "change_owners": change_owners
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