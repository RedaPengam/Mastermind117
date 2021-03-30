import os, time, sys
import random as rd
import pygame as pg
from moviepy.editor import VideoFileClip
from pathlib import Path

##### path #####

L = str(__file__)
print(L[0:-13])
os.chdir(L[0:-13])

##### game window #####

# Initialize the program & clock
pg.init()
clock = pg.time.Clock()
# title and icon
pg.display.set_caption('Oss Mastermind')
pg.display.set_icon(pg.image.load('data/dujardin32.jpg')) # 32*32 icon
# create the screen : top left O(0,0); (width=x_axis, height=y_axis)
#screen = pg.display.set_mode((1600, 900), pg.RESIZABLE)
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.toggle_fullscreen()
background = pg.image.load('data/play.png').convert()

class Boule:
    def num(i):
        if i == '*':
            return pg.image.load('data/0.png').convert_alpha()
        else:
            return pg.image.load('data/{}.png'.format(i)).convert_alpha()

#### constants ####

# balls position
xinit = 40
yinit = 720
xinitt = xinit+320
yinitt = yinit+35

txt_instru = "Frappe entrer pour valider ton supra code à 4 chiffres (entre 1 et 8)"
txt_win = "Vous êtes doué, quel agent !"
txt_lose = "Même pas trouvé ! C'est la piquette Jack !"

font = pg.font.SysFont("calibri.ttf", 32)
input_box = pg.Rect(820, 615, 200, 30)

# Filing rectangle color
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive

Listessais = []
Listpos = []
code = ''

click = False

#### game fonctions ####

def codesecret():
    codesecret = ''
    for i in range(4):
        codesecret += str(rd.randint(1,8))
    return codesecret

def evalue(essai="uorp", codesecret="prou"):
    pos_ok, pos_nok = 0, 0
    # cherche nb positions ok
    for i in range(len(essai)):
        if essai[i] == codesecret[i]:
            essai = essai[:i] + '*' + essai[i+1:]
            codesecret = codesecret[:i] +'*' + codesecret[i+1:]
            pos_ok += 1
    # cherche nb positions non-ok
    for i in range(len(essai)):
        for j in range (len(essai)):
            if essai[i] == codesecret[j] and codesecret[j] != '*' and essai[i] != '*':
                essai = essai[:i] + '*' + essai[i+1:]
                codesecret = codesecret[:j] +'*' + codesecret[j+1:]
                pos_nok += 1
                # print(essai, codesecret)
    return (pos_ok, pos_nok)

def set_boules(i):
    for j in range (i):
        screen.blit(Boule.num(Listessais[j][0]), (xinit, yinit-67*j))
        screen.blit(Boule.num(Listessais[j][1]), (xinit+80, yinit-67*j))
        screen.blit(Boule.num(Listessais[j][2]), (xinit+160, yinit-67*j))
        screen.blit(Boule.num(Listessais[j][3]), (xinit+240, yinit-67*j))

def set_pos(i):
    for j in range (i):
        nb_posok = Listpos[j][0]
        nb_posnok = Listpos[j][1]
        for n in range (nb_posok):
            screen.blit(Boule.num(0), (xinitt+40*n, yinitt-30-67*j))
        for m in range (nb_posnok):
            screen.blit(Boule.num(9), (xinitt+40*m, yinitt-67*j))

def display_text(txt_instru, xtxt=400, ytxt=800):
    return screen.blit(font.render(txt_instru, True, (255, 255, 80)), (xtxt, ytxt))

def display_text2(txt_instru, xtxt=400, ytxt=800):
    return screen.blit(font.render(txt_instru, True, (0, 0, 0)), (xtxt, ytxt))

def play_sound(sound):
    return pg.mixer.Sound(sound).play()

def play_video(video):
    clip = VideoFileClip(video)
    clip.preview(fps=25)

#### game itself ####

def menu():
    play_video('data/mission.ts')

    # sound stuff
    pg.mixer.music.load('data/bambino_full.wav')
    pg.mixer.music.play(-1)

    while True:
        screen.blit(background, (0, 0))
        display_text('Menu', 20, 20)
        mx, my = pg.mouse.get_pos()
        button = pg.Rect(520, 580, 200, 50)

        # if the user clicked on the play button, start a new game
        if button.collidepoint((mx, my)):
            if click:
                pg.mixer_music.stop()
                game()

        pg.draw.rect(screen, (0, 0, 0), button)
        display_text('Jouer', 590, 594)
        click = False

        for event in pg.event.get():
            # if the user clicked on the cross button, exit game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                # if the user clicked on 'Space', play mission video
                if event.key == pg.K_SPACE:
                    play_video('data/mission.ts')
                # if the user clicked on 'Enter', start a new game
                if event.key == pg.K_RETURN:
                    pg.mixer_music.stop()
                    game()
                # if the user clicked on 'Echap', leave the game
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pg.display.update()
        clock.tick(60)

