import tkinter as tk
import turtle, random
import winsound

FRAME_LIMIT = 300  # define frame size

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.game_over = False  # track when game is over

        # initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.penup()

        # set up drawers for score, timer, and message
        self.score_drawer = turtle.RawTurtle(canvas)
        self.score_drawer.hideturtle()
        self.score_drawer.penup()
        self.score_drawer.speed(0)
        self.score_drawer.color("white")

        self.timer_drawer = turtle.RawTurtle(canvas)
        self.timer_drawer.hideturtle()
        self.timer_drawer.penup()
        self.timer_drawer.speed(0)
        self.timer_drawer.color("white")


        self.message_drawer = turtle.RawTurtle(canvas)
        self.message_drawer.hideturtle()
        self.message_drawer.penup()
        self.message_drawer.speed(0)
        self.message_drawer.color("white")

        self.move_count = 0  # track number of moves

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def check_boundaries(self, turtle):
        x, y = turtle.xcor(), turtle.ycor()
        if x > FRAME_LIMIT:
            turtle.setx(FRAME_LIMIT)
        elif x < -FRAME_LIMIT:
            turtle.setx(-FRAME_LIMIT)

        if y > FRAME_LIMIT:
            turtle.sety(FRAME_LIMIT)
        elif y < -FRAME_LIMIT:
            turtle.sety(-FRAME_LIMIT)

    def start(self, init_dist=400, ai_timer_msec=100, time_limit=30):
        self.time_remaining = time_limit  # game timer
        self.base_score = 1000  # base score
        self.move_count = 0  # reset move count
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.update_timer()
        self.update_score()
        self.randomize_colors()  # start randomizing turtle colors every 3 seconds
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def update_timer(self):
        if self.game_over:
            return  # stop updating the timer if the game is over

        self.timer_drawer.clear()
        self.timer_drawer.penup()
        self.timer_drawer.setpos(-300, 270)
        self.timer_drawer.write(f'Time Left: {self.time_remaining}', font=("Arial", 16, "normal"))

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.canvas.ontimer(self.update_timer, 1000)  # decrease timer every second
        else:
            self.end_game(timer_ended=True)

    def update_score(self):
        if self.game_over:
            return  # stop updating the score if the game is over

        time_penalty = (30 - self.time_remaining) * 5  # more penalty for more time used
        move_penalty = self.move_count * 2  # more penalty for more moves
        score = max(0, self.base_score - time_penalty - move_penalty)

        if self.game_over and self.time_remaining == 0:
            score = 0  # set score to 0 if runner wins

        self.score_drawer.clear()
        self.score_drawer.penup()
        self.score_drawer.setpos(-300, 300)
        self.score_drawer.write(f'Score: {score}', font=("Arial", 16, "normal"))

    def step(self):
        if self.game_over:
            return  # stop the game loop if the game is over

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        self.check_boundaries(self.runner)
        self.check_boundaries(self.chaser)

        is_catched = self.is_catched()
        if is_catched:
            self.end_game(timer_ended=False)
        else:
            self.move_count += 1  # increment move count
            self.update_score()
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    def end_game(self, timer_ended):
        self.game_over = True  # set game over flag to true
        self.message_drawer.clear()
        self.message_drawer.penup()
        self.message_drawer.setpos(-300, 200)

        if timer_ended:
            self.message_drawer.write("Time's Up! Runner Wins!", font=("Arial", 24, "bold"))
        else:
            self.message_drawer.write("Chaser Wins! Game Over!", font=("Arial", 24, "bold"))

    def randomize_colors(self):
        if self.game_over:
            return  # stop changing colors if the game is over

        random_color_runner = (random.random(), random.random(), random.random())
        random_color_chaser = (random.random(), random.random(), random.random())
        self.runner.color(random_color_runner)
        self.chaser.color(random_color_chaser)

        # change colors every 3 seconds to make game a bit more difficult
        self.canvas.ontimer(self.randomize_colors, 3000)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # register event handlers for manual control
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class SmartRunner(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, chaser_pos, chaser_heading):
        x_diff = self.xcor() - chaser_pos[0]
        y_diff = self.ycor() - chaser_pos[1]
        if x_diff > 0:
            self.setheading(0)  # move right
        else:
            self.setheading(180)  # move left
        if y_diff > 0:
            self.setheading(90)  # move up
        else:
            self.setheading(270)  # move down
        self.forward(self.step_move)

def create_pixelated_background(screen, pixel_count=100):
    star_drawer = turtle.RawTurtle(screen)
    star_drawer.hideturtle()
    star_drawer.speed(0)
    star_drawer.penup()

    screen_width, screen_height = screen.window_width(), screen.window_height()

    for _ in range(pixel_count):
        x = random.randint(-screen_width // 2, screen_width // 2)
        y = random.randint(-screen_height // 2, screen_height // 2)
        star_drawer.setpos(x, y)
        star_drawer.dot(2, 'white')  # draw small white dot (size 2) at each position

if __name__ == '__main__':
    # Set up the window
    root = tk.Tk()
    root.title("Space Turtle Runaway")

    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor('black')

    # play sound while generating background
    winsound.PlaySound("turtle_runaway.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
    # create a space background effect
    create_pixelated_background(screen, pixel_count=40)

    # start game with the two turtles
    runner = SmartRunner(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()

    root.mainloop()
