import pygame
#import settings2
#from classes import Nieruchomosc, Ulica

#settings2.init()
#globaldict = settings2.globaldict

globaldict = {}

def init():
    global globaldict
    pygame.init()
    pygame.font.init()
    #pygame.mouse.set_visible(True)

    global globaldict
    globaldict = {}
    
    #global screen_size
    screen_size = pygame.display.Info()
    globaldict['screen_size'] = screen_size
    print("screen_size to",screen_size.current_h, screen_size.current_w)
    #global win_width
    win_width = 1200
    #win_width = screen_size.current_w
    globaldict['win_width'] = win_width
    #global win_height
    win_height = 650
    #win_height = screen_size.current_h
    globaldict['win_height'] = win_height
    #global win
    #win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    win = pygame.display.set_mode((win_width,win_height))
    globaldict['win'] = win
    #global win_color
    win_color = (255,255,128)
    globaldict['win_color'] = win_color
    #global space_color
    space_color = (255,255,255)
    globaldict['space_color'] = space_color
    #global win_rect
    #win_rect = (0,0,win_width,win_height)
    win_rect = (0,0,globaldict["win_width"],globaldict["win_height"])
    globaldict['win_rect'] = win_rect
    #pygame.display.set_caption("Oligopoly")
    #global grid_len
    grid_len = 11
    globaldict['grid_len'] = grid_len
    #global block_size
    #block_size = int(win_height/grid_len)
    block_size = int(globaldict["win_height"]/grid_len)
    globaldict['block_size'] = block_size
    #global bialy
    bialy = (255,255,255)
    globaldict['bialy'] = bialy
    #global brazowy
    brazowy = (120,60,0)
    globaldict['brazowy'] = brazowy
    #global niebieski
    niebieski = (36,178,255)
    globaldict['niebieski'] = niebieski
    #global rozowy
    rozowy = (255,103,129)
    globaldict['rozowy'] = rozowy
    #global pomaranczowy
    pomaranczowy = (231,68,0)
    globaldict['pomaranczowy'] = pomaranczowy
    #global czerwony
    czerwony = (255,0,0)
    globaldict['czerwony'] = czerwony
    #global zolty
    zolty = (252,242,0)
    globaldict['zolty'] = zolty
    #global zielony
    zielony = (0,199,20)
    globaldict['zielony'] = zielony
    #global fioletowy
    fioletowy = (120,0,94)
    globaldict['fioletowy'] = fioletowy
    #global black
    black = (0,0,0)
    globaldict['black'] = black
    bialy = (255,255,255)
    globaldict['bialy'] = bialy
    #global central_square
    central_square = (block_size+2, block_size+2, 9*block_size-3, 9*block_size-3)
    globaldict['central_square'] = central_square
    #global right_square
    #right_square = (grid_len*block_size, 0, win_width, win_height)
    right_square = (grid_len*block_size, 0, globaldict["win_width"], globaldict["win_height"])
    globaldict['right_square'] = right_square

    #global font
    #font = pygame.font.SysFont("comicsans", 60)
    #globaldict['font'] = font

    #pygame.quit()
    #global n
    '''n = []
    n.append(Nieruchomosc("start","start",0,bialy))
    n.append(Ulica("konopacka","ulica",60,brazowy))
    n.append(Nieruchomosc("kasa spoleczna","kasa spoleczna",0,bialy))
    n.append(Ulica("stalowa","ulica",60,brazowy))
    n.append(Nieruchomosc("podatek dochodowy","podatek dochodowy",0,bialy))
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
    n.append(Nieruchomosc("kasa spoleczna","kasa spoleczna",0,bialy))
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
    n.append(Nieruchomosc("idz do wiezienia","idz do wiezienia",0,bialy))
    n.append(Ulica("plac trzech krzyzy","ulica",300,zielony))
    n.append(Ulica("marszalkowska","ulica",300,zielony))
    n.append(Nieruchomosc("kasa spoleczna","kasa spoleczna",0,bialy))
    n.append(Ulica("aleje jerozolimskie","ulica",320,zielony))
    n.append(Nieruchomosc("dworzec centralny","dworzec",200,bialy))
    n.append(Nieruchomosc("szansa","szansa",0,bialy))
    n.append(Ulica("belwederska","ulica",350,fioletowy))
    n.append(Nieruchomosc("domiar podatkowy","podatek",0,bialy))
    n.append(Ulica("aleje ujazdowskie","ulica",400,fioletowy))
    globaldict['n'] = n'''

    player_colors = [zielony, czerwony, niebieski, pomaranczowy, zolty, fioletowy]
    globaldict['player_colors'] = player_colors

    return globaldict

#globaldict = init()

class Settings:
    win_color = (255,255,128)
    space_color = (255,255,255)
    bialy = (255,255,255)
    brazowy = (120,60,0)
    niebieski = (36,178,255)
    rozowy = (255,103,129)
    pomaranczowy = (231,68,0)
    czerwony = (255,0,0)
    zolty = (252,242,0)
    zielony = (0,199,20)
    fioletowy = (120,0,94)
    black = (0,0,0)
    bialy = (255,255,255)
    player_colors = [zielony, czerwony, niebieski, pomaranczowy, zolty, fioletowy]