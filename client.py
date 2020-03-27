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

#calculate x and y coordinates for each field
def initialize_fields():
    xpom = 0
    ypom = 0
    for i, val in enumerate(s.n):
        if i < 10:
            s.n[i].x = xpom
            s.n[i].y = ypom
            xpom += s.block_size
        elif i < 20:
            s.n[i].x = xpom
            s.n[i].y = ypom
            ypom += s.block_size
        elif i < 30:
            s.n[i].x = xpom
            s.n[i].y = ypom
            xpom -= s.block_size
        else:
            s.n[i].x = xpom
            s.n[i].y = ypom
            ypom -= s.block_size
        
        print(i, " -> ", s.n[i].x, s.n[i].y)


#sprawdz czy ktos wygral
def winner():
    pass


#create grid and fill with colors
def create_grid():
    grid = [[s.win_color for j in range(s.grid_len)] for i in range(s.grid_len)]

    for i in range(s.grid_len):
        for j in range(s.grid_len):
            if j == 0 or j == (s.grid_len-1) or i == 0 or i == (s.grid_len-1):
                grid[i][j] = s.space_color

    '''for i, val in enumerate(grid):
        print(i, " -> ", val)'''
    return grid

#draw grid on screen
def draw_grid(grid):
    squares = []
    grid = grid
    for i in range(s.grid_len):
        for j in range(s.grid_len):
            square = (j*s.block_size,i*s.block_size,s.block_size,s.block_size)
            pygame.draw.rect(s.win, grid[i][j], square)
            squares.append(square)

            
            #print(square)

    for i in range(grid_len):
        pygame.draw.line(win, (0,0,0),(i*s.block_size,0),(i*s.block_size,s.win_height),3)
        pygame.draw.line(win, (0,0,0), (0,i*s.block_size),(s.grid_len*s.block_size, i*s.block_size),3)

    central_square = (s.block_size+2, s.block_size+2, 9*s.block_size-3, 9*s.block_size-3)
    pygame.draw.rect(s.win, s.win_color, s.central_square)

    return squares

def show_domki(c):
    domek = pygame.Surface((int(c.block_size/2), int(c.block_size/2)))
    domek.set_alpha(100)
    #domek.fill(color)
    for i in range(len(c.n)):
        if c.n[i].domki is not None:
            domek.fill(c.n[i].color)
            plus = int(c.block_size/2)
            for domek in range(c.n[i].domki):
                if domek < 2:
                    c.win.blit(domek, (c.n[i].x + (domek%2)*plus, c.n[i].y))
                else:
                    c.win.blit(domek, (c.n[i].x, c.n[i].y + (domek%2)*plus))

#draw window
def draw_window2(c):
    win.fill(c.win_color)
    grid = create_grid()
    draw_grid(grid)
    #draw_field(c)

#show details about a specific field
def draw_field2(c):
    if c.rendered_field is not None:
        #print("pole o numerze: ", c.rendered_field)
        name = c.font.render(c.rendered_field.name, 1, c.black)
        if c.rendered_field.belongs is not None:
            belongs = c.font.render(c.rendered_field.belongs, 1, c.black)
            if c.rendered_field.pledged == True:
                pledged = c.font.render("zastawione", 1, c.black)
            else:
                pledged = c.font.render("nie zastawione", 1, c.black)
        else:
            belongs = c.font.render("Jeszcze niezakupione", 1, c.black)
            pledged = c.font.render("nie zastawione", 1, c.black)
        
        value = c.font.render(str(c.rendered_field.value), 1, c.black)
        pygame.draw.rect(win, c.bialy, c.central_square)
        win.blit(name, (c.central_square[0] + c.block_size, c.central_square[1] + c.block_size))
        win.blit(value, (c.central_square[0] + c.block_size, c.central_square[1] + 3*c.block_size))
        win.blit(belongs, (c.central_square[0] + c.block_size, c.central_square[1] + 5*c.block_size))
        win.blit(pledged, (c.central_square[0] + c.block_size, c.central_square[1] + 7*c.block_size))

        #czy_domki = sprawdz_domki(c.rendered_field, c)
        if c.czy_domki and c.player.interested:
            show_kup_domek(c)
            show_sprzedaj_domek(c)
        
        if c.rendered_field.belongs == c.player.name and c.player.interested:
            show_zastaw(c)
        #print("czy domki wynosza:", czy_domki)

