import pygame
import rules


'''s["right_square"] = gdict["s["right_square"]"]
s["block_size"] = gdict["s["block_size"]"]
s["win_width"] = gdict["s["win_width"]"]
s["win_height"] = gdict["s["win_height"]"]
win = gdict["win"]
pomaranczowy = gdict["pomaranczowy"]
zielony = gdict["zielony"]
czerwony = gdict["czerwony"]
zolty = gdict["zolty"]
font = gdict["font"]
black = gdict["black"]
n = gdict["n"]'''

def functionality2_add_settings(c): #c to klasa
    c.modified_square = (c.right_square[0], c.right_square[1], c.right_square[2], c.right_square[3] - c.block_size)
    c.player_tab = (c.right_square[0], c.win_height - c.block_size, (c.win_width-c.right_square[0])/3, c.block_size)
    c.negotiations_tab = (c.right_square[0] + (c.win_width-c.right_square[0])/3, c.win_height - c.block_size, (c.win_width-c.right_square[0])/3, c.block_size)
    c.buy_tab = (c.right_square[0] + 2*(c.win_width-c.right_square[0])/3, c.win_height - c.block_size, (c.win_width-c.right_square[0])/3, c.block_size)
    c.tak_rect = (c.right_square[0] + c.block_size, 6*c.block_size, 4*c.block_size, c.block_size)
    c.nie_rect = (c.right_square[0] + 5*c.block_size, 6*c.block_size, 4*c.block_size, c.block_size)
    c.finish_square = (c.right_square[0], c.win_height-2*c.block_size, c.win_width-c.right_square[0], c.block_size)

    c.wyslij_oferte_rect = (c.right_square[0], c.win_height-3*c.block_size, c.right_square[2] - c.right_square[0], c.block_size)
    c.wyswietl_otrzymane_oferty_rect = (c.right_square[0], 0, c.right_square[2]-c.right_square[0], c.block_size)
    c.akceptuj_rect = (c.right_square[0] + 20, c.win_height - 3*c.block_size, 200, c.block_size)
    c.odrzuc_rect = (c.right_square[0] + 250, c.win_height - 3*c.block_size, 200, c.block_size)
    
global flaga
flaga = 1

def show_manage(c):
    if flaga == 1:
        pygame.draw.rect(c.win, c.pomaranczowy, c.modified_square)
    elif flaga == 2:
        #zakladka negocjacje
        show_negocjacje(c)
        #pygame.draw.rect(c.win, c.zielony, c.modified_square)
    elif flaga == 3:
        pygame.draw.rect(c.win, c.zolty, c.modified_square)
    #flaga = 4 oznacza ekran, na ktorym wyswietlaja sie oferty negocjacji od innych graczy
    elif flaga == 4:
        wyswietl_oferty(c)
    else:
        szczegoly_oferty(c)
        show_accept_negocjacje(c)

    font = pygame.font.SysFont("comicsans", 40)
    pygame.draw.rect(c.win, c.pomaranczowy, c.player_tab)
    pygame.draw.rect(c.win, c.zielony, c.negotiations_tab)
    if check_belongs(c.n[c.player.pos], c.player) and c.player.juz_sprawdzone == False:
        pygame.draw.rect(c.win, c.czerwony, c.buy_tab)
    else:
        pygame.draw.rect(c.win, c.zolty, c.buy_tab)
    stan = font.render("moj stan2", 1, c.black)
    negocjacje = font.render("negocjacje", 1, c.black)
    oferty = font.render("oferty", 1, c.black)
    c.win.blit(stan, (c.player_tab[0] + 10, c.player_tab[1] + 10))
    c.win.blit(negocjacje, (c.negotiations_tab[0] + 10, c.negotiations_tab[1] + 10))
    c.win.blit(oferty, (c.buy_tab[0] + 10, c.buy_tab[1] + 10))
    finish_move(c)

def manage(c):
    premise = c.n[c.player.pos]
    #zakladki gracza, negocjacji, kupna
    global flaga
    show_manage(c)
    
    czy_do_kupienia = check_belongs(premise, c.player)
    #if czy_do_kupienia and c.player.juz_sprawdzone == False:
        #pygame.draw.rect(c.win, c.czerwony, c.buy_tab)

    #stan konta gracza
    if flaga == 1:
        #pygame.draw.rect(c.win, c.pomaranczowy, c.modified_square)
        show_money(c.player, c)
    
    #negocjacje
    elif flaga == 2:
        pass
        #pygame.draw.rect(c.win, c.zielony, c.modified_square)
    
    #oferty kupna posiadlosci (nie otrzymane od innych graczy)
    elif flaga == 3:
        #pygame.draw.rect(c.win, c.zolty, c.modified_square)
        if czy_do_kupienia and c.player.interested == True and c.player.juz_sprawdzone == False:
            buy_offer(premise, c)

    else:
        pass

