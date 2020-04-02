import pygame
import random
import re

#poprawa cala kase spoleczna

class Rules:
    flaga = False
    pokaz = False
    szansa_index = None
    kasa_spoleczna_index = None

class Szansa:
    def __init__(self, description, value = None, position = None):
        self.description = description
        self.value = value
        self.position = position

    def action(self, c):
        print("description: ", self.description)
        print("action: value to: ", self.value, ", position to: ", self.position)
        if self.value is not None:
            c.player.money += self.value

        if self.position is not None:
            value = (self.position - c.player.pos) % 40
            #c.player.pos = self.position
            c.player.move_engine(value, c)
            print("pozycja playera to: ", c.player.pos)

class Kasa_spoleczna(Szansa):
    def __init__(self, description, value = None, position = None):
        super().__init__(description, value, position)

def rules_add_settings(c): #c to klasa
    szanse = []
    dworzec_gdanski = find_premise(c,"dworzec gdanski")
    #print("rules_add_settings: dworzec gdanski to: ", dworzec_gdanski)
    szanse.append(Szansa("Przejdz na dworzec gdanski. Jesli miniesz po drodze START, pobierz 200 zl", 0, dworzec_gdanski))
    szanse.append(Szansa("Zaplac za szkole 150 zl.", -150))
    plowiecka = find_premise(c,"plowiecka")
    #print("rules_add_settings: plowiecka to: ", plowiecka)
    szanse.append(Szansa("Przejdz na ulice Plowiecka. Jesli miniesz po drodze START, pobierz 200 zl.", 0,plowiecka))
    szanse.append(Szansa("Grzywna. Zaplac 20 zl.", -20))
    szanse.append(Szansa("Mandat za przekroczenie szybkosci. Zaplac 15 zl.", -15))
    szanse.append(Szansa("Przejdz na START.", 0, 0))
    szanse.append(Szansa("Otrzymales kredyt budowlany. Pobierz 150 zl.", 150))
    wiezienie = find_premise(c, "wiezienie/odwiedzajacy")
    #tutaj w razie przejscia przez start naliczy sie 200 zl. co z tym???
    szanse.append(Szansa("Idz do WIEZIENIA. Przejdz prosto do WIEZIENIA. Nie przechodz przez START. Nie pobieraj 200 zl.", 0, wiezienie))
    szanse.append(Szansa("Bank wyplaca Ci dywidende w wysokosci 50 zl.",50))
    szanse.append(Szansa("Wygrales konkurs krzyzowkowy. Pobierz 100 zl.", 100))
    ujazdowskie = find_premise(c, "aleje ujazdowskie")
    szanse.append(Szansa("Przejdz na ALEJE UJAZDOWSKIE.", 0, ujazdowskie))
    plac_wilsona = find_premise(c,"plac wilsona")
    szanse.append(Szansa("Przejdz na Plac Wilsona. Jesli miniesz po drodze START, pobierz 200 zl.",0,plac_wilsona))

    c.szanse = szanse

    kasa_spoleczna = []
    kasa_spoleczna.append(Kasa_spoleczna("Sprzedales obligacje. Pobierz 100 zl.", 100))
    kasa_spoleczna.append(Kasa_spoleczna("Honorarium lekarza. Zaplac 50 zl.", -50))
    kasa_spoleczna.append(Kasa_spoleczna("Otrzymujesz 50 zl za sprzedane akcje.", 50))
    kasa_spoleczna.append(Kasa_spoleczna("Zaplac rachunek za szpital 100 zl.", -100))
    kasa_spoleczna.append(Kasa_spoleczna("Otrzymujesz zwrot podatku dochodowego. Pobierz 20 zl.",20))
    kasa_spoleczna.append(Kasa_spoleczna("Zaplac skladke ubezpieczeniowa 50 zl.", -50))
    kasa_spoleczna.append(Kasa_spoleczna("Odziedziczyles w spadku 100 zl.",100))
    kasa_spoleczna.append(Kasa_spoleczna("Otrzymujesz odsetki od lokaty terminowej. Pobierz 25 zl.", 25))
    kasa_spoleczna.append(Kasa_spoleczna("Przejdz na START", 0, 0))
    kasa_spoleczna.append(Kasa_spoleczna("Blad bankowy na twoja korzysc. Pobierz 200 zl.",200))
    kasa_spoleczna.append(Kasa_spoleczna("Wygrana druga nagroda w konkursie pieknosci. Pobierz 10 zl.",10))
    konopacka = find_premise(c,"konopacka")
    kasa_spoleczna.append(Kasa_spoleczna("Wroc na ulice Konopacka.",0,konopacka))

    c.kasa_spoleczna = kasa_spoleczena

    c.close_szansa_rect = (c.central_square[0], c.central_square[1]+c.central_square[3]-c.block_size, c.central_square[2], c.block_size)
    c.kup_domek_rect = (c.central_square[0], c.central_square[1]+c.central_square[3]-c.block_size, int((c.central_square[0]+c.central_square[2])/3), c.block_size)
    c.zastaw_rect = (c.central_square[0] + 2*c.central_square[2]/3, c.central_square[1]+c.central_square[3]-c.block_size, int((c.central_square[0]+c.central_square[2])/3) - 18, c.block_size)
    c.sprzedaj_domek_rect = (c.central_square[0] + c.central_square[2]/3, c.central_square[1]+c.central_square[3]-c.block_size, int((c.central_square[0]+c.central_square[2])/3), c.block_size)

