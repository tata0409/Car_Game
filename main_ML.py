from collections import defaultdict
import numpy as np
import pygame as pg
import random

width, height = 700, 450
FPS = 2

BLACK = (0, 0, 0)


def start_positions():
    global player_view
    player_view = 'rear'
    player_rect.x = 300
    player_rect.y = 300
    #hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
    parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
    passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
    while passenger_rect.x == hotel_rect.x and passenger_rect.y == hotel_rect.y:
        passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
    passenger_rect.y += hotel_rect.height


def draw():
    screen.fill(BLACK)
    screen.blit(images_dict['bg'], (0, 0))
    screen.blit(parking_img, parking_rect)
    screen.blit(hotel_img, hotel_rect)
    screen.blit(passenger_img, passenger_rect)
    screen.blit(images_dict['player'][player_view], player_rect)
    pg.display.flip()


def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1):
            try:
                if screen.get_at((x, y)) == (220, 215, 177):
                    return True
            except IndexError:
                print("Oops")
    if hotel_rect.colliderect(player_rect):
        return True
    return False


def apply_action(action):
    if action is None:
        return
    global player_view
    x_direction, y_direction = 0, 0
    if action == 0:
        x_direction = 1
        player_view = 'right'
    elif action == 1:
        x_direction = -1
        player_view = 'left'
    elif action == 2:
        y_direction = -1
        player_view = 'rear'
    elif action == 3:
        y_direction = 1
        player_view = 'front'

    new_x = player_rect.x + player_rect.width * x_direction
    new_y = player_rect.y + player_rect.height * y_direction
    if 0 < new_x <= width - player_rect.width and 0 < new_y <= height - player_rect.height:
        player_rect.x, player_rect.y = new_x, new_y




def draw_message(text, color):
    font = pg.font.SysFont(None, 36)
    message = font.render(text, True, color)
    screen.blit(message, (350, 150))
    pg.display.flip()
    pg.time.delay(4000)


images_dict = {
    'bg': pg.image.load('img/Background.png'),
    'player': {
        'rear': pg.image.load('img/cab_rear.png'),
        'left': pg.image.load('img/cab_left.png'),
        'front': pg.image.load('img/cab_front.png'),
        'right': pg.image.load('img/cab_right.png'),
    },
    'hotel': pg.transform.scale(pg.image.load('img/hotel.png'), (80, 80)),
    'passenger': pg.image.load('img/passenger.png'),
    'hole': pg.image.load('img/hole.png'),
    'taxi_background': pg.transform.scale(pg.image.load('img/taxi_background.png'), (80, 45)),
    'parking': pg.transform.scale(pg.image.load('img/parking.png'), (80, 70))
}

player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()

hotel_img = images_dict['hotel']
hotel_rect = hotel_img.get_rect()
hotel_positions = [
    (60, 30),
    (555, 30),
    (60, 250),
    (440, 250)
]
hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

parking_img = images_dict['parking']
parking_rect = parking_img.get_rect()


passenger_img = images_dict['passenger']
passenger_rect = passenger_img.get_rect()


pg.init()
screen = pg.display.set_mode([width, height])

########################################################################

actions = [0, 1, 2, 3]  # 0 - right, 1 - left, 2 - up, 3 - down

Q_table = defaultdict(lambda: [0, 0, 0, 0])

learning_rate = 0.9
discount_factor = 0.9
epsilon = 0.1

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        return np.argmax(Q_table[state])


def update_q(state, action, reward, next_state):
    best_next = max(Q_table[next_state])
    Q_table[state][action] += learning_rate * (reward + discount_factor * best_next - Q_table[state][action])


def make_step():
    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)
    draw()
    reward = -1
    episode_end = False
    success = False
    if is_crash():
        reward = -100
        episode_end = True
    if parking_rect.contains(player_rect):
        print("Win")
        reward = 100
        episode_end = True
        success = True
    next_state = (player_rect.x, player_rect.y)
    update_q(current_state, action, reward, next_state)
    return (episode_end, success)


pg.init()
screen = pg.display.set_mode([width, height])
timer = pg.time.Clock()
start_positions()
learned = False
draw()

num_episodes = 300
max_steps = 50

for episode in range(num_episodes):
    player_rect.x = 300
    player_rect.y = 300
    for step in range(max_steps):
        (episode_end, success) = make_step()
        if episode_end:
            print("Win? -", success)
            break

learned = True
print(Q_table)

draw_message("End of learning", pg.Color("blue"))
########################################################################

timer = pg.time.Clock()

run = True
while run:
    timer.tick(FPS)
    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)
    draw()

    if is_crash():
        draw_message("CRASH", pg.Color('red'))
        run = False
        break

    if parking_rect.contains(player_rect):
        draw_message("You won", pg.Color('green'))
        start_positions()
        run = False
        break

pg.quit()
