import pygame as pg
import random

width, height = 700, 450
FPS = 60
BLACK = (0, 0, 0)
x_direction = 0
y_direction = 0
player_speed = 2
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
}

player_view = 'rear'
player_rect = images_dict['player'][player_view].get_rect()
player_rect.x = 300
player_rect.y = 300

hotel_img = images_dict['hotel']
hotel_rect = hotel_img.get_rect()
hotel_positions = [
    (60, 30),
    (555, 30),
    (60, 250),
    (440, 250)
]
hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

passenger_img = images_dict['passenger']
passenger_rect = passenger_img.get_rect()
passenger_rect.x, passenger_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height

parking_img = images_dict['taxi_background']
parking_rect = parking_img.get_rect()
parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height

def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1):
            try:
                if screen.get_at((x,y)) == (220, 215, 177):
                    return True
            except:
                print("Oops")
    if hotel_rect.colliderect(player_rect):
        return True
    return False

pg.init()
screen = pg.display.set_mode([width, height])
timer = pg.time.Clock()

run = True
while run:
    timer.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys_klava = pg.key.get_pressed()
    if keys_klava[pg.K_RIGHT] and player_rect.x < width - player_rect.width:
        x_direction = 1
        player_view = 'right'
    elif keys_klava[pg.K_LEFT] and player_rect.x > 0:
        x_direction = -1
        player_view = 'left'
    elif keys_klava[pg.K_UP] and player_rect.y > 0:
        y_direction = -1
        player_view = 'rear'
    elif keys_klava[pg.K_DOWN] and player_rect.y <= height - player_rect.height:
        y_direction = 1
        player_view = 'front'

    player_rect.x += player_speed * x_direction
    player_rect.y += player_speed * y_direction
    x_direction = 0
    y_direction = 0

    if is_crash():
        print("CRASH")

    screen.fill(BLACK)
    screen.blit(images_dict['bg'], (0, 0))

    screen.blit(parking_img, parking_rect)
    screen.blit(hotel_img, hotel_rect)
    screen.blit(passenger_img, passenger_rect)
    screen.blit(images_dict['player'][player_view], player_rect)

    pg.display.flip()

pg.quit()