def rules_manage(c):
    if c.n[c.player.pos].group == "szansa":# or c.n[c.player.pos].group == "kasa_spoleczna":
        Rules.flaga = True
    if Rules.flaga and Rules.pokaz and (Rules.szansa_index is not None):
        szansa = c.szanse[Rules.szansa_index]
        show_szansa(szansa,c)
    if Rules.flaga and Rules.pokaz and (Rules.kasa_spoleczna_index is not None):
        kasa = c.kasa_spoleczena[Rules.kasa_spoleczna_index]
        show_szansa(kasa, c)

def rules_show_status(mouse_pos, c):
    x, y = mouse_pos
    if x >= c.close_szansa_rect[0] and x <= c.close_szansa_rect[0]+c.close_szansa_rect[2] and y >= c.close_szansa_rect[1] and y <= c.close_szansa_rect[1]+c.close_szansa_rect[3]:
        Rules.pokaz = False
        Rules.szansa_index = None
        Rules.kasa_spoleczna_index = None



#return index
def find_premise(c, name):
    for i in range(len(c.n)):
        if c.n[i].name == name:
            return i

    return None


def start(c):
    #nic nie rob
    pass

def ulica(c):
    '''if c.n[c.player.pos].belongs is not None and c.n[c.player.pos].belongs != c.player.name:
        c.player.money = int(c.player.money - (c.n[c.player.pos].value/4)) '''
    warunek = check_belongs(c)
    if warunek:
        print("gracz musi zaplacic: ", c.n[c.player.pos].oplaty[c.n[c.player.pos].domki])
        c.player.money -= (c.n[c.player.pos].oplaty[c.n[c.player.pos].domki])
        data = {
            "function":"ulica",
            "game_name":c.game_name,    
            "kwota":c.n[c.player.pos].oplaty[c.n[c.player.pos].domki],
            "player":c.player.name,
            "nieruchomosc":c.player.pos #pozycja gracza; na serwerze wybierasz nieruchomosc o danej
            #pozycji i dodajesz kwote graczowi ktora te posiadlosc nabyl
        }
        c.network.send(data)



def szansa(c):
    print("rules->szansa funkcja")
    #wylosuj szanse
    '''szansa = random.randrange(2)
    if szansa == 0:
        c.player.money += 50
    else:
        c.player.money -= 50'''
    data = {
        "function": "szansa",
        "game_name":c.game_name
    }
    szansa_index = c.network.send(data)
    print("szansa_index: ", szansa_index)
    Rules.szansa_index = szansa_index
    print("Rules.szansa_index: ", Rules.szansa_index)
    Rules.pokaz = True
    print("Rules.pokaz: ", Rules.pokaz)
    c.szanse[szansa_index].action(c)
    #szansa = c.szanse[szansa_index]
    #show_szansa(szansa, c)


def kasa_spoleczena(c):
    #wylosuj kase spoleczna
    '''kasa_spoleczna = random.randrange(2)
    if kasa_spoleczna == 0:
        c.player.money += 50
    else:
        c.player.money -= 50'''
    data = {
        "function": "kasa_spoleczna",
        "game_name":c.game_name
    }
    kasa_spoleczna_index = c.network.send(data)
    print("kasa_spoleczna_index: ", szansa_index)
    Rules.kasa_spoleczna_index = kasa_spoleczna_index
    print("Rules.kasa_spoleczna_index: ", Rules.kasa_spoleczna_index)
    Rules.pokaz = True
    print("Rules.pokaz: ", Rules.pokaz)
    c.kasa_spoleczna[kasa_spoleczna_index].action(c)

def idz_do_wiezienia(c):
    #jesli znajdujesz sie na polu prowadzacym do wiezienia, wyrzuciles
    #trzeci dublet lub dostajesz kare od szansy lub kasy spolecznej
    #to idz do wiezenia
    #c.player.pos = 30 #na 30 miejscu znajduje sie wiezienie
    value = (10 - c.player.pos) % 40
    c.player.move_engine(value, c)

def podatek_dochodowy(c):
    c.player.money -= 100

def wiezienie(c):
    #nic nie rob
    pass

def parking(c):
    #nic nie rob
    pass

