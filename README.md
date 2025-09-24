from pygame import *
from random import randint

init()
window_size = 1200, 800
window = display.set_mode(window_size)

clock = time.Clock()

player_img = transform.scale(image.load('bird.png'), (100, 100))

player_rect = Rect(150, window_size[1]//2 - 100, 100, 100)

def generate_pipes(count, pipes_width=140, gap=280, min_height=50, max_height = 450, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipes_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipes_width, window_size[1] - height - gap)
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pipes = generate_pipes(10)
main_font = font.Font(None, 100)
score = 0
lose = False
y_speed = 2
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.fill('sky blue')
    draw.rect(window, 'yellow', player_rect)
    window.blit(player_img, (player_rect.x, player_rect.y))

    keys = key.get_pressed()
    if keys[K_w] and not lose: player_rect.y -= 15
    if keys[K_s] and not lose: player_rect.y += 15
    if lose: 
        player_rect.y += y_speed
        y_speed *= 1.1
    if player_rect.y < 0 or player_rect.bottom > window_size[1]: lose =True
    if keys[K_r] and lose:
        player_rect.y = window_size[1]//2
        lose = False
        pipes = generate_pipes(10)
        y_speed = 2

    for pipe in pipes[:]:
        if not lose:
            pipe.x -= 10
        draw.rect(window, 'green', pipe)
        if player_rect.colliderect(pipe):
            lose = True
        if pipe.x <= -100:
            pipes.remove(pipe)
            score += 0.5
    if len(pipes) < 4:
        pipes += generate_pipes(10)

    score_txt = main_font.render(f'{int(score)}', 1, 'black')
    window.blit(score_txt, (100, 40))

    display.update()
    clock.tick(60)
