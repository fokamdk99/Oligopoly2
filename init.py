from classes import config_classes
from settings import init

def setup():
    globaldict = init()
    nieruchomosci = config_classes(globaldict)
    globaldict.update(nieruchomosci)
    return globaldict

globaldict = setup()

