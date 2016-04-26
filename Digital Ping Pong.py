# -----------------------------------------------------------------------------
# _____________________________________________________________________________
# =============================================================================
# Digital Ping Pong
# v1.66
# By Tristen Unrau 2013
# An event-driven program in Python created for CodeSkulptor.
# To play the game, paste this code into codeskulptor.org and press play.
# =============================================================================
# _____________________________________________________________________________
# -----------------------------------------------------------------------------


#
# READ-ME
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

"""
Some info about this game:

1:
The paddles change size when you reach these points: 5, 10, 25, 50, and 100.
    Single-Player: The higher you score, the bigger the A.I. paddle gets.
    Multi-Player: The higher you score, the smaller your own paddle gets.

2:
The ball's velocity will be adjusted in the direction that your paddle is
moving, so if you end up with a ball bouncing in a straight line back and
forth, just move your paddle as the ball hits it :)

3:
The reason I included ',' and 'o' as Player 1 controls in addition to 'w' and
's' is because I use an alternate keyboard layout called DVORAK. In DVORAK,
the ',' and 'o' keys are where 'w' and 's' are in the standard QWERTY layout.

I hope you enjoy Digital Ping Pong! Feel free to contribute :)
"""


#
# TO-DO LIST
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

# 1) Different colour for A.I. Paddle
# 2) 3rd mode where P2 is a giant wall and P1 gets a point every time the ball
#    hits their own paddle.
# 3) Achievement graphics for the 5, 10, 25, 50 and 100 point milestones
# 4) Score-Streaks
# 5) High-Scores
# 6) Sound for ball hitting top/bottom walls?
#    (different from ball hitting the paddle)
# 7) Rally counter for Multi-player (+1 every time the ball hits a paddle)


#
# IMPORT MODULES
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

import simplegui
import random


#
# DECLARE GLOBAL VARIABLES
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

# control
game_in_progress = False
ai_is_on = False
is_down = {}
is_down['p1'] = False
is_down['p2'] = False
is_up = {}
is_up['p1'] = False
is_up['p2'] = False

# canvas settings
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
CONTROL_WIDTH = 300

# text settings
ball_colour = '#ffffff'
paddle_default_colour = '#ffffff'
paddle_grow_colour = '#b86969'
paddle_shrink_colour = '#b86969'
changed_this_score = False
paddle_colour = {}
paddle_colour['p1'] = paddle_default_colour
paddle_colour['p2'] = paddle_default_colour
label_size = 30
label_colour = "#5f5f5f"
label_font = "monospace"
p1_label = "PLAYER 1"
p1_label_x = 0
p2_label = "PLAYER 2"
p2_label_x = (FRAME_WIDTH / 2) + 40
LABEL_Y = FRAME_HEIGHT - 30
score_size = 40
score_colour = '#5f5f5f'
score_font = 'monospace'
top_bottom_space = 0

# score settings
score = {}
score['p1'] = 0
score['p2'] = 0
old_score = {}
old_score['p1'] = 0
old_score['p2'] = 0
score_string = {}
score_string['p1'] = str(score['p1'])
score_string['p2'] = str(score['p2'])
score_x = {}
score_x['p1'] = 0
score_x['p2'] = 0
SCORE_Y = 50
last_scored = 'none'

# ball dynamics
BALL_RADIUS = 4
CENTRE_BALL = {}
CENTRE_BALL['x'] = FRAME_WIDTH / 2
CENTRE_BALL['y'] = FRAME_HEIGHT / 2
ball_pos = {}
ball_pos['x'] = CENTRE_BALL['x']
ball_pos['y'] = CENTRE_BALL['y']
ball_vel = {}
ball_vel['x'] = 0
ball_vel['y'] = 0


