import pygame
from random import seed, randint
from rules import rulebook, Rules

class Nieruchomosc:
    
    def __init__(self, name, group, value, color=None, hipoteka = None):
        self.name = name
        self.group = group #ulica, szansa, kasa spoleczna, dworzec
        self.belongs = None
        self.pledged = False #czy w zastawie
        self.value = value
        self.color = color #czy zielone czy rozowe, podawane w rgb!!!
        self.x = None
        self.y = None
        self.hipoteka = hipoteka
        #self.game_name = game_name#po co?

    def display():
        pass


class Ulica(Nieruchomosc):
    def __init__(self, zero, jeden, dwa, trzy, cztery, hotel, hipoteka, name, group, value, color = None):
        super().__init__(name, group, value, color)
        self.domki = 0
        self.oplaty = []
        self.oplaty.append(zero)
        self.oplaty.append(jeden)
        self.oplaty.append(dwa)
        self.oplaty.append(trzy)
        self.oplaty.append(cztery)
        self.oplaty.append(hotel)
        self.hipoteka = hipoteka

class Player:
    #players_number = 0
    def __init__(self, id, name, color, game_name, money=1500):
        self.id = id
        self.name = name
        self.game_name = game_name
        self.money = money
        self.premises = None
        self.pos = 0
        #self.image = self.create_image(name)
        self.image = self.create_image(color)
        self.x = self.image["coordinates"][0]
        self.y = self.image["coordinates"][1]
        self.interested = False #zmienna pomocnicza np. gdy gra oczekuje od gracza decyzji,
        #czy chce kupic dana posiadlosc. Dopoki sie nie zdecyduje, nie moze sie ruszyc dalej
        self.juz_kupione = False #zmienna pomocnicza, np. gdy gracz juz cos kupil, ale nadal jest
        #jego ruch
        self.movement = False #zmienna zalezna od serwera: jesli serwer daje info, ze gracz moze
        #sie ruszyc, to wartosc jest zmieniana na True
        self.wait = False

    def create_image(self, color):
        square = {"color":color, "size":40,"coordinates": (self.id*10, self.id*10)}
        return square

    def draw_player2(self, c):
        square = (self.x, self.y, self.image["size"], self.image["size"])
        pygame.draw.rect(c.win, self.image["color"], square)

    def move_engine(self, value, c):
        if (self.pos + value) % 40 < self.pos:
                    self.money += 200

        for i in range(value):
            
            if self.pos < 10:
                self.x += c.block_size
            elif self.pos < 20:
                self.y += c.block_size
            elif self.pos < 30:
                self.x -= c.block_size
            else:
                self.y -= c.block_size

            self.pos = (self.pos + 1) % 40
    
    #poruszanie sie gracza, zwraca czy gracz sie ruszyl czy nie
    def move2(self, event, c):
        #self.control_movement(network)
        print("interested: ", self.interested, ", movement: ", self.movement, ", wait: ", self.wait)

        #if (not self.interested) and self.movement and (not self.wait):
        if not self.interested:
            print("move2 dziala poprawnie")
            if event.key == pygame.K_UP:
                value = randint(1,12)
                self.wait = True
                self.interested = True
                self.juz_sprawdzone = False
                #sprawdz czy zawodnik przeszedl przez start
                self.move_engine(value, c)
                
                rulebook[c.n[c.player.pos].group](c)
                
    def control_movement(self, network):
        tmp = self.movement

        if self.interested == False and self.movement == True:
            data = {
                "function":"next_move",
                "game_name": self.game_name
            }
            network.send(data)
        
        data = {
            "function":"get_players",
            "nazwa": self.game_name
        }
        act = network.send(data)
        move = act["move"]
        if move == self.id:
            self.movement = True
        else:
            self.movement = False
        
        #sprawdz czy serwer odebral graczowi ruch(bo gracz juz swoj ruch wykonal)
        if self.movement != tmp and tmp == True:
            self.wait = False



