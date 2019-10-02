import pgzrun, math
import pygame
import text_utils
import levels

from random import randint
import enum
from high_scores import HighScores

# TODO: Fix the "base" rocks to use texture that matches background better.
# TODO: better pellet graphic and intersection.
# TODO: refactor to use objects for state instead of globals
# TODO: improve collision detection between timmy and rocks

class GameStatus(enum.Enum):
    start = 0
    playing = 1
    over = 2
    paused = 3


player = Actor("timmy", (400, 550))
boss = Actor("spider")
gameStatus = GameStatus.start
highScore = []
moveCounter = 0
moveSequence = 0
moveDelay = 0
score = 0
lasers = []
enemies = []
bases = []
level = 1

# These control the width in Pygame zero.
WIDTH = 800
HEIGHT = 600
PLAYER_MARGIN = 40

ENEMIES_PER_ROW = 6

ENEMY_MOVE_DELAY = 30

BOSS_MARGIN = 100
BOSS_KILL_Y = 500

HIGH_SCORES_PATH = "highscores.txt"

# These are actor status values.
ALIVE = 0
DEAD = 1
PLAYER_FINAL_STATUS = 30  # This is after death animation.

levels = [
    levels.Level(1, {}),
    levels.Level(1, {'spider': 10}),
    levels.Level(2, {'spider': 20}),
    levels.Level(3, {'spider': 30}),
]


def draw():
    # draw background
    screen.blit('cave', (0, 0))
    if gameStatus == GameStatus.start:
        ts = text_utils.TextScreen(
            screen=screen,
            top=100,
            centered=True,
            screen_width=WIDTH,
            rows=[
                "Timmy, Cave Dweller",
                "",
                "Type your name then",
                "   press Enter to start",
                "Arrow keys move. Space fires.",
                "",
                player.name
            ])
        ts.draw()
    if gameStatus == GameStatus.playing or gameStatus == GameStatus.paused:
        player.image = player.images[math.floor(player.status / 6)]
        player.draw()
        if boss.active:
            boss.draw()
        draw_lasers()
        draw_enemies()
        draw_bases()
        text_utils.draw_string(screen, str(score), topright=(WIDTH - 20, 10))
        text_utils.draw_string(screen, "LEVEL " + str(level), midtop=(WIDTH / 2, 10))
        draw_lives()
        if player.status >= PLAYER_FINAL_STATUS:
            if player.lives > 0:
                text_utils.draw_center_text(screen, "You were hit!\nPress Enter to re-spawn", screen_width=WIDTH)
            else:
                text_utils.draw_center_text(screen, "GAME OVER!\nPress Enter to continue", screen_width=WIDTH)
        if len(enemies) == 0:
            text_utils.draw_center_text(screen, "Level Complete!\nPress Enter to begin next level", screen_width=WIDTH)
        if gameStatus == GameStatus.paused:
            text_utils.draw_center_text(screen, "PAUSED", screen_width=WIDTH, top=HEIGHT / 3)
    if gameStatus == GameStatus.over:
        draw_high_score()


def update():
    global moveCounter, player, gameStatus, lasers, level, boss, highScore
    if gameStatus == GameStatus.start:
        if keyboard.RETURN and player.name != "":
            gameStatus = GameStatus.playing
    if gameStatus == GameStatus.playing:
        if player.status < PLAYER_FINAL_STATUS and len(enemies) > 0:
            check_keys()
            update_lasers()
            update_boss()
            check_bases()
            if moveCounter == 0:
                update_enemies()
            moveCounter += 1
            if moveCounter == moveDelay:
                moveCounter = 0
            if player.status > ALIVE:
                player.status += 1
                if player.status == PLAYER_FINAL_STATUS:
                    player.lives -= 1
        else:
            if keyboard.RETURN:
                if player.lives > 0:
                    player.status = ALIVE
                    lasers = []
                    if len(enemies) == 0:
                        level += 1
                        boss.active = False
                        init_enemies()
                        init_bases()
                else:
                    scores = HighScores()
                    scores.read_from_file(HIGH_SCORES_PATH)
                    scores.add_score(player.name, score)
                    scores.write_to_file(HIGH_SCORES_PATH)
                    highScore = scores.get_scores()
                    gameStatus = GameStatus.over

    if gameStatus == GameStatus.over:
        if keyboard.ESCAPE:
            init()
            gameStatus = GameStatus.start
    if gameStatus == GameStatus.paused:
        pass  # do nothing while paused.


def on_key_down(key):
    global player, gameStatus
    if gameStatus == GameStatus.start and key.name != "RETURN":
        if len(key.name) == 1:
            player.name += key.name
        else:
            if key.name == "BACKSPACE":
                player.name = player.name[:-1]
    else:
        if key == key.P:
            if gameStatus == GameStatus.playing:
                gameStatus = GameStatus.paused
            elif gameStatus == GameStatus.paused:
                gameStatus = GameStatus.playing

        if key == keys.F:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        elif key == keys.W:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_high_score():
    global highScore
    y = 0
    screen.draw.text("High Scores", midtop=(WIDTH / 2, 30), owidth=0.5, ocolor=(255, 255, 255), color=(0, 64, 255),
                     fontsize=60)
    for line in highScore:
        if y < 400:
            screen.draw.text(line, fontsize=50, midtop=(WIDTH / 2, 100 + y), ocolor=(0, 0, 255), color=(255, 255, 0))
            y += 50
    text_utils.draw_string(screen, "Press Escape to play again", center=(WIDTH / 2, 550))


