import turtle
import random
import time

# Register a new shape for the invader (man shape)
turtle.register_shape("man_shape", ((0, 0), (0, 20), (5, 25), (-5, 25), (0, 20)))

# Set up the screen
wn = turtle.Screen()
wn.title("Space Invaders")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # Turn off automatic screen updates

# Player Ship
player = turtle.Turtle()
player.shape("circle")
player.color("yellow")
player.shapesize(stretch_wid=1, stretch_len=2)
player.penup()
player.goto(0, -250)
player.setheading(90)

# Set the speed for the player's movement
player_speed = 15

# Bullets
bullets = []
invader_bullets = []

# Score
score = 0

# Score display
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: {}".format(score), align="center", font=("Arial", 16, "normal"))

# Function to shoot bullets
def shoot(bullet_list, x, y):
    bullet = turtle.Turtle()
    bullet.shape("triangle")
    bullet.color("pink")
    bullet.shapesize(stretch_wid=0.15, stretch_len=0.1)
    bullet.penup()
    bullet.speed(0)
    bullet.goto(x, y)
    bullet_list.append(bullet)

# Function to choose an invader to shoot
def choose_invader_to_shoot():
    return random.choice(invaders)

# Function to display Game Over message
def game_over(message="You got hit! Game Over. Write OK to exit."):
    user_input = turtle.textinput("Game Over", message)
    if user_input is None or user_input.lower() == "ok":
        wn.bye()

# Function to display You Win message
def you_win(message="You Win!!!"):
    turtle.clear()
    turtle.goto(0, 0)
    turtle.color("white")
    turtle.shape("circle")
    turtle.write(message, align="center", font=("Arial", 50, "normal"))

# Keyboard bindings
wn.listen()
wn.onkey(lambda: player.setx(player.xcor() + player_speed), "Right")
wn.onkey(lambda: player.setx(player.xcor() - player_speed), "Left")
wn.onkey(lambda: shoot(bullets, player.xcor(), player.ycor() + 10), "space")

# Invaders
invaders = []

# Create three lines of six invaders each
for y_offset in range(3):
    for x_offset in range(6):
        invader = turtle.Turtle()
        invader.shape("man_shape")  # Use the custom man shape
        invader.color("red")
        invader.penup()
        invader.speed(0)
        x = -300 + x_offset * 100
        y = 200 - y_offset * 40
        invader.goto(x, y)
        invaders.append(invader)

# Set the speed of the invaders to a slower value
invader_speed = 0.15  # Adjust this value to make invaders slower

# Main game loop
while True:
    wn.update()

    # Move the invaders
    for invader in invaders:
        invader.setx(invader.xcor() + invader_speed)

        # Check if any invader has reached the screen edges
        if invader.xcor() > 390 or invader.xcor() < -390:
            # Move all invaders down
            for inv in invaders:
                inv.sety(inv.ycor() - 20)

            # Reverse the direction of all invaders
            invader_speed *= -1

    # Move the bullets and hide/remove them when reaching the top
    for bullet in bullets:
        bullet.sety(bullet.ycor() + 20)

        # Check if the bullet has reached the top
        if bullet.ycor() >= 320:
            # Hide or remove the bullet based on your preference
            bullet.hideturtle()

    # Randomly make invaders shoot
    if random.random() < 0.01:
        invader_to_shoot = choose_invader_to_shoot()
        shoot(invader_bullets, invader_to_shoot.xcor(), invader_to_shoot.ycor() - 10)

    # Shoot the invader bullets and hide/remove them when reaching the bottom
    for invader_bullet in invader_bullets:
        invader_bullet.sety(invader_bullet.ycor() - 10)

        # Check if the invader bullet has reached the bottom
        if invader_bullet.ycor() <= -300:
            # Hide or remove the invader bullet based on your preference
            invader_bullet.hideturtle()

    # Check for collisions between bullets and invaders
    for bullet in bullets:
        for invader in invaders:
            if (
                invader.distance(bullet) < 15
                and bullet.ycor() < 200
                and bullet.ycor() > -200
            ):
                # Bullet hit an invader
                invader.hideturtle()
                bullet.hideturtle()
                score += 10
                score_display.clear()
                score_display.write(
                    "Score: {}".format(score), align="center", font=("Arial", 16, "normal")
                )

    # Check for collisions between invader bullets and the player
    for invader_bullet in invader_bullets:
        if (
            player.distance(invader_bullet) < 15
            and invader_bullet.ycor() < -200
        ):
            # Player hit by an invader bullet
            game_over()

    # Check for player collisions with the screen boundaries
    if player.xcor() > 390:
        player.setx(390)
    elif player.xcor() < -390:
        player.setx(-390)

    # Check if there are no more invaders left
    if not any(invader.isvisible() for invader in invaders):
        you_win("You Win!!!")
        # Stop updating the screen to freeze the game state
        wn.update()
        break

    # Add a small delay to avoid high CPU usage
    time.sleep(0.01)

# Keep the window open until the user closes it
turtle.mainloop()





