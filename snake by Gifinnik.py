from tkinter import *
import random

#global vars
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


# snake's meal
def create_block():
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE, posy + SEG_SIZE,
                          fill="#DC143C")

# Score counter
class Score(object):

    # Score proector
    def __init__(Gifinnik):
        Gifinnik.score = 0
        Gifinnik.x = 55
        Gifinnik.y = 15
        c.create_text(Gifinnik.x, Gifinnik.y, text="score: {}".format(Gifinnik.score), font="Arial 20",
                      fill="#FFD700", tag="score", state='hidden')

    # Count and share to the screen
    def increment(Gifinnik):
        c.delete("score")
        Gifinnik.score += 1
        c.create_text(Gifinnik.x, Gifinnik.y, text="score: {}".format(Gifinnik.score), font="Arial 20",
                      fill="#FFD700", tag="score")

    # Score cleaner
    def reset(Gifinnik):
        c.delete("score")
        Gifinnik.score = 0

# main part:)
def main():
    global IN_GAME
    if IN_GAME:
        s.move()

        # Head coords
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # Walls
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Apple eating
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # Snake's eating
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False

        # Snake's speed
        root.after(100, main)

    else:
        set_state(res_text, 'normal')
        set_state(gg_text, 'normal')
        set_state(close, 'normal')

class Segment(object):
    def __init__(Gifinnik, x, y):
        Gifinnik.instance = c.create_rectangle(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill="#006400")
                                           
class Snake(object):
    def __init__(Gifinnik, segments):
        Gifinnik.segments = segments

        # moving variants
        Gifinnik.mapping = {"s": (0, 1), "d": (1, 0),
                        "w": (0, -1), "a": (-1, 0)}

        # start angle
        Gifinnik.vector = Gifinnik.mapping["d"]

    def move(Gifinnik):
        for index in range(len(Gifinnik.segments) - 1):
            segment = Gifinnik.segments[index].instance
            x1, y1, x2, y2 = c.coords(Gifinnik.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(Gifinnik.segments[-2].instance)
        c.coords(Gifinnik.segments[-1].instance,
                 x1 + Gifinnik.vector[0] * SEG_SIZE, y1 + Gifinnik.vector[1] * SEG_SIZE,
                 x2 + Gifinnik.vector[0] * SEG_SIZE, y2 + Gifinnik.vector[1] * SEG_SIZE)

    def add_segment(Gifinnik):
        score.increment()
        last_seg = c.coords(Gifinnik.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        Gifinnik.segments.insert(0, Segment(x, y))

    def change_direction(Gifinnik, event):
        if event.keysym in Gifinnik.mapping:
            Gifinnik.vector = Gifinnik.mapping[event.keysym]

    # Reset
    def reset_snake(Gifinnik):
        for segment in Gifinnik.segments:
            c.delete(segment.instance)

# Write text
def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK, state='hidden')


# Start button pressing
def start_button(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    score.reset()
    c.itemconfigure(res_text, state='hidden')
    c.itemconfigure(gg_text, state='hidden')
    c.itemconfigure(close, state='hidden')
    start_game()

# Game start
def start_game():
    global s
    create_block()
    s = create_snake()

    c.bind("<w>", s.change_direction)
    c.bind("<a>", s.change_direction)
    c.bind("<s>", s.change_direction)
    c.bind("<d>", s.change_direction)
    main()


# Snake and her segments
def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)
    
# Exit
def close_win(root):
    exit()


root = Tk()
root.title("Snake game|Gifinnik")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
c.grid()
c.focus_set()

# Text for game
gg_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER!",
                               font='Arial 20', fill='#8B0000',
                               state='hidden')

res_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3,
                             font='Arial 25',
                             fill='#228B22',
                             text="START NEW",
                             state='hidden')

close = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 5, font='Arial 25',
                          fill='#8B0000',
                          text="EXIT",
                          state='hidden')

# Binds
c.tag_bind(res_text, "<Button-1>", start_button)
c.tag_bind(close, "<Button-1>", close_win)

# Score counting
score = Score()

# Start
start_game()

root.mainloop()