# paddle dynamics
paddle_height_default = 80
paddle_height = {}
paddle_height['p1'] = paddle_height_default
paddle_height['p2'] = paddle_height_default
PADDLE_WIDTH = {}
PADDLE_WIDTH['p1'] = 11
PADDLE_WIDTH['p2'] = 12
PADDLE_X = {}
PADDLE_X['p1'] = 0
PADDLE_X['p2'] = FRAME_WIDTH - PADDLE_WIDTH['p2']
paddle_y = {}
paddle_y['p1'] = (FRAME_HEIGHT / 2) - (paddle_height['p1'] / 2)
paddle_y['p2'] = (FRAME_HEIGHT / 2) - (paddle_height['p2'] / 2)
paddle_vel = {}
paddle_vel['p1'] = 0
paddle_vel['p2'] = 0
paddle_pos = {}
paddle_pos['p1'] = [
                   [PADDLE_X['p1'], paddle_y['p1']], 
                   [(PADDLE_X['p1'] + PADDLE_WIDTH['p1']), paddle_y['p1']], 
                   [(PADDLE_X['p1'] + PADDLE_WIDTH['p1']), (paddle_y['p1'] + paddle_height['p1'])], 
                   [PADDLE_X['p1'], (paddle_y['p1'] + paddle_height['p1'])]
                   ]
paddle_pos['p2'] = [
                   [PADDLE_X['p2'], paddle_y['p2']], 
                   [(PADDLE_X['p2'] + PADDLE_WIDTH['p2']), paddle_y['p2']], 
                   [(PADDLE_X['p2'] + PADDLE_WIDTH['p2']), (paddle_y['p2'] + paddle_height['p2'])], 
                   [PADDLE_X['p2'], (paddle_y['p2'] + paddle_height['p2'])]
                   ]

# gutter settings
GUTTER_X = {}
GUTTER_X['p1'] = PADDLE_WIDTH['p1']
GUTTER_X['p2'] = FRAME_WIDTH - PADDLE_WIDTH['p2']

# effects settings
blink_interval = 500
global_tick = 0
message_delay = 2
music_interval = 8352
played_score_sound = False
music_is_on = True


#
# DEFINE HELPER FUNCTIONS
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

def spawn_ball():
    """ Reset ball position and velocity after a player scores """
    global ball_pos, ball_vel, blink_effect, global_tick

    # reset the ball position and velocity
    ball_vel['x'], ball_vel['y'] = 0, 0
    ball_pos['x'] = CENTRE_BALL['x']
    ball_pos['y'] = CENTRE_BALL['y']

    # start the timer and launch the ball
    event_timer.start()

def launch_ball():
    """ Apply random velocity on the ball toward the last player who scored """
    global last_scored

    # if it's a new game, choose left or right at random
    if last_scored == 'none':
        if random.randrange(0, 2):
            last_scored = 'p1'
        else:
            last_scored = 'p2'

    # assign random upward velocity
    rand_x = random.randrange(2, 5)
    rand_y = random.randrange(1, 3)

    # launch ball left
    if last_scored == 'p1':
        ball_vel['x'] = -rand_x
        ball_vel['y'] = -rand_y
    # launch ball right
    elif last_scored == 'p2':
        ball_vel['x'] = rand_x
        ball_vel['y'] = -rand_y

    play_sound('launch')

