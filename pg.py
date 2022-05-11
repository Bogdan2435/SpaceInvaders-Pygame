import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Primul joc!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BOARDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 5

RACHETA_WIDTH, RACHETA_HEIGHT = 55, 40

RACHETA_GALBENA_IMAGINE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
RACHETA_GALBENA = pygame.transform.rotate(
    pygame.transform.scale(RACHETA_GALBENA_IMAGINE, (RACHETA_WIDTH, RACHETA_HEIGHT)), 90)

RACHETA_ROSIE_IMAGINE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RACHETA_ROSIE = pygame.transform.rotate(
    pygame.transform.scale(RACHETA_ROSIE_IMAGINE, (55, 40)), 270)

GALBEN_HIT = pygame.USEREVENT + 1
ROSU_HIT = pygame.USEREVENT + 2

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(rosu, galben, rosu_bullets, galben_bullets, viata_rosu, viata_galben):

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BOARDER)

    viata_rosu_text = HEALTH_FONT.render("HEALTH: " + str(viata_rosu), 1, WHITE)
    viata_galben_text = HEALTH_FONT.render("HEALTH: " + str(viata_galben), 1, WHITE)

    WIN.blit(viata_rosu_text, (WIDTH - viata_rosu_text.get_width() - 10, 10))
    WIN.blit(viata_galben_text, (10, 10))

    WIN.blit(RACHETA_ROSIE, (rosu.x, rosu.y)) 
    WIN.blit(RACHETA_GALBENA, (galben.x, galben.y)) 



    for bullet in rosu_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in galben_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def miscare_galben(keys_pressed, galben):
    if keys_pressed[pygame.K_a] and galben.x - VEL > 0: #STANGA
        galben.x -= VEL
    if keys_pressed[pygame.K_d] and galben.x + VEL + galben.width < BOARDER.x + 10 : #DREAPTA
        galben.x += VEL
    if keys_pressed[pygame.K_w] and galben.y - VEL > 0: #SUS
        galben.y -= VEL
    if keys_pressed[pygame.K_s] and galben.y + VEL + galben.height  < HEIGHT- 15: #JUS
        galben.y += VEL

def miscare_rosu(keys_pressed, rosu):
    if keys_pressed[pygame.K_LEFT] and rosu.x - VEL > BOARDER.x + 15: #STANGA
        rosu.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and rosu.x + VEL + rosu.width - 15 < WIDTH: #DREAPTA
        rosu.x += VEL
    if keys_pressed[pygame.K_UP] and rosu.y - VEL > 0: #SUS
        rosu.y -= VEL
    if keys_pressed[pygame.K_DOWN] and rosu.y + VEL + rosu.height  < HEIGHT- 15: #JUS
        rosu.y += VEL

def handle_bullets(galben_bullets, rosu_bullets, galben, rosu):
    for bullet in galben_bullets:
        bullet.x +=BULLET_VEL
        if rosu.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ROSU_HIT))
            galben_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            galben_bullets.remove(bullet)
    
    for bullet in rosu_bullets:
        bullet.x -=BULLET_VEL
        if galben.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GALBEN_HIT))
            rosu_bullets.remove(bullet)
        elif bullet.x < 0:
            rosu_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    rosu = pygame.Rect(600, 100, RACHETA_WIDTH, RACHETA_HEIGHT)
    galben = pygame.Rect(200, 100, RACHETA_WIDTH, RACHETA_HEIGHT)

    rosu_bullets = []
    galben_bullets = []
    viata_rosu = 10
    viata_galben = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(galben_bullets) < MAX_BULLETS :
                    bullet = pygame.Rect(galben.x + galben.width, galben.y + galben.height//2 - 2, 10, 5)
                    galben_bullets.append(bullet) 
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(rosu_bullets) < MAX_BULLETS :
                    bullet = pygame.Rect(rosu.x , rosu.y + rosu.height//2 - 2, 10, 5)
                    rosu_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play() 
            
            if event.type == ROSU_HIT:
                viata_rosu -= 1
                BULLET_HIT_SOUND.play()
            if event.type == GALBEN_HIT:
                viata_galben -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if viata_rosu <= 0:
            winner_text = "Yellow WINS!"
        if viata_galben <= 0:
            winner_text = "Red WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        miscare_galben(keys_pressed, galben)
        miscare_rosu(keys_pressed, rosu)

        handle_bullets(galben_bullets, rosu_bullets, galben, rosu)

        draw_window(rosu, galben, rosu_bullets, galben_bullets, viata_rosu, viata_galben)

    pygame.quit()

if __name__ == '__main__':
    main()