def wodociagi(c):
    if c.n[c.player.pos].belongs is not None and c.n[c.player.pos].belongs != c.player.name:
        c.player.money -= 28

def podatek(c):
    c.player.money -= 150

def dworzec(c):
    if c.n[c.player.pos].belongs is not None and c.n[c.player.pos].belongs != c.player.name:
        c.player.money -= 50

def elektrownia(c):
    if c.n[c.player.pos].belongs is not None and c.n[c.player.pos].belongs != c.player.name:
        c.player.money -= 50


rulebook = {
    "start":start,
    "ulica":ulica,
    "kasa_spoleczna":kasa_spoleczena,
    "podatek_dochodowy":podatek_dochodowy,
    "dworzec":dworzec,
    "szansa":szansa,
    "wiezienie":wiezienie,
    "elektrownia":elektrownia,
    "parking":parking,
    "wodociagi":wodociagi,
    "idz_do_wiezienia":idz_do_wiezienia,
    "podatek":podatek
}

def show_szansa(szansa, c):
    text = szansa.description
    chunks = re.split(r'(?<=[,.])(?<!\d.)\s', text)
    pygame.draw.rect(c.win, c.bialy, c.central_square)
    for i in range(len(chunks)):
        line = c.font.render(chunks[i], 1, c.niebieski)
        c.win.blit(line, (c.central_square[0] + 10, c.central_square[1] + 10 + i*c.block_size))

    pygame.draw.rect(c.win, c.czerwony, c.close_szansa_rect)
    zamknij_text = c.font.render("Zamknij", 1, c.bialy)
    c.win.blit(zamknij_text, (c.central_square[0] + int(c.central_square[2]/2 - 90), c.central_square[1]+c.central_square[3]-c.block_size))

#funkcja sprawdzajaca czy nalezy od playera zabrac hajs (np. czy stanal na czyims polu)
def check_belongs(c):
    if c.n[c.player.pos].belongs is not None and c.n[c.player.pos].belongs != c.player.name:
        return True
    else:
        return False

def sprawdz_domki(field, c):
    if field is not None:
        kolor = field.color
        licznik = 0
        for i in range(len(c.n)):
            if c.n[i].color == kolor and c.n[i].belongs == c.player.name:
                licznik += 1

        if kolor == c.brazowy or kolor == c.fioletowy:
            print("sprawdz domki funkcja: wybrales brazowy lub fioletowy")
            print("licznik wynosi: ", licznik)
            if licznik == 2:
                return True
        elif kolor == c.bialy:
            return False
        else:
            if licznik == 3:
                return True

    return False

def show_kup_domek(c):
    #1/3 na kupno domku, 1/3 na sprzedaz domku, 1/3 na zastawienie posiadlosci
    #kup_domek_rect = (c.central_square[0], c.central_square[1]+c.central_square[3]-c.block_size, int((c.central_square[0]+c.central_square[2])/3), c.central_square[1]+c.central_square[3])
    pygame.draw.rect(c.win, c.zielony, c.kup_domek_rect)
    text = c.small_font.render("Kup dom", 1, c.black)
    c.win.blit(text, (c.kup_domek_rect[0]+10, c.kup_domek_rect[1]+10))

def show_sprzedaj_domek(c):
    pygame.draw.rect(c.win, c.pomaranczowy, c.sprzedaj_domek_rect)
    text = c.small_font.render("Sprzedaj dom", 1, c.black)
    c.win.blit(text, (c.sprzedaj_domek_rect[0]+5, c.sprzedaj_domek_rect[1]+10))

def show_zastaw(c):
    #zastaw_rect = (c.central_square[0] + 2*c.central_square[2]/3, c.central_square[1]+c.central_square[3]-c.block_size, c.central_square[0]+c.central_square[2], c.central_square[1]+c.central_square[3])
    pygame.draw.rect(c.win, c.czerwony, c.zastaw_rect)
    if c.rendered_field.pledged:
        text = c.small_font.render("wykup", 1, c.black)
    else:
        text = c.small_font.render("zastaw", 1, c.black)
    c.win.blit(text, (c.zastaw_rect[0]+10, c.zastaw_rect[1]+10))

