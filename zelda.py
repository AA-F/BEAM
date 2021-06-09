import pygame
import random
import math

pygame.init()

###  ustawienia ekranu i inne technikalia  ###

szerokosc = 800
wysokosc = 600
ekran = pygame.display.set_mode((szerokosc, wysokosc))
background = pygame.image.load("background.jpg")           # obrazek tła

gracz_obrazek_neutralny = pygame.image.load('normalka.png')
gracz_obrazek_ruchu_strony = [pygame.image.load('Ruch pl_1.png'), pygame.image.load('Ruch pl_1.png')]
gracz_obrazek_ruchu_goradol = [pygame.image.load('Ruch gd_1.png'), pygame.image.load('Ruch gd_2.png')]
przeciwnik_obrazek = pygame.image.load('przeciwnik.png')
pocisk_obrazek = pygame.image.load('fire_arrow.png')

pygame.display.set_caption("Pacyfistyczna Zelda na programowańsko YEEHAW")
ikona_gry = pygame.image.load('icon.png')
pygame.display.set_icon(ikona_gry)

# napis SCORE i GAME OVER #

score_text = pygame.font.SysFont('monospace', 30, True)
game_over_text = pygame.font.SysFont('monospace', 64, True)


#######################################################

"""#######              GRACZ               ######"""

#######################################################


######     RUCH GRACZA     ######


gracz_ruch_strony = False  # prawo - lewo
gracz_ruch_goradol = False  # góra - dół

def animacja_ruchu_gracza():
    global klatki
    if klatki + 1 >= 3:
        klatki = 0
    if gracz_ruch_strony == False and gracz_ruch_goradol == False:  # gracz sie nie rusza
        ekran.blit(gracz_obrazek_neutralny, (gracz_pozycja_x, gracz_pozycja_y))
    elif gracz_ruch_strony == True:         # gracz rusza sie horyzontalnie
        ekran.blit(gracz_obrazek_ruchu_strony[klatki], (gracz_pozycja_x, gracz_pozycja_y))
        klatki += 1
    elif gracz_ruch_goradol == True:            # gracz rusza sie wertykalnie
        ekran.blit(gracz_obrazek_ruchu_goradol[klatki], (gracz_pozycja_x, gracz_pozycja_y))
        klatki += 1

def gracz(x, y):
    ekran.blit(gracz_obrazek_neutralny, (x, y))  # Wielkosc 64X64
    pygame.draw.rect(ekran, (250, 0, 0), (gracz_pozycja_x, gracz_pozycja_y - 20, gracz_zdrowie, 10))
    #"""trzeba bedzie przeniesc ten pasek gdzies indziej"""

gracz_pozycja_x = 370 #pozycja gracza (tutaj poczatkowa)
gracz_pozycja_y = 480
gracz_pozycja_x_zmiana = 0
gracz_pozycja_y_zmiana = 0
gracz_szybkosc = 1.8
score = 0
gracz_zdrowie = 64


#######################################################

"""#######              PRZECIWNIK               ######"""

#######################################################

# pozycja, gracz_szybkosc, generalnie taki __init__
przeciwnik_pozycja_x = random.randint(0, 800)
przeciwnik_pozycja_y = random.randint(50, 150)
przeciwnik_pozycja_x_zmiana = 0
przeciwnik_pozycja_y_zmiana = 0
przeciwnik_szybkosc = 0.5

def przeciwnik(x, y):
    ekran.blit(przeciwnik_obrazek, (x, y))  # Wielkosc 64X64
    pygame.draw.rect(ekran, (250,0,0), (przeciwnik_pozycja_x, przeciwnik_pozycja_y - 20, 64,10))




def ekran_zmiana():
    global gracz_zdrowie  # Do "rysowania" na ekranie
    global gracz_pozycja_x
    global gracz_pozycja_y
    # ekran.fill("background.tif")
    ekran.blit(background, (0,0))

    gracz(gracz_pozycja_x, gracz_pozycja_y)
    przeciwnik(przeciwnik_pozycja_x, przeciwnik_pozycja_y)
    text = score_text.render("Wynik: " + str(score), 1, (0, 0, 0))
    ekran.blit(text, (600, 20))
    if gracz_zdrowie <= 0:
        ekran.fill((0, 0, 0))
        gracz_pozycja_x = 2000
        gracz_pozycja_y = 2000
        game_over = game_over_text.render("GAME OVER", 1, (250, 0, 0))#kolor RGB napisu po 'game over'
        ekran.blit(game_over, (225, 185)) #polozenie napisu
    animacja_ruchu_gracza()
    pygame.display.update()


################


def wystrzal_pocisku(x, y):
    global stan_pocisku
    stan_pocisku = "wystrzał"
    ekran.blit(pocisk_obrazek, (x + 16, y + 10))

pociskX = 0
pociskY = 480
pociskX_zmiana = 0
pociskY_zmiana = 10
stan_pocisku = "gotowa"  # gotowa - gdy nie widać pocisku/ wystrzał - gdy widać pocisk
###


