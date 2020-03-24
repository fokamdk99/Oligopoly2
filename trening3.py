#Nieruchomosc
class Premise:
    dom = 3

def add_premises(klasa):
    p1 = Premise()
    p2 = Premise()
    klasa.p1 = p1
    klasa.p2 = p2

def use_class(klasa):
    print(klasa.p1.dom)
    klasa.p1.dom = 5
    print(klasa.p1.dom)