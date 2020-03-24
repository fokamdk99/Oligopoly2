import random

class Game:
    def __init__(self, id, name, password, number_of_players, szanse, kasy_spoleczne):
        self.id = id
        self.name = name
        self.password = password
        self.number_of_players = number_of_players
        self.players = [] #store instances of players
        self.queue = 0 #zmienna pomocnicza przy zapisywaniu graczy do gry
        self.ready = False
        self.move = random.randrange(number_of_players) #kto aktualnie ma ruch
        self.szanse = random.sample(range(szanse), szanse)
        self.szansa = 0
        self.ilosc_szans = szanse
        self.kasy_spoleczne = random.sample(range(kasy_spoleczne), kasy_spoleczne)
        self.kasa_spoleczna = 0
        self.ilosc_kas = kasy_spoleczne
        self.nieruchomosci = self.init_nieruchomosci()

    def init_nieruchomosci(self):
        self.nieruchomosci = []
        for i in range(40):
            #calkowicie wersja debug ;)
            if i < 20:
                self.nieruchomosci.append(["Kasia", 0]) #pierwszy argument to nazwa gracza, drugi to ilosc domkow
            else:
                self.nieruchomosci.append(["Stas", 0])

        return self.nieruchomosci


    def losuj_szanse(self):
        szansa = self.szanse[self.szansa]
        self.szansa = (self.szansa + 1) % self.ilosc_szans
        return szansa

    def losuj_kase(self):
        kasa = self.kasy_spoleczne[self.kasa_spoleczna]
        self.kasa_spoleczna = (self.kasa_spoleczna + 1) % self.ilosc_kas
        return kasa
    
    def add_player(self):
        self.queue += 1
        if self.queue == self.number_of_players:
            self.ready = True

        return self.ready

    def play(self):
        #przyznawaj graczom po kolei mozliwosc ruchu,
        #np. mozesz rowniez kontrolowac czas, po ktorym nastepny gracz ma ruch
        self.move = (self.move + 1) % self.number_of_players
        print("game.play(): ruch ma gracz nr: ", self.move)
        return self.move

    def connected(self):
        return self.ready

    def winner(self):
        #wybierz zwyciezce gry
        pass