#returned value indicates whether to show an offer
def check_belongs(premise, player):
    if (player.interested == True) and (premise.belongs is None) and (premise.name != "start" and premise.name != "kasa spoleczna" and premise.name != "szansa" and premise.name != "podatek dochodowy" and premise.name != "wiezienie/odwiedzajacy" and premise.name != "bezplatny parking" and premise.name != "domiar podatkowy" and premise.name != "idz do wiezienia"):
        #buy(premise)
        return True
    else:
        #zaplac haracz lub skorzystaj z szansy lub kasy spolecznej lub zplac podatek lub idz do wiezienia lub skorzystaj z bezplatnego parkingu itd.
        #pay(premise)
        #sprawdzamy to juz po wykonaniu sprawdzenia czy trzeba zaplacic innemu graczowi,
        #wiec jesli zaplacilismy to mozemy od razu oddac ruch
        #player.interested = False
        return False

def negocjacje_check_belongs(premise, player):
    if (premise.belongs is not None) and premise.name != "start" and premise.name != "kasa spoleczna" and premise.name != "szansa" and premise.name != "podatek dochodowy" and premise.name != "wiezienie/odwiedzajacy" and premise.name != "bezplatny parking" and premise.name != "domiar podatkowy" and premise.name != "idz do wiezienia":
        return True
    else:
        return False

def show_status(mouse_pos, c):
    x, y = mouse_pos
    global flaga
    if x >= c.player_tab[0] and x <= (c.player_tab[0] + c.player_tab[2]) and y >= c.player_tab[1] and y <= (c.player_tab[1] + c.player_tab[3]):
        flaga = 1
    elif x >= c.negotiations_tab[0] and x <= (c.negotiations_tab[0] + c.negotiations_tab[2]) and y >= c.negotiations_tab[1] and y <= (c.negotiations_tab[1] + c.negotiations_tab[3]):
        flaga = 2
    elif x >= c.buy_tab[0] and x <= (c.buy_tab[0] + c.buy_tab[2]) and y >= c.buy_tab[1] and y <= (c.buy_tab[1] + c.buy_tab[3]):
        flaga = 3
    elif rules.button_clicked(mouse_pos, c.wyswietl_otrzymane_oferty_rect):
        flaga = 4
        c.oferty_rect = []
        for i in range(len(c.player.oferty)):
            #sa to prostokaty, ktore wykorzystamy do wyswietlania ofert
            c.oferty_rect.append((c.right_square[0], c.right_square[1] + (i+1)*c.block_size, c.win_width - c.right_square[0], c.block_size))

    if show_oferta(mouse_pos, c):
        flaga = 5


def show_money(player,c):
    black = (0,0,0)
    font = pygame.font.SysFont("comicsans", 60)
    money = font.render("Stan konta: " + str(player.money), 1, c.black)
    c.win.blit(money, (c.right_square[0] + 20, c.right_square[1] + 20))

def buy_offer(premise,c):
    oferta_text = c.font.render("Oferta:",1,c.black)
    premise_name_text = c.font.render(premise.name,1,c.black)
    za_text = c.font.render("za", 1, c.black)
    ile_text = c.font.render(str(premise.value),1,c.black)
    c.win.blit(oferta_text, (c.right_square[0] + c.block_size, 2*c.block_size))
    c.win.blit(premise_name_text, (c.right_square[0] + c.block_size, 3*c.block_size))
    c.win.blit(za_text, (c.right_square[0] + c.block_size, 4*c.block_size))
    c.win.blit(ile_text, (c.right_square[0] + c.block_size, 5*c.block_size))
    pygame.draw.rect(c.win, c.zielony, c.tak_rect)
    pygame.draw.rect(c.win, c.czerwony, c.nie_rect)
    tak_text = c.font.render("Akceptuj", 1, c.black)
    nie_text = c.font.render("Odrzuc", 1, c.black)
    c.win.blit(tak_text, (c.tak_rect[0] + 10, c.tak_rect[1] + 10))
    c.win.blit(nie_text, (c.nie_rect[0] + 10, c.nie_rect[1] + 10))