def classes_add_settings(c): #c to klasa
    bialy = c.bialy
    brazowy = c.brazowy
    niebieski = c.niebieski
    rozowy = c.rozowy
    pomaranczowy = c.pomaranczowy
    czerwony = c.czerwony
    zolty = c.zolty
    zielony = c.zielony
    fioletowy = c.fioletowy
    
    n = []
    n.append(Nieruchomosc("start","start",0,bialy))
    n.append(Ulica(2,10,30,90,160,250,30,"konopacka","ulica",60,brazowy))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica(4,20,60,180,320,450,30,"stalowa","ulica",60,brazowy))
    n.append(Nieruchomosc("podatek dochodowy","podatek_dochodowy",0,bialy))
    n.append(Nieruchomosc("dworzec zachodni","dworzec",200,brazowy))
    n.append(Ulica(6,30,90,270,400,550,50,"radzyminska","ulica",100,niebieski))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica(6,30,90,270,400,550,50,"jagiellonska","ulica",100,niebieski))
    n.append(Ulica(8,40,100,300,450,600,60,"targowa","ulica",120,niebieski))
    n.append(Nieruchomosc("wiezenie/odwiedzajacy","wiezienie",0,bialy))
    n.append(Ulica(10,50,150,450,625,750,70,"plowiecka","ulica",140,rozowy))
    n.append(Nieruchomosc("elektrownia","elektrownia",0,bialy, 75))
    n.append(Ulica(10,50,150,450,625,750,70,"marsa","ulica",140,rozowy))
    n.append(Ulica(12,60,180,500,700,900,80,"grochowska","ulica",160,rozowy))
    n.append(Nieruchomosc("dworzec gdanski","dworzec",200,bialy,100))
    n.append(Ulica(14,70,200,550,750,950,90,"obozowa","ulica",180,pomaranczowy))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica(14,70,200,550,750,950,90,"gorczewska","ulica",180,pomaranczowy))
    n.append(Ulica(16,80,220,600,800,1000,100,"wolska","ulica",200,pomaranczowy))
    n.append(Nieruchomosc("bezplatny parking","parking",0,bialy))
    n.append(Ulica(18,90,250,700,875,1050,110,"mickiewicza","ulica",220,czerwony))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica(18,90,250,700,875,1050,110,"slowackiego","ulica",220,czerwony))
    n.append(Ulica(20,100,300,750,925,1100,120,"plac wilsona","ulica",240,czerwony))
    n.append(Nieruchomosc("dworzec wschodni","dworzec",200,bialy,100))
    n.append(Ulica(22,110,330,800,975,1150,130,"swietokrzyska","ulica",260,zolty))
    n.append(Ulica(22,110,330,800,975,1150,130,"krakowskie przedmiescie","ulica",260,zolty))
    n.append(Nieruchomosc("wodociagi","wodociagi",0,bialy,75))
    n.append(Ulica(24,120,360,850,1025,1200,140,"nowy swiat","ulica",280,zolty))
    n.append(Nieruchomosc("idz do wiezienia","idz_do_wiezienia",0,bialy))
    n.append(Ulica(26,130,390,900,1100,1275,150,"plac trzech krzyzy","ulica",300,zielony))
    n.append(Ulica(26,130,390,900,1100,1275,150,"marszalkowska","ulica",300,zielony))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica(28,150,450,1000,1200,1400,160,"aleje jerozolimskie","ulica",320,zielony))
    n.append(Nieruchomosc("dworzec centralny","dworzec",200,bialy, 100))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica(35,175,500,1100,1300,1500,175,"belwederska","ulica",350,fioletowy))
    n.append(Nieruchomosc("domiar podatkowy","podatek",0,bialy))
    n.append(Ulica(50,200,600,1400,1700,2000,200,"aleje ujazdowskie","ulica",400,fioletowy))
    
    c.n = n


'''
n.append(Nieruchomosc("start","start",0,bialy))
    n.append(Ulica("konopacka","ulica",60,brazowy))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica("stalowa","ulica",60,brazowy))
    n.append(Nieruchomosc("podatek dochodowy","podatek_dochodowy",0,bialy))
    n.append(Nieruchomosc("dworzec zachodni","dworzec",200,brazowy))
    n.append(Ulica("radzyminska","ulica",100,niebieski))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica("jagiellonska","ulica",100,niebieski))
    n.append(Ulica("targowa","ulica",120,niebieski))
    n.append(Nieruchomosc("wiezenie/odwiedzajacy","wiezienie",0,bialy))
    n.append(Ulica("plowiecka","ulica",140,rozowy))
    n.append(Nieruchomosc("elektrownia","elektrownia",0,bialy))
    n.append(Ulica("marsa","ulica",140,rozowy))
    n.append(Ulica("grochowska","ulica",160,rozowy))
    n.append(Nieruchomosc("dworzec gdanski","dworzec",200,bialy))
    n.append(Ulica("obozowa","ulica",180,pomaranczowy))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica("gorczewska","ulica",180,pomaranczowy))
    n.append(Ulica("wolska","ulica",200,pomaranczowy))
    n.append(Nieruchomosc("bezplatny parking","parking",0,bialy))
    n.append(Ulica("mieckiewicza","ulica",220,czerwony))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica("slowackiego","ulica",220,czerwony))
    n.append(Ulica("plac wilsona","ulica",240,czerwony))
    n.append(Nieruchomosc("dworzec wschodni","dworzec",200,bialy))
    n.append(Ulica("swietokrzyska","ulica",260,zolty))
    n.append(Ulica("krakowskie przedmiescie","ulica",260,zolty))
    n.append(Nieruchomosc("wodociagi","wodociagi",0,bialy))
    n.append(Ulica("nowy swiat","ulica",280,zolty))
    n.append(Nieruchomosc("idz do wiezienia","idz_do_wiezienia",0,bialy))
    n.append(Ulica("plac trzech krzyzy","ulica",300,zielony))
    n.append(Ulica("marszalkowska","ulica",300,zielony))
    n.append(Nieruchomosc("kasa spoleczna","szansa",0,bialy))
    n.append(Ulica("aleje jerozolimskie","ulica",320,zielony))
    n.append(Nieruchomosc("dworzec centralny","dworzec",200,bialy))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica("belwederska","ulica",350,fioletowy))
    n.append(Nieruchomosc("domiar podatkowy","podatek",0,bialy))
    n.append(Ulica("aleje ujazdowskie","ulica",400,fioletowy))'''