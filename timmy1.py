import pgzrun, math, re, time
from random import randint
import enum

# TODO: fix all the formatting and other warnings.
# TODO: clean this all up to have fewer magic numbers and globals
# TODO: setup a remote server Git repo

# TODO: need cavern themed background image.
# TODO: replace or remove boss code.
# TODO: fix the wonky base positioning bug.


class GameStatus(enum.Enum):
    start = 0
    playing = 1
    over = 2


player = Actor("timmy", (400, 550))
boss = Actor("spider")
gameStatus = GameStatus.start
highScore = []
moveCounter = 0
score = 0
lasers = []
level = 1

# These control the width in Pygame zero.
WIDTH = 800
HEIGHT = 600
PLAYER_MARGIN = 40


def draw():
    screen.blit('background', (0, 0))
    if gameStatus == GameStatus.start:
        draw_centre_text(
            "Timmy, Cave Dweller\n\n\nType your name then\nPress Enter to start\nArrow keys move. Space fires.")
        screen.draw.text(player.name, center=(400, 500), owidth=0.5, ocolor=(255, 0, 0), color=(0, 64, 255),
                         fontsize=60)
    if gameStatus == GameStatus.playing:
        player.image = player.images[math.floor(player.status / 6)]
        player.draw()
        if boss.active:
            boss.draw()
        draw_lasers()
        draw_aliens()
        draw_bases()
        draw_string(str(score), topright=(WIDTH-20, 10))
        draw_string("LEVEL " + str(level), midtop=(WIDTH/2, 10))
        draw_lives()
        if player.status >= 30:
            if player.lives > 0:
                draw_centre_text("You were hit!\nPress Enter to re-spawn")
            else:
                draw_centre_text("GAME OVER!\nPress Enter to continue")
        if len(aliens) == 0:
            draw_centre_text("Level Complete!\nPress Enter to go to the next level")
    if gameStatus == GameStatus.over:
        draw_high_score()


def draw_string(s, **kwargs):
    screen.draw.text(s, owidth=0.5, ocolor=(255, 255, 255), color=(0, 64, 255),
                     fontsize=60, **kwargs)


def draw_centre_text(t):
    draw_string(t, center=(WIDTH/2, 300))


def update():
    global moveCounter, player, gameStatus, lasers, level, boss
    if gameStatus == GameStatus.start:
        if keyboard.RETURN and player.name != "": gameStatus = GameStatus.playing
    if gameStatus == GameStatus.playing:
        if player.status < 30 and len(aliens) > 0:
            check_keys()
            update_lasers()
            update_boss()
            if moveCounter == 0: update_aliens()
            moveCounter += 1
            if moveCounter == moveDelay: moveCounter = 0
            if player.status > 0:
                player.status += 1
                if player.status == 30:
                    player.lives -= 1
        else:
            if keyboard.RETURN:
                if player.lives > 0:
                    player.status = 0
                    lasers = []
                    if len(aliens) == 0:
                        level += 1
                        boss.active = False
                        init_aliens()
                        init_bases()
                else:
                    read_high_score()
                    gameStatus = GameStatus.over
                    write_high_score()
    if gameStatus == GameStatus.over:
        if keyboard.ESCAPE:
            init()
            gameStatus = GameStatus.start


def on_key_down(key):
    global player
    if gameStatus == GameStatus.start and key.name != "RETURN":
        if len(key.name) == 1:
            player.name += key.name
        else:
            if key.name == "BACKSPACE":
                player.name = player.name[:-1]


def read_high_score():
    global highScore, score, player
    highScore = []
    try:
        hsFile = open("highscores.txt", "r")
        for line in hsFile:
            highScore.append(line.rstrip())
    except:
        print("Unable to read high scores file!")
        pass
    finally:
        hsFile.close()

    highScore.append(str(score) + " " + player.name)
    highScore.sort(key=natural_key, reverse=True)


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def write_high_score():
    global highScore
    hsFile = open("highscores.txt", "w")
    for line in highScore:
        hsFile.write(line + "\n")
    hsFile.close()


def draw_high_score():
    global highScore
    y = 0
    screen.draw.text("High Scores", midtop=(WIDTH/2, 30), owidth=0.5, ocolor=(255, 255, 255), color=(0, 64, 255),
                     fontsize=60)
    for line in highScore:
        if y < 400:
            screen.draw.text(line, fontsize=50, midtop=(WIDTH/2, 100 + y), ocolor=(0, 0, 255), color=(255, 255, 0))
            y += 50
    draw_string("Press Escape to play again", center=(WIDTH/2, 550))


def draw_lives():
    for l in range(player.lives):
        screen.blit("timmy_life", (10 + (l * 32), 10))


def draw_aliens():
    for a in range(len(aliens)):
        aliens[a].draw()


def draw_bases():
    for b in range(len(bases)):
        bases[b].draw_clipped()