def update_ball():
    """
    Move the ball and update its velocity at certain collision conditions;
    if the ball hits a gutter, update the score.
    """
    global last_scored

    # if the ball hits the top or bottom wall
    if (ball_pos['y'] - BALL_RADIUS) <= 0 or (ball_pos['y'] + BALL_RADIUS) >= FRAME_HEIGHT:
        # vertical velocity is inverted
        ball_vel['y'] = -ball_vel['y']
        play_sound('bounce')

    # if the ball hits a paddle
    elif (((ball_pos['x'] - BALL_RADIUS) <= GUTTER_X['p1'] and ball_pos['y'] in range(paddle_y['p1'], (paddle_y['p1'] + paddle_height['p1']))) or 
          ((ball_pos['x'] + BALL_RADIUS) >= GUTTER_X['p2'] and ball_pos['y'] in range(paddle_y['p2'], (paddle_y['p2'] + paddle_height['p2'])))):

        # if a paddle is moving in a direction, adjust the vertical velocity of the ball in that direction
        if ((ball_vel['y'] == 0 and (paddle_vel['p1'] > 0 or paddle_vel['p2'] > 0)) or
            (ball_vel['y'] < 0 and (paddle_vel['p1'] > 0 or paddle_vel['p2'] > 0)) or
            (ball_vel['y'] > 0 and (paddle_vel['p1'] > 0 or paddle_vel['p2'] > 0))):
            ball_vel['y'] += 1
        elif ((ball_vel['y'] == 0 and (paddle_vel['p1'] < 0 or paddle_vel['p2'] < 0)) or
              (ball_vel['y'] < 0 and (paddle_vel['p1'] < 0 or paddle_vel['p2'] < 0)) or
              (ball_vel['y'] > 0 and (paddle_vel['p1'] < 0 or paddle_vel['p2'] < 0))):
            ball_vel['y'] -= 1

        # horizontal velocity is inverted and increased by 10%
        ball_vel['x'] = -ball_vel['x'] * 1.1
        play_sound('bounce')

    # if the ball hits the left gutter
    elif (ball_pos['x'] - BALL_RADIUS) <= GUTTER_X['p1']:
        play_sound('gutter')
        score['p2'] += 1
        update_score_pos()
        last_scored = 'p2'
        spawn_ball()

    # if the ball hits the right gutter
    elif (ball_pos['x'] + BALL_RADIUS) >= GUTTER_X['p2']:
        play_sound('gutter')
        score['p1'] += 1
        update_score_pos()
        last_scored = 'p1'
        spawn_ball()

def update_paddle(pad):
    """ Move a paddle and keep it within the frame """
    global paddle_y, paddle_vel
    # if the paddle has reached the top
    if paddle_y[pad] <= 0 and paddle_vel[pad] < 0:
        paddle_y[pad] = 0
        paddle_vel[pad] = 0
    # if the paddle has reached the bottom
    elif paddle_y[pad] >= (FRAME_HEIGHT - paddle_height[pad]) and paddle_vel[pad] > 0:
        paddle_y[pad] = (FRAME_HEIGHT - paddle_height[pad])
        paddle_vel[pad] = 0
    # if neither, move the paddle according to its velocity
    else:
        paddle_y[pad] += paddle_vel[pad]
    # retun new polygon point coordinates for the paddle
    return [
            [PADDLE_X[pad], paddle_y[pad]], 
            [(PADDLE_X[pad] + PADDLE_WIDTH[pad]), paddle_y[pad]], 
            [(PADDLE_X[pad] + PADDLE_WIDTH[pad]), (paddle_y[pad] + paddle_height[pad])], 
            [PADDLE_X[pad], (paddle_y[pad] + paddle_height[pad])]
            ]

def recentre_paddle(pad):
    """ Used in update_difficulty() when A.I. paddle size increases """
    paddle_y[pad] = (FRAME_HEIGHT / 2) - (paddle_height[pad] / 2)


def update_difficulty(player):
    """ Adjust the size of the paddles based on the players' scores """

    # if playing single-player, make the A.I. paddle bigger at certain user scores
    if ai_is_on:
        if score['p1'] < 5:
            paddle_height['p2'] = 80
        elif score['p1'] < 10:
            paddle_height['p2'] = 120
        elif score['p1'] < 25:
            paddle_height['p2'] = 160
        elif score['p1'] < 50:
            paddle_height['p2'] = 200
        elif score['p1'] < 100:
            paddle_height['p2'] = 250
        elif score['p1'] >= 100:
            paddle_height['p2'] = 300
        if score['p1'] in (5, 10, 25, 50, 100) and score['p1'] > old_score['p1']:
            # when paddle size is increased, re-centre the paddle vertically in the frame
            recentre_paddle('p2')
            paddle_colour['p2'] = paddle_grow_colour
            play_sound('grow')

    # if playing multi-player, make a paddle smaller at certain scores
    else:
        if score[player] < 5:
            reduction = paddle_height[player] - 80
            paddle_height[player] = 80
        elif score[player] < 10:
            reduction = paddle_height[player] - 65
            paddle_height[player] = 65
        elif score[player] < 25:
            reduction = paddle_height[player] - 50
            paddle_height[player] = 50
        elif score[player] < 50:
            reduction = paddle_height[player] - 35
            paddle_height[player] = 35
        elif score[player] < 100:
            reduction = paddle_height[player] - 10
            paddle_height[player] = 10
        elif score[player] >= 100:
            reduction = paddle_height[player] - 4
            paddle_height[player] = 4
        if score[player] in (5, 10, 25, 50, 100) and score[player] > old_score[player]:
            # when paddle size is reduced, centre the new paddle inside the old paddle position
            paddle_y[player] += (reduction / 2)
            paddle_colour[player] = paddle_shrink_colour
            play_sound('shrink')


