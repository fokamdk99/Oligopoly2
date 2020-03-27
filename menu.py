'''#import settings
import pygame
from settings import globaldict as gdict
from settings import init
from classes import config_classes

pygame.init()
pygame.font.init()
#screen_size = pygame.display.Info()

win_width = 1200
#win_width = screen_size.current_w
win_height = 650
#win_height = screen_size.current_h
#win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Oligopoly")
font = pygame.font.SysFont("comicsans", 60)
updt = {
    "win_width":win_width,
    "win_height":win_height,
    "win":win,
    "font":font
}
gdict.update(updt)
init()
gdict.update(config_classes(gdict))

import client
import network
import pickle

#from classes import Player

#gdict = settings.init()

#gdict = settings.globaldict
pygame.init()
pygame.font.init()
right_square = gdict["right_square"]
block_size = gdict["block_size"]
win_width = gdict["win_width"]
win_height = gdict["win_height"]
win = gdict["win"]
font = gdict["font"]
bialy = gdict["bialy"]
zielony = gdict["zielony"]
zolty = gdict["zolty"]
niebieski = gdict["niebieski"]
black = gdict["black"]'''

import pygame
from settings import Settings as s

pygame.init()
pygame.font.init()
screen_size = pygame.display.Info()
#win_width = screen_size.current_w
#win_height = screen_size.current_h
win_width = 1100
win_height = 600
win = pygame.display.set_mode((win_width,win_height))
win_rect = (0,0,win_width,win_height)
grid_len = 11
block_size = int(win_height/grid_len)
central_square = (block_size+2, block_size+2, 9*block_size-3, 9*block_size-3)
right_square = (grid_len*block_size, 0, win_width, win_height)
font = pygame.font.SysFont("comicsans", 60)
small_font = pygame.font.SysFont("comicsans", 30)
s.win_width = win_width
s.win_height = win_height
s.win = win
s.win_rect = win_rect
s.grid_len = grid_len
s.block_size = block_size
s.central_square = central_square
s.right_square = right_square
s.font = font
s.small_font = small_font

from functionality2 import functionality2_add_settings
from classes import classes_add_settings
from rules import rules_add_settings, rules_manage, rules_show_status

classes_add_settings(s)
functionality2_add_settings(s)
rules_add_settings(s)

from classes import Player
from functionality2 import manage, show_status, accept_offer, negocjuj, negocjuj_gotowke, show_oferta, accept_negocjacje
from network import Network
from rules import sprawdz_domki, button_clicked, show_kup_domek, show_sprzedaj_domek, show_zastaw, kup_domek, sprzedaj_domek, zastaw

full_screen = (0,0,win_width,win_height)
new_game_btn = (0,0,int(0.1*win_width),win_width)
okno_poczatkowe_options = ["graj", "wyjdz"]
connect_to_game_options = ["nowa gra", "wyjdz"]

#stworz te obiekty, ktore pozniej beda wyswietlane w oknie poczatkowym
def create_menu(options, znacznik):
    choice = []
    for i in range(len(options)):
        choice.append(font.render(options[i], 1, black))
    
    choice[znacznik] = font.render(options[znacznik], 1, zielony)
    
    return choice


#wyswietl obiekty w oknie poczatkowym
def show_menu(znacznik):
    title = font.render("Oligopoly", 1, niebieski)
    choice = create_menu(okno_poczatkowe_options, znacznik)

    pygame.draw.rect(win, bialy, full_screen)
    win.blit(title, (200, 100))
    for i in range(len(choice)):
        win.blit(choice[i], (200, (i+1)*200))
    
#wyswietl okno utworzenia nowej gry, zapamietaj i zwroc dane odnosnie tej gry
def create_new_game(mouse_pos = (1,1)):
    x, y = mouse_pos
    if x >= new_game_btn[0] and x <= new_game_btn[2] and y >= new_game_btn[1] and y <= new_game_btn[3]:
        run_create_new_game = True
        pygame.draw.rect(win, bialy, (0,0,win_width,win_height))
        wprowadz_nazwe = True
        wprowadz_haslo = False
        wprowadz_ilosc_graczy = False
        prompt_nazwa = font.render("Wprowadz nazwe",1,black)
        prompt_haslo = font.render("Wprowadz haslo",1,black)
        prompt_ilosc_graczy = font.render("Ile osob moze wziac udzial?",1,black)
        context = {}
        name = ""
        
        while run_create_new_game:
            pygame.draw.rect(win, bialy, (0,0,win_width,win_height))
            if wprowadz_nazwe:
                win.blit(prompt_nazwa, (int(0.11*win_width), int(0.09*win_height)))
            elif wprowadz_haslo:
                win.blit(prompt_haslo, (int(0.11*win_width), int(0.09*win_height)))
            else:
                win.blit(prompt_ilosc_graczy, (int(0.11*win_width), int(0.09*win_height)))

            tmp = font.render(name, 1, zielony)
            win.blit(tmp, (int(0.11*win_width), int(0.09*win_height) + 80))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha() or event.unicode.isnumeric():
                        name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if wprowadz_nazwe:
                            wprowadz_nazwe = False
                            wprowadz_haslo = True
                            context["nazwa"] = name
                            print("nazwa gry to: ", name)
                            name = ""
                        elif wprowadz_haslo:
                            wprowadz_haslo = False
                            wprowadz_ilosc_graczy = True
                            context["haslo"] = name
                            print("haslo gry to: ", name)
                            name = ""
                        else:
                            print("przed: ilosc graczy to: ", name)
                            context["ilosc_graczy"] = int(name)
                            print("ilosc graczy to: ", context["ilosc_graczy"])
                            run_create_new_game = False

        return context
    else:
        return None