def draw_lasers():
    for l in range(len(lasers)):
        lasers[l].draw()


def check_keys():
    global player, score
    if keyboard.left:
        if player.x > PLAYER_MARGIN: player.x -= 5
    if keyboard.right:
        if player.x < (WIDTH - PLAYER_MARGIN): player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            sounds.pellet.play()
            player.laserActive = 0
            clock.schedule(make_laser_active, 1.0)
            lasers.append(Actor("pellet", (player.x, player.y - 16))) # was 32
            lasers[len(lasers) - 1].status = 0
            lasers[len(lasers) - 1].type = 1
            score = max(score - 100, 0)


def make_laser_active():
    global player
    player.laserActive = 1


def check_bases():
    for b in range(len(bases)):
        # original: if l < len(bases):
        if b < len(bases):
            if bases[b].height < 5:
                del bases[b]


def update_lasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            check_laser_hit(l)
            if lasers[l].y > 600: lasers[l].status = 1  # TODO: constant for height
        if lasers[l].type == 1:
            lasers[l].y -= 5
            check_player_laser_hit(l)
            if lasers[l].y < 10: lasers[l].status = 1
    lasers = list_cleanup(lasers)
    aliens = list_cleanup(aliens)


def list_cleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0: newList.append(l[i])
    return newList


def check_laser_hit(l):
    global player
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        sounds.death.play()
        player.status = 1
        lasers[l].status = 1
    # Why are we checking this here and in check_player_laser_hit?
    for b in range(len(bases)):
        if collide_base_with_laser(bases[b], lasers[l]):
            bases[b].height = max(bases[b].height - 10, 0)
            lasers[l].status = 1


def check_player_laser_hit(l):
    global score, boss
    for b in range(len(bases)):
        if collide_base_with_laser(bases[b], lasers[l]):
            lasers[l].status = 1
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            aliens[a].status = 1
            score += 1000
    if boss.active:
        if boss.collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            boss.active = 0
            score += 5000


def update_aliens():
    global moveSequence, lasers, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30: movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 40 + (5 * level)
        moveDelay -= 1
    if moveSequence > 10 and moveSequence < 30:
        movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "batframe1"
        else:
            aliens[a].image = "batframe2"
            if randint(0, 5) == 0:
                lasers.append(Actor("batrock", (aliens[a].x, aliens[a].y)))
                lasers[len(lasers) - 1].status = 0
                lasers[len(lasers) - 1].type = 0
                sounds.batdrop.play()
        if aliens[a].y > 500 and player.status == 0:
            sounds.explosion.play()
            player.status = 1
            player.lives = 1
    moveSequence += 1
    if moveSequence == 40: moveSequence = 0


def update_boss():
    global boss, level, player, lasers
    if boss.active:
        boss.y += (0.3 * level)
        if boss.direction == 0:
            boss.x -= (1 * level)
        else:
            boss.x += (1 * level)
        # TODO: need constants
        if boss.x < 100: boss.direction = 1
        if boss.x > 700: boss.direction = 0
        if boss.y > 500:
            sounds.explosion.play()
            player.status = 1
            boss.active = False
        if randint(0, 30) == 0:
            lasers.append(Actor("batrock", (boss.x, boss.y)))
            lasers[len(lasers) - 1].status = 0
            lasers[len(lasers) - 1].type = 0
    else:
        if randint(0, WIDTH) == 0:
            boss.active = True
            boss.x = WIDTH
            boss.y = 100
            boss.direction = 0


def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay, level, boss
    init_aliens()
    init_bases()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    boss.active = False
    player.images = ["timmy", "death1", "death2", "death3", "death4", "death5"]
    player.laserActive = 1
    player.lives = 3
    player.name = ""
    level = 1

    # For testing tone generation.
    # pellet_tone = tone.create(2000, 0.5)
    # pellet_tone.play()


    music.play("mystical_caverns")

def init_aliens():
    global aliens, moveCounter, moveSequence
    aliens = []
    moveCounter = moveSequence = 0
    for a in range(18):
        # TODO: OMG Constants!
        aliens.append(Actor("batframe1", (210 + (a % 6) * 80, 100 + (int(a / 6) * 64))))
        aliens[a].status = 0


def draw_clipped(self):
    left = self.x -32
    top = self.y - self.height
    r = (0, 0, self.width, self.height)
    screen.surface.blit(self._surf, (left, top), r)


def collide_base_with_laser(base, other):
    return base.colliderect(other)


def init_bases():
    global bases
    bases = []
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("baserock", midbottom=(150 + (b * 200) + (p * 40), 520)))
            bases[bc].draw_clipped = draw_clipped.__get__(bases[bc])
            bases[bc].height = 44
            bases[bc].original_height = bases[bc].height
            bc += 1


init()
pgzrun.go()
