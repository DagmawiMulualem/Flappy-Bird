import pygame  # library for game
import sys  # provides information about constants, functions and methods of the Python interpreter
import random  # pick random number element and more


def game_floor():  # this function will contain our game floor
    screen.blit(floor_base, (floor_x_pos, 900))  # position out floor base
    screen.blit(floor_base, (floor_x_pos + 576, 900))  # this code will extend the floor


def check_collision(pipes):  # this is the function that will hold the code for collision
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # this checkes if our bird and pipes collided.
            die_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:  # this will check if the floor is not hit
        die_sound.play()
        return False
    return True


def create_pipe():
    random_pip_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pip_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pip_pos))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:  # this else is saying if the top pipe dont show up add the pipe to the screen.
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


pygame.init()  # it is initializing(setting value) pygame
clock = pygame.time.Clock()  # this allows as to have control over our frame per second

gravity = 0.25  # this will controll how fast our character goes down
bird_movement = 0  # this is the defalt value for bird movment
screen = pygame.display.set_mode((576, 1024))  # set our screen size

Background = pygame.image.load("sprites/background-day.png").convert()  # load our background image
Background = pygame.transform.scale2x(Background)  # scale the background image

bird = pygame.image.load("sprites/redbird-midflap.png").convert_alpha()  # load the character
bird = pygame.transform.scale2x(bird)  # scale the character
bird_rect = bird.get_rect(center=(100, 512))  # we add a rectangle to detect collitions
floor_base = pygame.image.load("sprites/base.png").convert()  # load our floor image
floor_base = pygame.transform.scale2x(floor_base)  # this will scale the floor
floor_x_pos = 0  # this code will allow as to update our floor in the while loop
message = pygame.image.load("sprites/message.png").convert_alpha()  # load our message
message = pygame.transform.scale2x(message)  # this will scale the message screen
game_over_rect = message.get_rect(center=(288, 512))  # pos of our game
pipe_surface = pygame.image.load("sprites/pipe-red.png").convert()  # load the pipe image
pipe_surface = pygame.transform.scale2x(pipe_surface)  # scale the pipe
pipe_list = []
pipe_height = [400, 600, 800]

SpawnPipe = pygame.USEREVENT  # user event allows run code at certin frames
pygame.time.set_timer(SpawnPipe, 1200)  # this will allows as to spawn the pipes every 1.2 secs
flap_sound = pygame.mixer.Sound('audio/wing.wav')  # import sound
die_sound = pygame.mixer.Sound('audio/die.wav')  # import sound
game_active = True  # declared the game active varible
while True:
    for event in pygame.event.get():  # this for loop allows as to control what is going on in our game
        if event.type == pygame.QUIT:  # this if statement is telling python what type of event we are looking for
            pygame.quit()  # this is telling pygame to quit
            sys.exit()  # this code tells python to exit
        if event.type == pygame.KEYDOWN:  # this if statement is telling python what type of event we are looking for
            if event.key == pygame.K_SPACE and game_active:  # we set key(the space bar) to use in our game
                bird_movement = 0  # this will have the defalt number for value so it will make the bird go back to
                # its orginal place
                bird_movement -= 8  # this will subtract the value of the bird by 12 which will cause the bird to go up
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 512)  # we create a rectangle around our bird
                bird_movement = 0
                pipe_list.clear()  # this removes pipes
                game_active = True
        if event.type == SpawnPipe:  # this code is saying if the event is equal to spawnpipe in this case every 1.2
            # sec then crate pipe
            pipe_list.extend(create_pipe())

    screen.blit(Background, (0, 0))  # this code will add our background to our game

    if game_active:
        bird_movement += gravity  # this will add the value of gravity to the defalt value of bird_movement
        bird_rect.centery += bird_movement  # we set the gravity of our rectangle same as our bird so they will go
        # down togather
        screen.blit(bird, bird_rect)  # our characters position
        game_active = check_collision(pipe_list)  # this code checks for collision
        # game_active = check_collision()# this code checks for collision

        move_pipe(pipe_list)
        draw_pipes(pipe_list)
    else:
        screen.blit(message, game_over_rect)  # call our game_over_rect
    floor_x_pos -= 1
    game_floor()  # call our game floor function

    if floor_x_pos <= -576:  # this if statment is saying when the floor is done moving reset the postions so we will
        # have infinite loop of floor
        floor_x_pos = 0
    pygame.display.update()  # this will keep our display updated
    clock.tick(120)  # we set our frames per second