def accept_offer(mouse_pos, c):
    #print("wchodze do accept_offer: juz_sprawdzone: ", c.player.juz_sprawdzone)
    #global juz_sprawdzone
    global flaga

    if flaga == 3 and c.player.interested:
        x, y = mouse_pos
        czy_do_kupienia = check_belongs(c.n[c.player.pos], c.player)
        #tak_rect = (c.right_square[0] + 2*c.block_size, 2*c.block_size)
        #nie_rect = (c.right_square[0] + 4*c.block_size, 2*c.block_size)
        #if x >= c.tak_rect[0] and x <= (c.tak_rect[0] + 100) and y >= c.tak_rect[1] and y <= (c.tak_rect[1] + 50):
        if rules.button_clicked(mouse_pos, c.tak_rect):
            #print("functionality2-accept_offer- tekst powinien zniknac")
            print("functionality2-accept_offer-akceptuj")
            
            
            #player.interested = False
            c.player.juz_sprawdzone = True
            c.player.money -= c.n[c.player.pos].value
            print("c.player.interested: ", c.player.interested, ", c.player.juz_sprawdzone: ", c.player.juz_sprawdzone, ", check_belongs: ", czy_do_kupienia)
            #c.n[c.player.pos].belongs = c.player.name
            data = {
                "function":"update_nieruchomosci",
                "game_name":c.game_name,
                "nieruchomosc":c.player.pos, #nr nieruchomosci
                "gracz":c.player.name,
                "domki":0
            }
            c.network.send(data)

            spend_money(c)
            #juz_sprawdzone = True

        #elif x >= nie_rect[0] and x <= (nie_rect[0] + 100) and y >= nie_rect[1] and y <= (nie_rect[1] + 50):
        elif rules.button_clicked(mouse_pos, c.nie_rect):
            c.player.juz_sprawdzone = True
            print("functionality2-accept_offer-odrzuc")
            czy_do_kupienia = check_belongs(c.n[c.player.pos], c.player)
            print("c.player.interested: ", c.player.interested, ", c.player.juz_sprawdzone: ", c.player.juz_sprawdzone, ", check_belongs: ", czy_do_kupienia)
            #player.interested = False
            #juz_sprawdzone = True

    #return juz_sprawdzone

def draw_players(c, players):
    for i in range(len(players)):
        square = (players[i].x, players[i].y, players[i].image["size"], players[i].image["size"])
        pygame.draw.rect(c.win, players[i].image["color"], square)

def update_players(network, game_name):
    data = {
        "function":"update_players2",
        "game_name":game_name
    }
    players = network.send(data)
    return players

def finish_move(c):    
    #pygame.draw.rect(c.win, c.niebieski, (700, 500, 300, 100))
    pygame.draw.rect(c.win, c.black, c.finish_square)
    
    finish_text = c.font.render("Zakoncz ruch", 1, c.bialy)
    c.win.blit(finish_text, (c.finish_square[0]+10, c.finish_square[1]+10))

#zakladka negocjacje

#jesli jestes w zakladce negocjacje, to mozesz negocjowac z innymi zawodnikami:
#jesli klikniesz na swoja posiadlosc, to dodasz ja do listy sprzedazy, a jesli posiadlosc
#innego gracza, to dodasz ja do listy zakupow; jesli dana posiadlosc bedzie kliknieta powtornie,
#to zniknie ona z oferty
def negocjuj(mouse_pos, c):
    global flaga
    if flaga == 2:
        for i in range(len(c.n)):
            rect = (c.n[i].x, c.n[i].y, c.block_size, c.block_size)
            czy_dodac = rules.button_clicked(mouse_pos, rect)
            if czy_dodac:
                if c.n[i].belongs == c.player.name:
                    if c.n[i] not in c.lista_sprzedazy:
                        c.lista_sprzedazy.append(c.n[i])
                    else:
                        c.lista_sprzedazy = [premise for premise in c.lista_sprzedazy if premise != c.n[i]]
                    
                elif negocjacje_check_belongs(c.n[i], c.player):
                    if c.n[i] not in c.lista_zakupow:
                        if c.lista_zakupow == []:
                            c.lista_zakupow.append(c.n[i])
                        else:
                            if c.lista_zakupow[0].belongs == c.n[i].belongs:
                                c.lista_zakupow.append(c.n[i])
                    else:
                        c.lista_zakupow = [premise for premise in c.lista_zakupow if premise != c.n[i]]

        czy_wyslij = rules.button_clicked(mouse_pos, c.wyslij_oferte_rect)        
        if czy_wyslij:
            #zaimplementuj wyslanie oferty przez serwer do danego gracza
            sprzedaz = []
            kupno = []
            for i in range(len(c.lista_sprzedazy)):
                item = c.lista_sprzedazy[i].name
                sprzedaz.append(item)

            for i in range(len(c.lista_zakupow)):
                item = c.lista_zakupow[i].name
                kupno.append(item)

            data = {
                "function":"przeslij_oferte",
                "game_name":c.game_name,
                "kupno":kupno, #lista obiektow ktore zamierzamy kupic
                "sprzedaz":sprzedaz, #lista obiektow ktore zamierzamy sprzedac
                "negocjowana_kwota":c.negocjowana_kwota, #dodatkowa kwota jaka chcielibysmy doplacic
                "oferujacy": c.player.name, #kto oferuje
                "do_kogo": c.lista_zakupow[0].belongs #dla kogo jest przeznaczona oferta
            }

            zwrot = c.network.send(data)
            print(zwrot)

            c.lista_sprzedazy = []
            c.lista_zakupow = []
            c.negocjowana_kwota = ""

    #print("negocjuj: lista zakupow to: ", c.lista_zakupow)
    #print("negocjuj: lista sprzedazy to: ", c.lista_sprzedazy)