def draw_lives():
    for l in range(player.lives):
        screen.blit("timmy_life", (10 + (l * 32), 10))


def draw_enemies():
    for a in range(len(enemies)):
        enemies[a].draw()


def draw_bases():
    for b in range(len(bases)):
        bases[b].draw_clipped()


def draw_lasers():
    for l in range(len(lasers)):
        lasers[l].draw()


def check_keys():
    global player, score
    if keyboard.left and player.x > PLAYER_MARGIN:
        player.x -= 5
    if keyboard.right and player.x < (WIDTH - PLAYER_MARGIN):
        player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            sounds.pellet.play()
            player.laserActive = 0
            clock.schedule(make_laser_active, 1.0)
            lasers.append(Actor("pellet", (player.x, player.y - 16)))  # was 32
            lasers[len(lasers) - 1].status = ALIVE
            lasers[len(lasers) - 1].type = 1
            score = max(score - 100, 0)


def make_laser_active():
    global player
    player.laserActive = 1


def check_bases():
    global bases
    for b in range(len(bases)):
        if bases[b].height == 0:
            bases[b].status = DEAD
    bases = list_cleanup(bases)


def update_lasers():
    global lasers, enemies
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            check_laser_hit(l)
            if lasers[l].y > 600:
                lasers[l].status = DEAD  # TODO: constant for height
        if lasers[l].type == 1:
            lasers[l].y -= 5
            check_player_laser_hit(l)
            if lasers[l].y < 10:
                lasers[l].status = DEAD
    lasers = list_cleanup(lasers)
    enemies = list_cleanup(enemies)


def list_cleanup(l):
    new_list = []
    for i in range(len(l)):
        if l[i].status == ALIVE:
            new_list.append(l[i])
    return new_list


def check_laser_hit(l):
    global player
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        sounds.death.play()
        player.status = DEAD
        lasers[l].status = DEAD
    for b in range(len(bases)):
        if collide_base_with_laser(bases[b], lasers[l]):
            bases[b].height = max(bases[b].height - 10, 0)
            lasers[l].status = DEAD


def check_player_laser_hit(l):
    global score, boss
    for b in range(len(bases)):
        if collide_base_with_laser(bases[b], lasers[l]):
            lasers[l].status = DEAD
    for a in range(len(enemies)):
        if enemies[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = DEAD
            enemies[a].status = DEAD
            score += 1000
    if boss.active:
        if boss.collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = DEAD
            boss.active = 0
            score += 5000


def update_enemies():
    global moveSequence, lasers, moveDelay
    move_x = move_y = 0
    if moveSequence < 10 or moveSequence > 30:
        move_x = -15
    if moveSequence == 10 or moveSequence == 30:
        move_y = 40 + (5 * level)
        moveDelay -= 1
    if 10 < moveSequence < 30:
        move_x = 15
    for a in range(len(enemies)):
        animate(enemies[a], pos=(enemies[a].x + move_x, enemies[a].y + move_y), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            enemies[a].image = "batframe1"
        else:
            enemies[a].image = "batframe2"
            if randint(0, 5) == 0:
                lasers.append(Actor("batrock", (enemies[a].x, enemies[a].y)))
                lasers[len(lasers) - 1].status = ALIVE
                lasers[len(lasers) - 1].type = ALIVE
                sounds.batdrop.play()
        if enemies[a].y > 500 and player.status == ALIVE:
            sounds.explosion.play()
            player.status = DEAD
            player.lives = 1  # TODO: waht? shouldn't this be -1
    moveSequence += 1
    if moveSequence == 40:
        moveSequence = 0


def update_boss():
    global boss, level, player, lasers
    if boss.active:
        boss.y += (0.3 * level)
        if boss.direction == 0:
            boss.x -= (1 * level)
        else:
            boss.x += (1 * level)
        if boss.x < BOSS_MARGIN:
            boss.direction = 1
        if boss.x > (WIDTH - BOSS_MARGIN):
            boss.direction = 0
        if boss.y > BOSS_KILL_Y:
            sounds.explosion.play()
            player.status = DEAD
            boss.active = False
        if randint(0, 30) == 0:
            lasers.append(Actor("batrock", (boss.x, boss.y)))
            lasers[len(lasers) - 1].status = ALIVE
            lasers[len(lasers) - 1].type = 0
    else:
        #if randint(0, WIDTH) == 0:
        lobj = levels[(level - 1) % len(levels)]
        if lobj.roll_for_mob('spider'):
            boss.active = True
            boss.x = WIDTH
            boss.y = 100
            boss.direction = 0


def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay, level, boss
    init_enemies()
    init_bases()
    moveCounter = moveSequence = score = player.laserCountdown = 0
    player.status = ALIVE
    lasers = []
    moveDelay = ENEMY_MOVE_DELAY
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


def init_enemies():
    global enemies, moveCounter, moveSequence, level
    enemies = []
    moveCounter = moveSequence = 0
    lobj = levels[(level-1) % len(levels)]
    n_enemies = ENEMIES_PER_ROW * lobj.rows
    for a in range(n_enemies):
        enemies.append(Actor("batframe1", (210 + (a % ENEMIES_PER_ROW) * 80, 100 + (int(a / ENEMIES_PER_ROW) * 64))))
        enemies[a].status = ALIVE


def draw_clipped(self):
    left = self.x - 32
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
            bases[bc].status = ALIVE
            bc += 1


init()
pgzrun.go()
