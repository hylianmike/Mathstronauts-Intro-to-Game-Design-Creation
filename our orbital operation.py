# Intro to GameDev - main game file

import pgzrun
import random

WIDTH = 1000
HEIGHT = 600
box = 60
score = 0
speed = 5
sSpeed = 3
dSpeed = 4
Leed = -5
level = 0
lScreen = 0
jc = 0
limit = 5
limit2 = 10

blogo = "background_logo"
st = "start_button"
ins = "instructions_button"
img1 = "lv1"
img2 = "lv2"
img3 = "lv3"
img = "logo_img"
ship = "wanna7"
rock = "path913"
satty = "satellite_adv"
devb = "space_debris2"
lz = "laser_red"

def init():
    global player, junks, sat, debris, lasers
    player = Actor(ship)

    player.center = (WIDTH - 70, HEIGHT / 2)

    junks = []
    lasers = []


    for i in range(5):
        bad = Actor(rock)
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(box, HEIGHT - bad.height)
        bad.topright = (x_pos, y_pos)
        junks.append(bad)
        
    sat = Actor(satty)
    xs = random.randint(-500, -50)
    ys = random.randint(box, HEIGHT - sat.height)
    sat.topright = (xs, ys)

    debris = Actor(devb)
    xd = random.randint(-500, -50)
    yd = random.randint(box, HEIGHT - debris.height)
    debris.topright = (xd, yd)

    player.laserActive = 1

    music.play("spacelife")

start = Actor(st)
start.center = (WIDTH/2, 425)
instrucc = Actor(ins)
instrucc.center = (WIDTH/2, 500)

init()

def draw():
    screen.clear()
    screen.blit(img, (0,0))
    if level == 0:
        start.draw()
        instrucc.draw()
    if level == -1:
        start.draw()
        show = "1. Use UP and DOWN arrow keys to move your player \n2. Press the SPACE bar to shoot lazers \n3. Have a blast playing!!"
        screen.draw.text(show, midtop=(WIDTH/2, 170), fontsize=35, color="white")
    if level >= 1:
        player.draw()
        for bad in junks:
            bad.draw()
        sat.draw()
        debris.draw()
        for laser in lasers:
            laser.draw()
        screen.draw.text("Junks Collected : " + str(jc) + "                     Score: " + str(score), topleft=(440,16), fontsize=35, color="black")

    if score < 0:
        screen.draw.text("GAME OVER \nPress Enter to Play Again", center=(WIDTH/2, HEIGHT/2), fontsize = 60, color = "white")

    if level >= 1:
        screen.draw.text("LEVEL " + str(level), topright=(365, 15), fontsize=35, color="white")

    if lScreen == 1 or lScreen == 3 or lScreen == 5:
        screen.draw.text("LEVEL " + str(level) +"\nPress ENTER to continue...", center=(WIDTH/2,HEIGHT/2), fontsize = 70, color = "white")

def Pupdate():
    if keyboard.up == True:
        player.y -= 5

    elif keyboard.down == True:
        player.y += 5

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    if player.top < 60:
        player.top = 60

    if keyboard.space == 1 and level == 3:
        laser = Actor(lz)
        laser.midright = player.midleft
        fireLasers(laser)

def Jupdate():
    global score, jc, speed
    for bad in junks:
        if level == 2:
            speed = 7
        if level == 3:
            speed == 10
        bad.x += speed
        collision = player.colliderect(bad)
        if bad.left > WIDTH or collision == True:
            x_pos = -50
            y_pos = random.randint(box, HEIGHT - bad.height)
            bad.topleft = (x_pos, y_pos)
        if collision == True:
            sounds.collect_pep.play()
            score += 1
            jc += 1

def Supdate():
    global score, xs, ys
    sat.x += sSpeed
    col = player.colliderect(sat)
    if sat.left > WIDTH or col == 1:
        xs = random.randint(-500, -50)
        ys = random.randint(box, HEIGHT - sat.height)
        sat.topright = (xs, ys)
    if col == 1:
        score -= 5

def Dupdate():
    global score, xd, yd
    debris.x += dSpeed
    col = player.colliderect(debris)
    if debris.left > WIDTH or col == 1:
        xd = random.randint(-500, -50)
        yd = random.randint(box, HEIGHT - debris.height)
        debris.topright = (xd, yd)
    if col == 1:
        score -= 5

def update():
    global level, lScreen, img, jc, score
    if jc == limit:
        level = 2
    if jc == limit2:
        level = 3
    if level == -1:
        img = img1
        
    if score >= 0 and level >= 1:
        if lScreen == 1:
            img = img1
            if keyboard.RETURN == 1:
                lScreen = 2
        if lScreen == 2:
            Pupdate()
            Jupdate()
        if level == 2 and lScreen <= 3:
            lScreen = 3
            img = img2
            if keyboard.RETURN == 1:
                lScreen = 4
                music.play("space_mysterious")
        if lScreen == 4:
            Pupdate()
            Jupdate()
            Supdate()
        if level == 3 and lScreen <= 5:
            lScreen = 5
            img = img3
            if keyboard.RETURN == 1:
                lScreen = 6
                music.play("space_suspense")
        if lScreen == 6:
            Pupdate()
            Jupdate()
            Supdate()
            Dupdate()
            Lupdate()
    if score < 0 or level == -2:
        if keyboard.RETURN == 1:
            img = img1
            score = 0
            jc = 0
            level = 0
            init()
            music.stop()
            music.play("space_life")

player.laserActive = 1

def on_mouse_down(pos):
    global level, lScreen
    if start.collidepoint(pos):
        level = 1
        lScreen = 1
        #print("start button pressed!")
        
    if instrucc.collidepoint(pos):
        level = -1
        #print("instructions button pressed!")

def makeLaserActive():
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)
        sounds.laserfire02.play()
        lasers.append(laser)

def Lupdate():
    global score, xs, ys, xd, yd
    for laser in lasers:
        laser.x += Leed
        if laser.right < 0:
            lasers.remove(laser)
        if sat.colliderect(laser) == 1:
            lasers.remove(laser)
            xs = random.randint(-500, -50)
            ys = random.randint(box, HEIGHT - sat.height)
            sat.topright = (xs, ys)
            score -= 5
            sounds.explosion.play()
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            xd = random.randint(-500, -50)
            yd = random.randint(box, HEIGHT - debris.height)
            debris.topright = (xd, yd)
            score += 5
            sounds.explosion.play()


pgzrun.go()
