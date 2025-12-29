# main.py
from ursina import *
import random

app = Ursina()

# Window setup
window.title = "Dodge Cubes"
window.borderless = False
window.fullscreen = False
window.color = color.azure

# Player cube
player = Entity(model='cube', color=color.orange, scale_y=0.5, scale_x=1, scale_z=1, position=(0,0,0))

# Ground
ground = Entity(model='plane', scale=20, color=color.gray, collider='box')

# Obstacles list
obstacles = []

# Game variables
speed = 5
spawn_timer = 0
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.85,0.45), scale=2)

def update():
    global spawn_timer, score

    # Player movement
    if held_keys['a'] or held_keys['left arrow']:
        player.x -= time.dt * speed * 5
    if held_keys['d'] or held_keys['right arrow']:
        player.x += time.dt * speed * 5

    # Limit player movement
    player.x = clamp(player.x, -4, 4)

    # Spawn obstacles
    spawn_timer += time.dt
    if spawn_timer > 1:
        spawn_timer = 0
        obs = Entity(model='cube', color=color.red, scale_y=1, scale_x=1, scale_z=1,
                     position=(random.randint(-4,4),0.5,10), collider='box')
        obstacles.append(obs)

    # Move obstacles
    for obs in obstacles:
        obs.z -= time.dt * speed
        if obs.z < -1:
            destroy(obs)
            obstacles.remove(obs)
            score += 1
            score_text.text = f'Score: {score}'

        # Collision
        if player.intersects(obs).hit:
            score_text.text = f'Game Over! Score: {score}'
            player.color = color.red
            invoke(application.quit, delay=2)

# Run the game
app.run()