def czy_kolizja(przeciwnik_pozycja_x, przeciwnik_pozycja_y, pociskX, pociskY):
    dystans = math.sqrt((math.pow(przeciwnik_pozycja_x - pociskX, 2)) + math.pow(przeciwnik_pozycja_y - pociskY, 2))
    if dystans < 27:
        return True
    else:
        return False

## GRANICA

def czy_kontakt(gracz_pozycja_x, gracz_pozycja_y, przeciwnik_pozycja_x, przeciwnik_pozycja_y):
    dystans = math.sqrt((math.pow(gracz_pozycja_x - przeciwnik_pozycja_x, 2)) + math.pow(gracz_pozycja_y - przeciwnik_pozycja_y, 2))
    if dystans < 27:
        return True
    else:
        return False





                                    #######       GLOWNA PETLA        #######

"""poprzenosic kolizje itp do funkcji!!!!!!!!!"""

klatki = 0

dziala = True
while dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False

        ### sterowanie graczem
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gracz_pozycja_x_zmiana = - gracz_szybkosc
                gracz_ruch_strony = True
                gracz_ruch_goradol = False
            if event.key == pygame.K_RIGHT:
                gracz_pozycja_x_zmiana = gracz_szybkosc
                gracz_ruch_strony = True
                gracz_ruch_goradol = False
            if event.key == pygame.K_UP:
                gracz_pozycja_y_zmiana = - gracz_szybkosc
                gracz_ruch_strony = False
                gracz_ruch_goradol = True
            if event.key == pygame.K_DOWN:
                gracz_pozycja_y_zmiana = gracz_szybkosc
                gracz_ruch_strony = False
                gracz_ruch_goradol = True

        ### pociskowanie (jezykiem Mari Sikorskiej XD)
            if event.key == pygame.K_SPACE:
                if stan_pocisku == "gotowa":
                    pociskX = gracz_pozycja_x
                    wystrzal_pocisku(pociskX, pociskY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                gracz_pozycja_x_zmiana = 0
                gracz_ruch_goradol = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                gracz_pozycja_y_zmiana = 0
                gracz_ruch_strony = False
        if event.type == pygame.KEYUP:
            gracz_ruch_strony = False
            gracz_ruch_goradol = False
    gracz_pozycja_x += gracz_pozycja_x_zmiana
    gracz_pozycja_y += gracz_pozycja_y_zmiana
    ###

    ### Ruch przeciwnika
    if gracz_pozycja_x > przeciwnik_pozycja_x:
        przeciwnik_pozycja_x_zmiana = przeciwnik_szybkosc
    elif gracz_pozycja_x < przeciwnik_pozycja_x:
        przeciwnik_pozycja_x_zmiana = - przeciwnik_szybkosc
    if gracz_pozycja_y > przeciwnik_pozycja_y:
        przeciwnik_pozycja_y_zmiana = przeciwnik_szybkosc
    elif gracz_pozycja_y < przeciwnik_pozycja_y:
        przeciwnik_pozycja_y_zmiana = - przeciwnik_szybkosc
    przeciwnik_pozycja_x += przeciwnik_pozycja_x_zmiana
    przeciwnik_pozycja_y += przeciwnik_pozycja_y_zmiana
    ###

    ### Granica mapy
    if gracz_pozycja_x <= 0:
        gracz_pozycja_x = 0
    elif gracz_pozycja_x >= szerokosc - 64:  # - szerokośc/wysokość naszego gracza
        gracz_pozycja_x = szerokosc - 64
    if gracz_pozycja_y <= 0:
        gracz_pozycja_y = 0
    elif gracz_pozycja_y >= wysokosc - 64:
        gracz_pozycja_y = wysokosc - 64

    if przeciwnik_pozycja_x <= 0:
        przeciwnik_pozycja_x = 0
    elif przeciwnik_pozycja_x >= szerokosc - 64:  # - szerokośc/wysokość naszego gracza
        przeciwnik_pozycja_x = szerokosc - 64
    if przeciwnik_pozycja_y <= 0:
        przeciwnik_pozycja_y = 0
    elif przeciwnik_pozycja_y >= wysokosc - 64:
        przeciwnik_pozycja_y = wysokosc - 64
    ###

    ###ruch pocisku
    if pociskY <= 0:
        pociskY = 480
        stan_pocisku = "gotowa"

    if stan_pocisku == "wystrzał":
        wystrzal_pocisku(pociskX, pociskY)
        pociskY -= pociskY_zmiana

    ### kolizja
    kolizja = czy_kolizja(przeciwnik_pozycja_x, przeciwnik_pozycja_y, pociskX, pociskY)
    if kolizja:
        pociskY = 480
        stan_pocisku = "gotowa"
        score += 1
        przeciwnik_pozycja_x = random.randint(0, 800)
        przeciwnik_pozycja_y = random.randint(50, 150)

    ### kontakt
    kontakt = czy_kontakt(gracz_pozycja_x, gracz_pozycja_y, przeciwnik_pozycja_x, przeciwnik_pozycja_y)
    if kontakt:
        gracz_zdrowie -= 2
    ###
    ekran_zmiana()