def update_score_pos():
    """ Update the position of the player scores so that they are always centred """
    global top_bottom_space
    score_string['p1'], score_string['p2'] = str(score['p1']), str(score['p2'])
    score_x['p1'] = (FRAME_WIDTH / 2) - frame.get_canvas_textwidth(score_string['p1'], score_size, score_font) - 40
    score_x['p2'] = (FRAME_WIDTH / 2) + 40

def update_label_pos():
    """ Update the Player 1 text-label position """
    global p1_label_x
    p1_label_x = (FRAME_WIDTH / 2) - frame.get_canvas_textwidth(p1_label, label_size, label_font) - 40

def play_sound(sound):
    if sound == 'launch':
        sound_launch.rewind()
        sound_launch.play()
    elif sound == 'bounce':
        sound_bounce.rewind()
        sound_bounce.play()
    elif sound == 'gutter':
        sound_gutter.rewind()
        sound_gutter.play()
    elif sound == 'score':
        sound_score.rewind()
        sound_score.play()
    elif sound == 'fail':
        sound_fail.rewind()
        sound_fail.play()
    elif sound == 'countdown':
        sound_countdown.rewind()
        sound_countdown.play()
    elif sound == 'newgame':
        sound_newgame.rewind()
        sound_newgame.play()
    elif sound == 'shrink':
        sound_shrink.rewind()
        sound_shrink.play()
    elif sound == 'grow':
        sound_grow.rewind()
        sound_grow.play()


#
# DEFINE EVENT HANDLERS
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

def new_game():
    """ End the current game and reset the board """
    global last_scored, effect_message, game_in_progress, global_tick, played_score_sound

    play_sound('newgame')
    game_in_progress = False

    # reset the score
    score['p1'], score['p2'] = 0, 0
    update_score_pos()
    old_score['p1'], old_score['p2'] = 0, 0

    # reset the paddles
    paddle_vel['p1'], paddle_vel['p2'] = 0, 0
    paddle_height['p1'] = paddle_height_default
    paddle_height['p2'] = paddle_height_default
    recentre_paddle('p1')
    recentre_paddle('p2')

    # reset the ball
    last_scored = 'none'
    ball_vel['x'], ball_vel['y'] = 0, 0
    ball_pos['x'] = CENTRE_BALL['x']
    ball_pos['y'] = CENTRE_BALL['y']

    # reset the effect message
    event_timer.stop()
    global_tick = 0
    effect_message = none
    played_score_sound = False

def keydown(key):
    global game_in_progress

    def _dir_up(player):
        global is_up
        if is_down[player]:
            paddle_vel[player] = 0
        else:
            paddle_vel[player] = -4
        is_up[player] = True

    def _dir_down(player):
        global is_down
        if is_up[player]:
            paddle_vel[player] = 0
        else:
            paddle_vel[player] = 4
        is_down[player] = True

    # player 1 controls
    if key == simplegui.KEY_MAP['w']:
        _dir_up('p1')
    if key == simplegui.KEY_MAP['s']:
        _dir_down('p1')

    # player 1 DVORAK controls
    if key == 188:
        _dir_up('p1')
    if key == 79:
        _dir_down('p1')

    # player 2 controls
    if not ai_is_on:
        if key == simplegui.KEY_MAP['up']:
            _dir_up('p2')
        if key == simplegui.KEY_MAP['down']:
            _dir_down('p2')

    # other controls
    if key == simplegui.KEY_MAP['space'] and not game_in_progress:
        launch_ball()
        game_in_progress = True
    if key == simplegui.KEY_MAP['m']:
        music_on_off()

