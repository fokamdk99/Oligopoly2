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

lista1 = [2,3,4,5,6,7,8]
lista2 = []

for i in range(len(lista1)):
    if lista1[i] % 2 == 0:
        lista2.append(lista1[i])

print("lista1: ", lista1)
for i in range(len(lista2)):
    lista2[i] += 10

print("lista1: ", lista1)
print("lista2: ", lista2)

def zwracanie():
    return 1,11

x, y = zwracanie()
print(x, y)