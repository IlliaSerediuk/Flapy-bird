from pygame import *
from random import randint
import sounddevice  as sd
import numpy as np

sr = 16000
block = 265 
mic_level=0.0

def audio_cb(indata, frame, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85* mic_level + 0.15 * rms








init()
window_size = 1200, 800
window = display.set_mode(window_size)

clock = time.Clock()


player_img = transform.scale(image.load('bird.jpg'), (100, 100))

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


y_vel = 0.0
wait = 40
gravity = 0.6
THRESH = 0.01
IMPULSE = -8.0
with sd.InputStream(samplerate=sr,channels=1, blocksize=block, callback=audio_cb):





    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()



        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player_rect.y += int(y_vel)




        window.fill('sky blue')
        draw.rect(window, 'yellow', player_rect)
        keys = key.get_pressed()
        if player_rect.bottom > window_size[1]: 
            player_rect.bottom = window_size[1]
            y_vel = 0.0

        #перевірка торкання верхньої межі
        if player_rect.top < 0:
            player_rect.top = 0
            if y_vel < 0:
                y_vel = 0.0

        # рестарт гри
        if keys[K_r] and lose:
            player_rect.y = window_size[1]//2
            lose = False
            pipes = generate_pipes(10)
            y_speed = 2
            score = 0
            y_vel = 0.0

        if lose and wait > 1:
            for pipe in pipes:
                pipe.x += 8
            wait -= 1
        else:
            lose = False
            wait = 40
        
        
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