def keyup(key):

    def _dir_up(player):
        global is_up
        if is_down[player]:
            paddle_vel[player] = 4
        else:
            paddle_vel[player] = 0
        is_up[player] = False

    def _dir_down(player):
        global is_down
        if is_up[player]:
            paddle_vel[player] = -4
        else:
            paddle_vel[player] = 0
        is_down[player] = False

    # player 1 controls
    if key == simplegui.KEY_MAP['w']:
        _dir_up('p1')
    if key == simplegui.KEY_MAP['s']:
        _dir_down('p1')

    # player 1 DVORAK controls
    if key == 188:
        _dir_up('p1')
    if key == 79:
        _dir_down('p1')

    # player 2 controls
    if not ai_is_on:
        if key == simplegui.KEY_MAP['up']:
            _dir_up('p2')
        if key == simplegui.KEY_MAP['down']:
            _dir_down('p2')

def ai_on_off():
    """ Single-Player / Multiplayer switcher """
    global ai_is_on, p2_label
    if ai_is_on:
        # if Single-Player is on, switch to Multi-Player
        button_ai.set_text("SINGLE PLAYER")
        p2_label = "PLAYER 2"
    else:
        # if Multi-Player is on, switch to Single-Player
        button_ai.set_text("MULTIPLAYER")
        p2_label = "A.I."
    ai_is_on = not ai_is_on
    new_game()

def event_tick():
    """ Display timed effects """
    global global_tick, effect_message, played_score_sound

    global_tick += 1

    # play score messages and sounds
    if global_tick <= message_delay:
        if last_scored == 'p1':
            effect_message = p1scored
            if not played_score_sound:
                play_sound('score')
                played_score_sound = True
        elif last_scored == 'p2' and ai_is_on:
            effect_message = aiscored
            if not played_score_sound:
                play_sound('fail')
                played_score_sound = True
        elif last_scored == 'p2':
            effect_message = p2scored
            if not played_score_sound:
                play_sound('score')
                played_score_sound = True

    # update the size of the paddles
    if global_tick == message_delay + 1:
        if last_scored == 'p1':
            update_difficulty('p1')
            old_score['p1'] = score['p1']
        elif last_scored == 'p2':
            update_difficulty('p2')
            old_score['p2'] = score['p2']

    # play the countdown
    if global_tick == message_delay + 2:
        effect_message = countdown_3
        play_sound('countdown')
        paddle_colour['p1'] = paddle_default_colour
        paddle_colour['p2'] = paddle_default_colour
    if global_tick == message_delay + 3:
        effect_message = countdown_2
        play_sound('countdown')
    if global_tick == message_delay + 4:
        effect_message = countdown_1
        play_sound('countdown')

    # reset the effect message and launch the new ball
    if global_tick == message_delay + 5:
        event_timer.stop()
        global_tick = 0
        played_score_sound = False
        effect_message = none
        launch_ball()

def music_on_off():
    global music_is_on
    music_is_on = not music_is_on
    if not music_is_on:
        music.pause()
        music.rewind()
        music_timer.stop()
    else:
        music_timer.start()
        music_tick()

def music_tick ():
    if music_is_on:
        music.rewind()
        music.play()