def show_negocjacje(c):
    pygame.draw.rect(c.win, c.zielony, c.modified_square)
    pygame.draw.rect(c.win, c.niebieski, c.wyswietl_otrzymane_oferty_rect)
    wyswietl_oferty_text = c.font.render("Wyswietl otrzymane oferty: " + str(c.otrzymane_oferty), 1, c.black)
    kup_text = c.font.render("Kup:", 1, c.black)
    sprzedaj_text = c.font.render("W zamian za:", 1, c.black)
    c.win.blit(wyswietl_oferty_text, (c.right_square[0] + 5,5))
    c.win.blit(kup_text, (c.right_square[0]+10, c.block_size + 20))
    c.win.blit(sprzedaj_text, (c.right_square[0]+250, c.block_size + 20))
    
    #wyswietl pozycje, ktore chcesz kupic
    for i in range(len(c.lista_zakupow)):
        posiadlosc = c.small_font.render(c.lista_zakupow[i].name, 1, c.black)
        c.win.blit(posiadlosc,(c.right_square[0] + 10, 3*c.block_size + i*c.block_size))

    #wyswietl pozycje, ktore chcesz sprzedac
    for i in range(len(c.lista_sprzedazy)):
        posiadlosc = c.small_font.render(c.lista_sprzedazy[i].name, 1, c.black)
        c.win.blit(posiadlosc,(c.right_square[0] + 250, 5*c.block_size + i*c.block_size))

    gotowka = c.small_font.render("Ilosc gotowki:", 1, c.black)
    c.win.blit(gotowka, (c.right_square[0] + 250, 3*c.block_size))

    czy_kursor = False
    c.kursor = (c.kursor + c.clock.get_rawtime()) % 1500
    if c.kursor < 750:
        gotowka_text = c.small_font.render(c.negocjowana_kwota + "|", 1, c.black)
    else:
        gotowka_text = c.small_font.render(c.negocjowana_kwota, 1, c.black)
    c.win.blit(gotowka_text, ((c.right_square[0] + 250, 4*c.block_size)))

    pygame.draw.rect(c.win, c.niebieski, c.wyslij_oferte_rect)
    wyslij_text = c.font.render("Wyslij", 1, c.bialy)
    c.win.blit(wyslij_text, (c.wyslij_oferte_rect[0]+5, c.wyslij_oferte_rect[1]+5))

def negocjuj_gotowke(event, c):
    if event.unicode.isnumeric():
        c.negocjowana_kwota += event.unicode
    elif event.key == pygame.K_BACKSPACE:
        c.negocjowana_kwota = c.negocjowana_kwota[:-1]


def wyswietl_oferty(c):
    rozowy2 = (210,103,129)
    pygame.draw.rect(c.win, c.bialy, c.modified_square)
    pygame.draw.rect(c.win, c.niebieski, c.wyswietl_otrzymane_oferty_rect)
    otrzymane_oferty_text = c.font.render("Otrzymane oferty:", 1, c.black)
    c.win.blit(otrzymane_oferty_text, (c.right_square[0] + 100, 10))
    for i in range(len(c.oferty_rect)):
        if i % 2 == 0:
            pygame.draw.rect(c.win, c.rozowy, c.oferty_rect[i])
        else:
            pygame.draw.rect(c.win, rozowy2, c.oferty_rect[i])
        text = c.font.render("Oferta nr " + str(i+1) + " od gracza " + c.player.oferty[i][3], 1, c.black)
        c.win.blit(text, (c.right_square[0] + 10, c.oferty_rect[i][1] + 10))