def kup_domek(c):
    #czy_domki = sprawdz_domki(C.rendered_field, c)
    print("kup domek funkcja")
    czy_domki = c.czy_domki
    print("kolor domku: ", c.rendered_field.color, ", czy_domki: ", czy_domki)
    if c.rendered_field is not None and czy_domki:
        premises = []
        kolor = c.rendered_field.color
        if kolor != c.bialy:
            for i in range(len(c.n)):
                if c.n[i].color == kolor and c.n[i].belongs == c.player.name:
                    #premises.append(c.n[i])
                    premises.append(i)
                    #print("nazwa nieruchomosci: ", premises[i].name)

            suma = 0
            for i in range(len(premises)):
                print("nr nieruchomosci to: ", premises[i])
                suma += c.n[premises[i]].domki
            print("suma wynosi: ", suma)

            if c.n[premises[0]].x < c.block_size/2:
                odejmij = 200
            elif c.n[premises[0]].y < c.block_size/2:
                odejmij = 50
            elif c.n[premises[0]].y > 9*c.block_size/2:
                odejmij = 150
            else:
                odejmij = 100

            print("odejmij wynosi: ", odejmij)
            if len(premises) == 2:
                print("brazowy lub fioletowy")
                #if suma < 10:
                c.player.money -= odejmij
                if suma % 2 == 0:
                    c.n[premises[0]].domki += 1
                    update_domki(c, premises[0])
                else:
                    c.n[premises[1]].domki += 1
                    update_domki(c, premises[1])
            else:
                print("3 sztuki")
                #if suma < 15:
                c.player.money -= odejmij
                if suma % 3 == 0:
                    c.n[premises[0]].domki += 1
                    update_domki(c, premises[0])
                elif suma % 3 == 1:
                    c.n[premises[1]].domki += 1
                    update_domki(c, premises[1])
                else:
                    c.n[premises[2]].domki += 1
                    update_domki(c, premises[2])

'''def sprzedaj_domek(c):
    czy_domki = c.czy_domki
    if c.rendered_field is not None and czy_domki:
        premises = []
        kolor = c.rendered_field.color
        if kolor != c.bialy:
            for i in range(len(c.n)):
                if c.n[i].color == kolor and c.n[i].belongs == c.player.name:
                    premises.append(c.n[i])

            suma = 0
            for i in range(len(premises)):
                suma += premises[i].domki
                if premises[0].x < c.block_size/2:
                    odejmij = 200
                elif premises[0].y < c.block_size/2:
                    odejmij = 50
                elif premises[0].y > 9*c.block_size/2:
                    odejmij = 150
                else:
                    odejmij = 100
            if len(premises) == 2:
                c.player.money += odejmij
                if suma % 2 == 0:
                    premises[1].domki -= 1
                else:
                    premises[0].domki -= 1
            else:
                c.player.money += odejmij
                if suma % 3 == 0:
                    premises[2].domki -= 1
                elif suma % 3 == 1:
                    premises[0].domki -= 1
                else:
                    premises[1].domki -= 1'''

def sprzedaj_domek(c):
    print("sprzedaj domek funkcja")
    czy_domki = c.czy_domki
    if c.rendered_field is not None and czy_domki:
        premises = []
        kolor = c.rendered_field.color
        if kolor != c.bialy:
            for i in range(len(c.n)):
                if c.n[i].color == kolor and c.n[i].belongs == c.player.name:
                    premises.append(i)

            suma = 0
            for i in range(len(premises)):
                suma += c.n[premises[i]].domki

            if c.n[premises[0]].x < c.block_size/2:
                odejmij = 200
            elif c.n[premises[0]].y < c.block_size/2:
                odejmij = 50
            elif c.n[premises[0]].y > 9*c.block_size/2:
                odejmij = 150
            else:
                odejmij = 100

            print("odejmij wynosi: ", odejmij)
            if len(premises) == 2:
                print("brazowy lub fioletowy")
                #if suma < 10:
                c.player.money += odejmij
                if suma % 2 == 0:
                    c.n[premises[1]].domki -= 1
                    update_domki(c, premises[1])
                else:
                    c.n[premises[0]].domki -= 1
                    update_domki(c, premises[0])
            else:
                print("3 sztuki")
                #if suma < 15:
                c.player.money += odejmij
                if suma % 3 == 0:
                    c.n[premises[2]].domki -= 1
                    update_domki(c, premises[2])
                elif suma % 3 == 1:
                    c.n[premises[0]].domki -= 1
                    update_domki(c, premises[0])
                else:
                    c.n[premises[1]].domki -= 1
                    update_domki(c, premises[1])

def zastaw(c):
    if c.rendered_field is not None:
        #AAAAAAAAAAAAAAA!!! SPRAWDZ TEZ CZY TO NIE JEST SZANSA, KASA SPOLECZNA ETC, WTEDY HIPOTEKA JEST NONE TYPE
        if not c.rendered_field.pledged:
            c.rendered_field.pledged = True
            c.player.money += c.rendered_field.hipoteka
        else:
            c.rendered_field.pledged = False
            c.player.money -= c.rendered_field.hipoteka

def button_clicked(mouse_pos, rect):
    x, y = mouse_pos
    if x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]:
        return True
    else:
        return False

def update_domki(c, premise_number):
    data = {
        "function": "update_domki",
        "game_name":c.game_name,
        "premise_number": premise_number,
        "ilosc_domkow": c.n[premise_number].domki
    }
    c.network.send(data)