def wait_for_game(ready, player_number, nazwa, n):
    if ready:
        client.main2(player_number, n, nazwa)
    else:
        run_wait_for_game = True
        while run_wait_for_game:
            pygame.draw.rect(win, bialy, full_screen)
            czekam = font.render("Czekam na rozpoczecie rozgrywki", 1, black)
            win.blit(czekam, (10,100))
            pygame.display.update()
            data = {
                "function":"ready_check",
                "nazwa": nazwa

            }
            ready = n.send(data)
            if ready:
                client.main2(player_number, n, nazwa)
                run_wait_for_game = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run_wait_for_game = False
                        data = {
                            "function": "remove_player_from_game",
                            "nazwa": nazwa
                        }
                        confirmation = n.send(data)
                        print("confirmation wynosi: ", confirmation)
    
def main_menu2():
    #global run
    run1 = True
    znacznik_main_menu = 0
    while run1:
        show_menu(znacznik_main_menu)
        pygame.display.update()

        act = handle_main_menu(znacznik_main_menu)
        run1 = act["run"]
        znacznik_main_menu = act["znacznik"]
        if not run1:
            pygame.display.quit()
            pygame.quit()

def handle_main_menu(znacznik):
    run_main_menu = True
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_main_menu = False

            act = keyboard_action(event, okno_poczatkowe_options, znacznik)
            run_main_menu = act["run"]
            znacznik = act["znacznik"]
            execute = act["execute"]
            if execute:
                run_main_menu = execute3(znacznik)

    context = {
        "run": run_main_menu,
        "znacznik":znacznik
    }

    return context

def keyboard_action(event, options, znacznik):
    run = True
    execute = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            znacznik = (znacznik + 1) % len(options)
        elif event.key == pygame.K_UP:
            znacznik = (znacznik - 1) % len(options)
        elif event.key == pygame.K_ESCAPE:
            run = False
        elif event.key == pygame.K_RETURN:
            #execute(znacznik)
            #run = globals()[function](znacznik, options, n)
            execute = True

    context = {
        "run":run,
        "znacznik": znacznik,
        "execute": execute
    }

    return context

def execute3(znacznik):
    run = True
    if znacznik == 0:
        #client.main()
        connect_to_game2()
    elif znacznik == 1:
        run = False

    return run

def connect_to_game2():
    znacznik_connect_to_game = 0
    run_connect_to_game = True
    n = network.Network()
    signal = n.getP()
    data = {
        "function":"get_games"
    }
    games_available = n.send(data)
    
    while run_connect_to_game:
        options = []
        options += connect_to_game_options
        for i in range(len(games_available)):
            options.append(games_available[i].name)
        show_connect_to_game(options, znacznik_connect_to_game)

        for event in pygame.event.get():
            act = keyboard_action(event, options, znacznik_connect_to_game)
            run_connect_to_game = act["run"]
            znacznik_connect_to_game = act["znacznik"]
            execute = act["execute"]
            if execute:
                act2 = execute4(znacznik_connect_to_game, options, n)
                run_connect_to_game = act2["run"]
                if "games_available" in act2.keys():
                    games_available = act2["games_available"]
            #rezygnuje z opcji wyboru mysza, mozesz to zakodowac ew. pozniej

def show_connect_to_game(options, znacznik):
    choose_game = font.render("Dolacz do gry",1,zielony)
    pygame.draw.rect(win, niebieski, (0,0,win_width, win_height))
    pygame.draw.rect(win, zolty, new_game_btn)
    win.blit(choose_game,(int(0.11*win_width),int(0.09*win_height)))
    if len(options) > 2:
        for i in range(2,len(options)):
            if znacznik == i:
                win.blit(font.render(options[i],1,zielony), (int(0.11*win_width), int(0.09*win_height + 80*(i+1))))
            else:
                win.blit(font.render(options[i],1,black), (int(0.11*win_width), int(0.09*win_height + 80*(i+1))))
    else:
        win.blit(font.render("brak dostepnych gier", 1, black), (int(0.11*win_width), int(0.09*win_height + 80)))

    
    win.blit(font.render(options[0],1,black), (int(0.11*win_width), int(0.9*win_height)))
    win.blit(font.render(options[1],1,black), (int(0.6*win_width), int(0.9*win_height)))
    if znacznik == 0:
        win.blit(font.render(options[0],1,zielony), (int(0.11*win_width), int(0.9*win_height)))
    elif znacznik == 1:
        win.blit(font.render(options[1],1,zielony), (int(0.6*win_width), int(0.9*win_height)))
    pygame.display.update()

def execute4(znacznik, options, n):
    run_connect_to_game = True
    context = {
        "run": run_connect_to_game
    }
    if znacznik == 0:
        new_game = create_new_game()
        rdict = add_new_game2(new_game, n)
        games_available = rdict["games_available"]
        context["games_available"] = games_available
    elif znacznik == 1:
        run_connect_to_game = False
        context["run"] = run_connect_to_game
    else:
        data = {
            "function": "add_player_to_game",
            "nazwa": options[znacznik]
        }
        #ready = n.send(data)
        print("execute4 przed wyslaniem")
        act = n.send(data)
        print("execute4 po wyslaniu")
        ready = act["ready"]
        player_number = act["player_number"]
        print("execute4 wchodze w wait")
        wait_for_game(ready, player_number, options[znacznik], n)

    return context

def add_new_game2(new_game, n):    
    data = {
        "function":"create_new_game",
        "game":new_game
    }
    games_available = n.send(data)
    
    context = {
        "games_available": games_available
    }

    return context

main_menu2()