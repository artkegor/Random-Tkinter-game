# --------------------------------------------------------------------------
# Управление при помощи стрелок. E, F и B создает обычного врага, огонь или босса соответственно.
# --------------------------------------------------------------------------
# Цель: пройти к выходу не столкнувшись с огнем или врагом.
# --------------------------------------------------------------------------


import tkinter
import random

STEP = 60
N_X = 10
N_Y = 10
WIDTH = STEP * N_X
HEIGHT = STEP * N_Y
N_FIRES = 6  # Число клеток, заполненных огнем
N_ENEMIES = 4  # Число врагов
N_BOSSES = 2  # Число боссов


def load_images():
    global PLAYER_PIC, EXIT_PIC, FIRE_PIC, ENEMY_PIC, BOSS_PIC
    PLAYER_PIC = tkinter.PhotoImage(file=r"C:\Users\artam\Pictures\doctor.png")
    EXIT_PIC = tkinter.PhotoImage(file=r"C:\Users\artam\Pictures\exit.png")
    FIRE_PIC = tkinter.PhotoImage(file=r"C:\Users\artam\Pictures\fire.png")
    ENEMY_PIC = tkinter.PhotoImage(file=r"C:\Users\artam\Pictures\enemy.png")
    BOSS_PIC = tkinter.PhotoImage(file=r"C:\Users\artam\Pictures\boss.png")


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    x_left, y_top = canvas.coords(obj)
    x_right = x_left + STEP
    y_bottom = y_top + STEP
    if x_right <= 0:
        canvas.move(obj, WIDTH, 0)
    if x_left >= WIDTH:
        canvas.move(obj, -WIDTH, 0)
    if y_bottom <= 0:
        canvas.move(obj, 0, HEIGHT)
    if y_top >= HEIGHT:
        canvas.move(obj, 0, -HEIGHT)


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
            break
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
            break
    for b in bosses:
        if canvas.coords(player) == canvas.coords(b[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
            break


def always_right(_):
    return (STEP, 0)


def always_left(_):
    return (-STEP, 0)


def always_top(_):
    return (0, -STEP)


def always_bottom(_):
    return (0, STEP)


def random_move(_):
    return random.choice([(STEP, 0), (-STEP, 0), (0, STEP), (0, -STEP)])


# Движение врагов
def enemy_move(enemy):
    player_x, player_y = canvas.coords(player)
    self_x, self_y = canvas.coords(enemy)
    dx = 0
    dy = 0
    if player_x > self_x:
        dx = STEP
    elif player_x < self_x:
        dx = -STEP
    if player_y > self_y:
        dy = STEP
    elif player_y < self_y:
        dy = -STEP
    return (dx, dy)


# Движение босса
def boss_move(boss):
    player_x, player_y = canvas.coords(player)
    self_x, self_y = canvas.coords(boss)
    dx = 0
    dy = 0
    if player_x > self_x:
        dx = STEP * 2
    elif player_x < self_x:
        dx = -STEP * 2
    if player_y > self_y:
        dy = STEP * 2
    elif player_y < self_y:
        dy = -STEP * 2
    return (dx, dy)


def do_nothing(x):
    pass


def key_pressed(event):
    for enemy, direction in enemies:
        move_wrap(enemy, direction(enemy))  # произвести перемещение
    for boss, direction in bosses:
        move_wrap(boss, direction(boss))
    if event.keysym == 'Up':
        move_wrap(player, (0, -STEP))
    elif event.keysym == 'Down':
        move_wrap(player, (0, STEP))
    elif event.keysym == 'Left':
        move_wrap(player, (-STEP, 0))
    elif event.keysym == 'Right':
        move_wrap(player, (STEP, 0))
    # B создаёт босса, который двигается в 2 раза быстрее чем игрок или обычный враг
    elif event.keysym == 'b':
        boss = canvas.create_image(0, 0, image=BOSS_PIC, anchor='nw')
        bosses.append((boss, boss_move))
    # E создает обычного врага
    elif event.keysym == 'e':
        enemy = canvas.create_image(0, 0, image=ENEMY_PIC, anchor='nw')
        enemies.append((enemy, random_move))
    # F создает клетку с огнем
    elif event.keysym == 'f':
        fire = canvas.create_image(0, 0, image=FIRE_PIC, anchor='nw')
        fires.append(fire)
    check_move()


def prepare_and_start():
    global player, exit, fires, enemies, bosses
    canvas.delete("all")
    busy_cells = set()
    player_pos = (random.randrange(0, N_X) * STEP,
                  random.randrange(0, N_Y) * STEP)
    busy_cells.add(player_pos)
    while True:
        exit_pos = (random.randrange(0, N_X) * STEP,
                    random.randrange(0, N_Y) * STEP)
        if exit_pos not in busy_cells:
            busy_cells.add(exit_pos)
            break
    player = canvas.create_image(
        (player_pos[0], player_pos[1]), image=PLAYER_PIC, anchor='nw')
    exit = canvas.create_image(
        (exit_pos[0], exit_pos[1]), image=EXIT_PIC, anchor='nw')
    fires = []
    for i in range(N_FIRES):
        while True:
            fire_pos = (random.randrange(0, N_X) * STEP,
                        random.randrange(0, N_Y) * STEP)
            if fire_pos not in busy_cells:
                busy_cells.add(fire_pos)
                break

        fire = canvas.create_image(
            (fire_pos[0], fire_pos[1]), image=FIRE_PIC, anchor='nw')
        fires.append(fire)
    enemies = []
    for i in range(N_ENEMIES):
        while True:
            enemy_pos = (random.randrange(0, N_X) * STEP,
                         random.randrange(0, N_Y) * STEP)
            if enemy_pos not in busy_cells:
                busy_cells.add(enemy_pos)
                break
        enemy = canvas.create_image(enemy_pos, image=ENEMY_PIC, anchor='nw')
        enemies.append(
            (enemy, random.choice([always_right, random_move, always_left, always_top, always_bottom, enemy_move])))
    bosses = []
    for i in range(N_BOSSES):
        while True:
            boss_pos = (random.randrange(0, N_X) * STEP,
                        random.randrange(0, N_Y) * STEP)
            if boss_pos not in busy_cells:
                busy_cells.add(boss_pos)
                break
        boss = canvas.create_image(boss_pos, image=BOSS_PIC, anchor='nw')
        bosses.append((boss, boss_move))
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


master = tkinter.Tk()
load_images()
canvas = tkinter.Canvas(master, bg='blue', width=WIDTH, height=HEIGHT)
label = tkinter.Label(master)
label.pack()
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()
