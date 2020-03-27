#settings
import sys

class Settings:
    var1 = 1
    var2 = 2


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

print("rozmiar ulicy: ", sys.getsizeof(Ulica))

cos = ["Mickiewicza", 12]

print("rozmiar cosia: ", sys.getsizeof(cos))

imiona = ["Stas","Jas","Kasia"]

gracz = [gracz for gracz in imiona if gracz == "Kasia"]
print("gracz to: ", gracz)