def manage_draw_window(mouse_pos, c):
    #central_square = (s.block_size+2, s.block_size+2, 9*s.block_size-3, 9*s.block_size-3)
    #font = pygame.font.SysFont("comicsans", 60)
    font = c.font
    mouse_x, mouse_y = mouse_pos
    #field = None

    #zaktualizuj pola: kto je posiada, ile maja domkow
    data = {
        "function":"get_nieruchomosci",
        "game_name":c.game_name
    }
    nieruchomosci = c.network.send(data)

    for i in range(len(c.n)):
        c.n[i].belongs = nieruchomosci[i][0]
        c.n[i].domki = nieruchomosci[i][1]

    previous_field = c.rendered_field
    next_field = None
    for i in range(len(s.n)):
        if (mouse_x >= s.n[i].x and mouse_x <= s.n[i].x + s.block_size) and (mouse_y >= s.n[i].y and mouse_y <= s.n[i].y + s.block_size):
            next_field = s.n[i]
            break

    #jesli gracz nacisnie na inne pole, pokaza sie informacje na jego temat; jesli kliknal na to
    #samo pole lub nie kliknal na zadne pole w ogole, informacje o dotychczasowym polu znikna
    if next_field is None or previous_field == next_field:
        c.rendered_field = None
    else:
        c.rendered_field = next_field

    #jesli gracz kliknie mysza wewnatrz planszy, to nie chcemy zamykac okna z nieruchomoscia
    #po to, by gracz mogl wykonac ewentualny zakup domkow, zastawienie itp.
    czy_wewnatrz_planszy = button_clicked(mouse_pos, c.central_square)
    if czy_wewnatrz_planszy:
        c.rendered_field = previous_field

    c.czy_domki = sprawdz_domki(c.rendered_field, c)

    if czy_wewnatrz_planszy and previous_field is not None and c.player.interested:
        czy_kup_domek = button_clicked(mouse_pos, c.kup_domek_rect)
        czy_sprzedaj_domek = button_clicked(mouse_pos, c.sprzedaj_domek_rect)
        czy_zastaw = button_clicked(mouse_pos, c.zastaw_rect)

        if czy_kup_domek:
            kup_domek(c)
        if czy_sprzedaj_domek:
            sprzedaj_domek(c)
        if czy_zastaw:
            zastaw(c)
            


def main2():
    print("right_square to: ", right_square)
    print("finish_square to: ", s.finish_square)
    print("player_tab to: ", s.player_tab)
    s.rendered_field = None
    s.czy_domki = False
    s.lista_zakupow = []
    s.lista_sprzedazy = []
    s.negocjowana_kwota = ""
    s.kursor = 0
    s.otrzymane_oferty = 0
    s.nr_oferty = -1 #przydatne w functionality do ustalenia ktora oferte wyswietlic
    s.clock = pygame.time.Clock()
    #wyswietlaj plansze, kontroluj gracza i wykonywane przez niego czynnosci,
    #aktualizuj dzialania innych graczy

    #do poprawy w wersji ostatecznej
    s.game_name="dev_game"
    #do poprawy w wersji ostatecznej

    run = True
    s.network = Network()
    #s.player = Player(1, "Stas", (255,0,0), "gierka")
    data = {
        "function":"get_players",
        "game_name": s.game_name
    }
    act = s.network.send(data)
    s.players = act["players"]
    s.player = s.players[0]

    print("odpalam main2")
    initialize_fields()
    
    data = {
        "function":"get_nieruchomosci",
        "game_name":s.game_name
    }
    nieruchomosci = s.network.send(data)

    for i in range(len(s.n)):
        s.n[i].belongs = nieruchomosci[i][0]
        print("wlasnosc: ", nieruchomosci[i][0])
        s.n[i].domki = nieruchomosci[i][1]

    
    while run:
        data = {
            "function": "update_players2",
            "game_name":s.game_name,
            "name" : s.player.name,
            "money": s.player.money,
            "pos": s.player.pos,
            "x": s.player.x,
            "y": s.player.y,
            "interested": s.player.interested,
            "movement": s.player.movement,
            "wait": s.player.wait
        }
        
        act = s.network.send(data)
        s.player = act["player"]
        #c.players = act["players"] na pozniej

        draw_window2(s)
        draw_field2(s)
        #players = functionality2.update_players(network, game_name)
        #player = players[player_number]
        #player.control_movement(network)
        s.player.draw_player2(s)
        #functionality2.draw_players(players)
        manage(s)
        rules_manage(s)
        pygame.display.update()

        s.clock.tick()
        #rusz sie graczem
        #narysuj gracza
        #narysuj reszte graczy
        #sprawdz co zrobil gracz(negocjacje, kupno, inne functionality)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                keyboard_action(event, s)

                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_action(s.player)
    
    


def keyboard_action(event, c):
    c.player.move2(event, c)
    negocjuj_gotowke(event, c)
    if event.key == pygame.K_RETURN:
        c.player.interested = False
    

def mouse_action(player):
    mouse_pos = pygame.mouse.get_pos()
    #draw_field2(mouse_pos, s)
    manage_draw_window(mouse_pos, s)
    show_status(mouse_pos, s)
    accept_offer(mouse_pos, s)
    rules_show_status(mouse_pos, s)
    negocjuj(mouse_pos, s)
    show_oferta(mouse_pos, s)
    accept_negocjacje(mouse_pos, s)
    
    x, y = mouse_pos
    if x >= s.finish_square[0] and x <= s.finish_square[0] + s.finish_square[2] and y >= s.finish_square[1] and y <= s.finish_square[1] + s.finish_square[3]:
        s.player.interested = False


main2()