from trening1 import Settings
from trening3 import add_premises, use_class
import re

add_premises(Settings)
use_class(Settings)


'''from trening1 import add_parameter

a = None

def wyswietl():
    print(a)

class Klasa:
    gl1 = 111
    def __init__(self):
        a = 5

    def wyswietl(self):
        print(a)

i1 = Klasa()
i1.wyswietl()
Klasa.b = 7
print(i1.b)
add_parameter(Klasa)
print(i1.c)

print(Klasa.gl1)
print(Klasa.c)'''

text = "Przejdz na dworzec gdanski. Jesli miniesz po drodze START, pobierz 200 zl."

#chunks = text.split()
chunks = re.split(r'(?<=[,.])(?<!\d.)\s', text)
print(chunks)

print(-15 % 40)

secik = {1,2,3}
print(secik)
secik.add(3)
print(secik)