def game():
    play_video('data/desk1.mkv')

    # initialisation
    global color
    global Listessais
    global Listpos
    global code
    i = 0
    text = ''
    active = False
    running = True

    # test python
    code = codesecret()
    print('\n++++++++++++++++++++++++++++++++++++++++++++++++++\ncodesecret : {}\n++++++++++++++++++++++++++++++++++++++++++++++++++'.format(code))

    # sound stuff
    pg.mixer.music.load('data/desk.wav')
    pg.mixer.music.play(-1)

    while running:
        screen.blit(background, (0, 0))
        color = color_active if active else color_inactive

        for event in pg.event.get():
            # if the user clicked on the cross button, exit game
            if event.type == pg.QUIT:
                pg.mixer_music.stop()
                running = False

            # if the user clicked on the box, input available
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos): active = not active
                else: active = False

            if event.type == pg.KEYDOWN:
                # if the user clicked on 'Space', play mission video
                if event.key == pg.K_ESCAPE:
                    pg.mixer_music.stop()
                    menu()

                # if the user clicked on 'Enter' while input_box rect. is active
                if active:
                    if event.key == pg.K_RETURN:
                        play_sound('data/toum.wav')
                        i += 1

                        # test python
                        print('\nessai n°', i)
                        print('entré : ', text)

                        # noob alert initialization
                        play = False

                        # noob alert: if the text entered is less than 4 digits
                        if len(text) < 4 and play == False:
                            play_sound('data/tusaispasjouer.wav')
                            play = True
                            for m in range (4-len(text)):
                                text = text + 'a'
                            # tests if parts of the text entered is not a digit between 1 and 8
                            L=[]
                            for m in text:
                                L.append(m)
                            for m in range(len(L)):
                                if L[m]!='1' and L[m]!='2' and L[m]!='3' and L[m]!='4' and L[m]!='5' and L[m]!='6' and L[m]!='7' and L[m]!='8':
                                    text = text[:m] + 'a' + text[m+1:]

                        # noob alert: if the text entered is greater than 4 digits
                        elif len(text) > 4 and play == False:
                            play_sound('data/tusaispasjouer.wav')
                            play = True
                            text = text[:4]
                            # tests if parts of the text entered is not a digit between 1 and 8
                            L=[]
                            for m in text:
                                L.append(m)
                            for m in range(len(L)):
                                if L[m]!='1' and L[m]!='2' and L[m]!='3' and L[m]!='4' and L[m]!='5' and L[m]!='6' and L[m]!='7' and L[m]!='8':
                                    text = text[:m] + 'a' + text[m+1:]

                        # tests if parts of the text entered is not a digit between 1 and 8
                        L=[]
                        for m in text:
                            L.append(m)
                        for m in range(len(L)):
                            if L[m]!='1' and L[m]!='2' and L[m]!='3' and L[m]!='4' and L[m]!='5' and L[m]!='6' and L[m]!='7' and L[m]!='8':
                                text = text[:m] + 'a' + text[m+1:]

                        # update user test lists and user position list
                        Listessais.append(text)
                        Listpos.append(evalue(text, code))

                        # test python
                        print("Listpos :", Listpos)
                        print("text :", text)

                        # noob alert: if the text entered has nothing in common with the code
                        if evalue(text, code) == (0, 0) and i != 10 and play == False: play_sound('data/tusaispasjouer.wav')

                        # end game conditions
                        if i > 0 and Listpos[-1] == (4, 0):
                            pg.mixer_music.stop()
                            win()
                            running = False
                        if i == 10 and Listpos[-1] != (4, 0):
                            pg.mixer_music.stop()
                            lost()
                            running = False

                        text = ''

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]

                    else: text += event.unicode

        # displayed each frame
        screen.blit(pg.image.load('data/background{}.png'.format(i)).convert(), (0, 0))
        display_text(txt_instru, 600, 700)
        display_text('Game', 20, 20)
        display_text('Essai(s) restant : {}'.format(10-i), 600, 620)
        set_boules(i)
        set_pos(i)

        # resize the box if the text is too long
        width = max(200, font.render(text, True, color).get_width()+10)
        input_box.w = width
        screen.blit(font.render(text, True, color), (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)

        # refresh screen at 60fps
        pg.display.flip()
        clock.tick(60)

def win():
    play_video('data/scep.mkv')
    screen.blit(background, (0, 0))
    global Listessais
    global Listpos
    Listessais = []
    Listpos = []

    while True:
        screen.blit(pg.image.load('data/scep.png').convert(), (0, 0))
        display_text(txt_win, 500, 500)
        display_text('Appuie sur entrer pour recommencer ou echap pour quitter...', 20, 20)

        for event in pg.event.get():
            # if the user clicked on the cross button, exit game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                # if the user clicked on 'Echap', play ending video
                if event.key == pg.K_ESCAPE:
                    pg.mixer_music.stop()
                    play_video('data/aurevoir.mkv')
                    pg.quit()
                    sys.exit()
                # if the user clicked on 'Enter', start a new game and reset lists
                if event.key == pg.K_RETURN:
                    pg.mixer_music.stop()
                    Listessais = []
                    Listpos = []
                    game()

        pg.display.update()
        clock.tick(60)

def lost():
    play_video('data/jack1.mkv')
    running = True
    screen.blit(background, (0, 0))
    global Listessais
    global Listpos
    global code

    while running:
        screen.blit(pg.image.load('data/lost.png').convert(), (0, 0))
        display_text2(txt_lose, 800, 400)
        display_text('Appuie sur entrer pour recommencer ou echap pour quitter...', 20, 20)
        screen.blit(Boule.num(code[0]), (900, 460))
        screen.blit(Boule.num(code[1]), (900+80, 460))
        screen.blit(Boule.num(code[2]), (900+160, 460))
        screen.blit(Boule.num(code[3]), (900+240, 460))
        set_boules(10)

        for event in pg.event.get():
            # if the user clicked on the cross button, exit game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                # if the user clicked on 'Echap', play ending video
                if event.key == pg.K_ESCAPE:
                    pg.mixer_music.stop()
                    play_video('data/aurevoir.mkv')
                    pg.quit()
                    sys.exit()
                # if the user clicked on 'Enter', start a new game and reset lists
                if event.key == pg.K_RETURN:
                    pg.mixer_music.stop()
                    Listessais = []
                    Listpos = []
                    game()

        pg.display.update()
        clock.tick(60)

menu()
pg.quit()