def show_oferta(mouse_pos, c):
    global flaga
    if flaga == 4:
        nr_oferty = [index for index, elem in enumerate(c.player.oferty) if rules.button_clicked(mouse_pos, c.oferty_rect[index])]
        print("show_oferta: nr oferty to: ", nr_oferty)
        if len(nr_oferty) != 0:
            c.nr_oferty = nr_oferty[0]
            return True
    
    return False
            

def szczegoly_oferty(c):
    nr_oferty = c.nr_oferty
    pygame.draw.rect(c.win, c.bialy, c.modified_square)
    pygame.draw.rect(c.win, c.niebieski, c.wyswietl_otrzymane_oferty_rect)
    wyswietl_oferty_text = c.font.render("Oferta od: " + c.player.oferty[nr_oferty][3], 1, c.black)
    kup_text = c.font.render("Sprzedaj:", 1, c.black)
    sprzedaj_text = c.font.render("W zamian za:", 1, c.black)
    c.win.blit(wyswietl_oferty_text, (c.right_square[0] + 5,5))
    c.win.blit(kup_text, (c.right_square[0]+10, c.block_size + 20))
    c.win.blit(sprzedaj_text, (c.right_square[0]+250, c.block_size + 20))
    
    #wyswietl pozycje, ktore oferujacy chce od ciebie kupic
    kupno = c.player.oferty[nr_oferty][0]
    for i in range(len(kupno)):
        posiadlosc = c.small_font.render(kupno[i], 1, c.black)
        c.win.blit(posiadlosc,(c.right_square[0] + 10, 3*c.block_size + i*c.block_size))

    #wyswietl pozycje, ktore oferujacy chce ci dac w zamian
    sprzedaz = c.player.oferty[nr_oferty][1]
    for i in range(len(sprzedaz)):
        posiadlosc = c.small_font.render(sprzedaz[i], 1, c.black)
        c.win.blit(posiadlosc,(c.right_square[0] + 250, 4*c.block_size + i*c.block_size))


    hajs = c.player.oferty[nr_oferty][2]
    gotowka = c.small_font.render("gotowke: " + hajs, 1, c.black)
    c.win.blit(gotowka, (c.right_square[0] + 250, 3*c.block_size))

def show_accept_negocjacje(c):
    pygame.draw.rect(c.win, c.zielony, c.akceptuj_rect)
    pygame.draw.rect(c.win, c.czerwony, c.odrzuc_rect)
    akceptuj_text = c.font.render("Akceptuj", 1, c.black)
    odrzuc_text = c.font.render("Odrzuc", 1, c.black)
    c.win.blit(akceptuj_text, (c.akceptuj_rect[0] + 5, c.akceptuj_rect[1] + 5))
    c.win.blit(odrzuc_text, (c.odrzuc_rect[0] + 5, c.odrzuc_rect[1] + 5))

def accept_negocjacje(mouse_pos, c):
    global flaga
    if flaga == 5:
        if rules.button_clicked(mouse_pos, c.akceptuj_rect):
            data = {
                "function": "change_owners",
                "game_name":c.game_name,
                "player":c.player.name,
                "nr_oferty": c.nr_oferty
            }
            confirm = c.network.send(data)
            
            
            
            update_negocjacje(c)
        elif rules.button_clicked(mouse_pos, c.odrzuc_rect):
            update_negocjacje(c)

def update_negocjacje(c):
    global flaga
    flaga = 4
    c.player.oferty = [oferta for index, oferta in enumerate(c.player.oferty) if index != c.nr_oferty]
    c.oferty_rect = []
    for i in range(len(c.player.oferty)):
        c.oferty_rect.append((c.right_square[0], c.right_square[1] + (i+1)*c.block_size, c.win_width - c.right_square[0], c.block_size))
        
    data = {
        "function":"update_oferty",
        "game_name": c.game_name,
        "player":c.player.name,
        "oferty": c.player.oferty
    }
    confirm = c.network.send(data)
    print("confirm")

def spend_money(c):
    data = {
            "function":"spend_money",
            "game_name":c.game_name,
            "player":c.player.name,
            "money":c.player.money
        }

    c.player.money = c.network.send(data)