def draw(canvas):
    """ Draw the game's graphics """
    global paddle_pos, ball_pos, ball_vel, ai_difficulty
 
    canvas.draw_image(background, (300, 200), (600, 400), (300, 200), (600, 400))

    # draw the scores
    canvas.draw_text(score_string['p1'], [score_x['p1'], SCORE_Y], score_size, score_colour, score_font)
    canvas.draw_text(score_string['p2'], [score_x['p2'], SCORE_Y], score_size, score_colour, score_font)

    # draw player labels
    canvas.draw_text(p1_label, [p1_label_x, LABEL_Y], label_size, label_colour, label_font)
    canvas.draw_text(p2_label, [p2_label_x, LABEL_Y], label_size, label_colour, label_font)

    # A.I. subroutine
    if ai_is_on and ball_vel['x'] > 0:
        if ball_pos['y'] < (paddle_y['p2'] - 10):
            paddle_vel['p2'] = -4
        elif ball_pos['y'] > (paddle_y['p2'] + (paddle_height['p2'] - 10)):
            paddle_vel['p2'] = 4
    elif ai_is_on:
        paddle_vel['p2'] = 0

    # update and draw the paddles
    paddle_pos['p1'] = update_paddle('p1')
    paddle_pos['p2'] = update_paddle('p2')
    canvas.draw_polygon(paddle_pos['p1'], 1, paddle_colour['p1'], paddle_colour['p1'])
    canvas.draw_polygon(paddle_pos['p2'], 1, paddle_colour['p2'], paddle_colour['p2'])

    # update and draw the ball
    ball_pos['x'] += ball_vel['x']
    ball_pos['y'] += ball_vel['y']
    update_ball()
    canvas.draw_circle([ball_pos['x'], ball_pos['y']], BALL_RADIUS, 1, ball_colour, ball_colour)

    # draw the effects
    canvas.draw_image(effect_message, (286, 40), (572, 80), (300, 200), (572, 80))


#
# DEFINE FRAME ELEMENTS
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

# create frame
frame = simplegui.create_frame('Pong', FRAME_WIDTH, FRAME_HEIGHT, CONTROL_WIDTH)

# define draw handler
frame.set_draw_handler(draw)

# define key handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# create timers
event_timer = simplegui.create_timer(blink_interval, event_tick)
music_timer = simplegui.create_timer(music_interval, music_tick)

# load images
background = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/bg-c.jpg')
p1scored = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/p1-scored.jpg')
p2scored = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/p2-scored.jpg')
aiscored = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/ai-scored.jpg')
countdown_3 = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/cd3.jpg')
countdown_2 = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/cd2.jpg')
countdown_1 = simplegui.load_image('http://www.chloeunrau.com/stuff/pong/cd1.jpg')
none = simplegui.load_image('')
effect_message = none

# load music
# music is from http://www.flashkit.com/loops/Techno-Dance/Techno/Technola-Billy_Pf-10125/index.php
# and is under a Shareware license, with no license details specified by the author
music = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/music.ogg')
music.set_volume(0.7)

# load sound effects
# All sound effects are from www.freesound.org under a Creative Commons license
sound_gutter = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/gutter.ogg')
sound_bounce = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/bounce.ogg')
sound_score = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/score.ogg')
sound_fail = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/failure.ogg')
sound_countdown = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/countdown.ogg')
sound_launch = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/launch.ogg')
sound_newgame = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/reset.ogg')
sound_shrink = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/shrink.ogg')
sound_grow = simplegui.load_sound('http://www.chloeunrau.com/stuff/pong/grow.ogg')


#
# REGISTER EVENT HANDLERS (elements that appear in the Control area)
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

frame.add_button("RESET / NEW GAME", new_game, CONTROL_WIDTH)
frame.add_label("")
frame.add_label("Change mode to...")
button_ai = frame.add_button("SINGLE PLAYER", ai_on_off, CONTROL_WIDTH)
frame.add_label("")
frame.add_label("Press SPACEBAR to launch the ball.")
frame.add_label("")
frame.add_label("Press M to mute/unmute music.")
frame.add_label("")
frame.add_label("PLAYER 1 controls:")
frame.add_label("Up: W or ,")
frame.add_label("Down: S or O")
frame.add_label("")
frame.add_label("PLAYER 2 controls:")
frame.add_label("Up: Up Arrow")
frame.add_label("Down: Down Arrow")


#
# INITIATE PROGRAM
# _____________________________________________________________________________
# -----------------------------------------------------------------------------

frame.start()
update_score_pos()
update_label_pos()
music_timer.start()
music_tick()

