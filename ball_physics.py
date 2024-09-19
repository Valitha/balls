import pygame
import sys
import random
import math

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("i <3 balls")

PINK = (255, 192, 203)
PURPLE = (186, 85, 211)
DARK_PURPLE = (148, 0, 211)
BLACK = (0, 0, 0)

ball_radius = 20
num_balls = 10
gravity = 0.2
elasticity = 0.8
erratic_force = 0.1

balls = []
team_a_collisions = 0
team_b_collisions = 0

for i in range(num_balls):
    ball_pos = [random.randint(ball_radius, width - ball_radius), random.randint(ball_radius, height - ball_radius)]
    ball_velocity = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)]
    team = "A" if i < num_balls // 2 else "B"  # Split into two teams
    balls.append({"pos": ball_pos, "velocity": ball_velocity, "team": team})

rectangles = [
    {"pos": [100, 200], "size": [150, 30], "velocity": [2, 0]},
    {"pos": [500, 400], "size": [200, 30], "velocity": [-2, 0]},
]

num_small_rects = 10
small_rects = []
for _ in range(num_small_rects):
    rect_width = random.randint(20, 40)
    rect_height = random.randint(10, 20)
    rect_x = random.randint(0, width - rect_width)
    rect_y = random.randint(0, height - rect_height)
    rect_velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
    small_rects.append({"pos": [rect_x, rect_y], "size": [rect_width, rect_height], "velocity": rect_velocity})

dragging = None
clock = pygame.time.Clock()

def check_ball_collision(ball1, ball2):
    dist = math.hypot(ball1["pos"][0] - ball2["pos"][0], ball1["pos"][1] - ball2["pos"][1])
    return dist < ball_radius * 2

def resolve_ball_collision(ball1, ball2):
    dx = ball1["pos"][0] - ball2["pos"][0]
    dy = ball1["pos"][1] - ball2["pos"][1]
    distance = math.hypot(dx, dy) or 0.1

    nx = dx / distance
    ny = dy / distance

    dpTan1 = ball1["velocity"][0] * -ny + ball1["velocity"][1] * nx
    dpTan2 = ball2["velocity"][0] * -ny + ball2["velocity"][1] * nx

    dpNorm1 = ball1["velocity"][0] * nx + ball1["velocity"][1] * ny
    dpNorm2 = ball2["velocity"][0] * nx + ball2["velocity"][1] * ny

    m1 = dpNorm1 * (1 - elasticity) + 2 * dpNorm2
    m2 = dpNorm2 * (1 - elasticity) + 2 * dpNorm1

    ball1["velocity"][0] = -ny * dpTan1 + nx * m1
    ball1["velocity"][1] = nx * dpTan1 + ny * m1
    ball2["velocity"][0] = -ny * dpTan2 + nx * m2
    ball2["velocity"][1] = nx * dpTan2 + ny * m2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, ball in enumerate(balls):
                if (ball["pos"][0] - mouse_x) ** 2 + (ball["pos"][1] - mouse_y) ** 2 <= ball_radius ** 2:
                    dragging = i
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging is not None:
            balls[dragging]["pos"] = list(event.pos)
            balls[dragging]["velocity"] = [0, 0]

    if dragging is None:
        for ball in balls:
            ball["velocity"][1] += gravity

            ball["velocity"][0] += random.uniform(-erratic_force / 2, erratic_force / 2)
            ball["velocity"][1] += random.uniform(-erratic_force / 2, erratic_force / 2)

            ball["pos"][0] += ball["velocity"][0]
            ball["pos"][1] += ball["velocity"][1]

            if ball["pos"][0] - ball_radius < 0:
                ball["pos"][0] = ball_radius
                ball["velocity"][0] = -ball["velocity"][0] * elasticity
            elif ball["pos"][0] + ball_radius > width:
                ball["pos"][0] = width - ball_radius
                ball["velocity"][0] = -ball["velocity"][0] * elasticity

            if ball["pos"][1] - ball_radius < 0:
                ball["pos"][1] = ball_radius
                ball["velocity"][1] = -ball["velocity"][1] * elasticity
            elif ball["pos"][1] + ball_radius > height:
                ball["pos"][1] = height - ball_radius
                ball["velocity"][1] = -ball["velocity"][1] * elasticity

            for rect in rectangles + small_rects:
                r_x, r_y, r_w, r_h = rect["pos"][0], rect["pos"][1], rect["size"][0], rect["size"][1]
                if (r_x < ball["pos"][0] < r_x + r_w and r_y < ball["pos"][1] + ball_radius < r_y + r_h):
                    ball["velocity"][1] = -ball["velocity"][1] * elasticity
                    ball["pos"][1] = r_y - ball_radius

        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                if check_ball_collision(balls[i], balls[j]):
                    resolve_ball_collision(balls[i], balls[j])
                    if balls[i]["team"] == "A" or balls[j]["team"] == "A":
                        team_a_collisions += 1
                    if balls[i]["team"] == "B" or balls[j]["team"] == "B":
                        team_b_collisions += 1

        for rect in rectangles:
            rect["pos"][0] += rect["velocity"][0]
            if rect["pos"][0] < 0 or rect["pos"][0] + rect["size"][0] > width:
                rect["velocity"][0] = -rect["velocity"][0]

        for rect in small_rects:
            rect["pos"][0] += rect["velocity"][0]
            rect["pos"][1] += rect["velocity"][1]
            if rect["pos"][0] < 0 or rect["pos"][0] + rect["size"][0] > width:
                rect["velocity"][0] = -rect["velocity"][0]
            if rect["pos"][1] < 0 or rect["pos"][1] + rect["size"][1] > height:
                rect["velocity"][1] = -rect["velocity"][1]

        for i in range(len(small_rects)):
            for j in range(i + 1, len(small_rects)):
                if check_ball_collision(small_rects[i], small_rects[j]):
                    

                    pass  

        for ball in balls:
            for rect in small_rects:
                r_x, r_y, r_w, r_h = rect["pos"][0], rect["pos"][1], rect["size"][0], rect["size"][1]
                if (r_x < ball["pos"][0] < r_x + r_w and r_y < ball["pos"][1] + ball_radius < r_y + r_h):
                    ball["velocity"][1] = -ball["velocity"][1] * elasticity
                    ball["pos"][1] = r_y - ball_radius

    window.fill(PINK)

    for rect in rectangles:
        pygame.draw.rect(window, DARK_PURPLE, (*rect["pos"], *rect["size"]))

    for rect in small_rects:
        pygame.draw.rect(window, PURPLE, (*rect["pos"], *rect["size"]))

    for ball in balls:
        color = PURPLE if ball["team"] == "A" else DARK_PURPLE
        pygame.draw.circle(window, color, (int(ball["pos"][0]), int(ball["pos"][1])), ball_radius)

    
    font = pygame.font.Font(None, 36)
    a_text = font.render(f"Team A Collisions: {team_a_collisions}", True, BLACK)
    b_text = font.render(f"Team B Collisions: {team_b_collisions}", True, BLACK)
    window.blit(a_text, (10, 10))
    window.blit(b_text, (10, 50))

    pygame.draw.line(window, BLACK, (0, 0), (0, height), 5)
    pygame.draw.line(window, BLACK, (width - 1, 0), (width - 1, height), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


