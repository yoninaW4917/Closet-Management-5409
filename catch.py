import pygame
import random

# Initialize pygame
pygame.init()

# Set the width and height of the screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Catch Game")

# Set the clock
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Load the player's image
playerImage = pygame.image.load("images/stormont.png")
objImage = pygame.image.load("images/kraken.png")
rain = pygame.image.load("images/obs.png")

# Load sounds
pygame.mixer.music.load("sounds/driftveilCity.mp3")
pygame.mixer.music.play(-1)  # Play music in a loop
# catch_sound = pygame.mixer.Sound("sounds/catch.wav")
hitSound = pygame.mixer.Sound("sounds/jump.mp3")
gameOver = pygame.mixer.Sound("sounds/gameOver.mp3")


class Player(pygame.sprite.Sprite):
    """
    A class representing the player.

    Attributes:
        image (pygame.Surface): The image of the player.
        rect (pygame.Rect): The rectangle defining the player's position and dimensions.
        speed (int): The speed at which the player moves.
    """
    def __init__(self):
        super().__init__()
        self.image = playerImage
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 500
        self.speed = 5

    def update(self):
        """
        Update the player's position based on key presses and ensure the player stays within screen boundaries.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class Object(pygame.sprite.Sprite):
    """
    A class representing objects that the player should catch.

    Attributes:
        image (pygame.Surface): The image of the object.
        rect (pygame.Rect): The rectangle defining the object's position and dimensions.
        speed (int): The speed at which the object moves downwards.
    """
    def __init__(self):
        super().__init__()
        self.image = objImage
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 750)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randint(2, 8)

    def update(self):
        """
        Update the position of the object, moving it down the screen and resetting it if it goes off the screen.
        """
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.x = random.randrange(0, 750)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randint(2, 8)


class Obstacle(pygame.sprite.Sprite):
    """
    A class representing obstacles that the player should avoid.

    Attributes:
        image (pygame.Surface): The image of the obstacle.
        rect (pygame.Rect): The rectangle defining the obstacle's position and dimensions.
        speed (int): The speed at which the obstacle moves downwards.
    """
    def __init__(self):
        super().__init__()
        self.image = rain
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 750)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randint(2, 8)

    def update(self):
        """
        Update the position of the obstacle, moving it down the screen and resetting it if it goes off the screen.
        """
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.x = random.randrange(0, 750)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randint(2, 8)


# Function to initialize the game
def initGame():
    global allSprites, objects, obstacles, player, score, hitCounter
    allSprites = pygame.sprite.Group()
    objects = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player()
    allSprites.add(player)

    for i in range(10):
        obj = Object()
        allSprites.add(obj)
        objects.add(obj)

    for i in range(10):
        obs = Obstacle()
        allSprites.add(obs)
        obstacles.add(obs)

    score = 0
    hitCounter = 0


def saveHighScore(highScore):
    """
    Save the high score to a file.

    Args:
        highScore (int): The high score to be saved.
    """
    with open("highScore.txt", "w") as f:
        f.write(str(highScore))

    """
    Load the high score from a file.

    Returns:
        int: The high score loaded from the file.
    """
def loadHighScore():
    try:
        with open("highScore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


fontName = pygame.font.match_font("arial")


def drawText(surf, text, size, x, y):
    """
    Draw text on the screen at a specified position.

    Args:
        surf (pygame.Surface): The surface to draw on.
        text (str): The text to be displayed.
        size (int): The font size of the text.
        x (int): The x-coordinate of the text position.
        y (int): The y-coordinate of the text position.
    """
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, black)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurface, textRect)


def showHowToPlayScreen():
    """
    Display the "How to Play" screen with game instructions.
    """
    screen.fill(white)
    drawText(screen, "How to Play", 64, 400, 100)
    drawText(screen, "Catch the krakens and avoid the acid rain.", 22, 400, 250)
    drawText(screen, "If stormont got hit by acid 3 times, you lose.", 22, 400, 280)
    drawText(screen, "Use arrow keys to move.", 22, 400, 310)
    drawText(screen, "Press SPACE to start", 22, 400, 340)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def showGameOverScreen():
    global running
    screen.fill(white)
    drawText(screen, "Game Over", 64, 400, 100)
    drawText(screen, f"Score: {score}", 22, 400, 250)
    drawText(screen, f"High Score: {highScore}", 22, 400, 280)
    drawText(screen, "Press R to Restart or Q to Quit", 22, 400, 310)
    pygame.display.flip()
    gameOver.play()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    initGame()
                    waiting = False
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    exit()


# Load the high score at the start
highScore = loadHighScore()

# Show the "How to Play" screen
showHowToPlayScreen()

# Initialize the game
initGame()

# Game loop
running = True
while running:
    # Set the frame rate
    clock.tick(60)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    allSprites.update()

    # Check for collisions between the player and objects
    hits = pygame.sprite.spritecollide(player, objects, True)
    for hit in hits:
        score += 1
        if score > highScore:
            highScore = score
            saveHighScore(highScore)
        obj = Object()
        allSprites.add(obj)
        objects.add(obj)

    obsHits = pygame.sprite.spritecollide(player, obstacles, True)
    for hit in obsHits:
        hitCounter += 1
        hitSound.play()
        if hitCounter == 3:
            showGameOverScreen()
        obs = Obstacle()
        allSprites.add(obs)
        obstacles.add(obs)

    # Update the high score if necessary
    if score > highScore:
        highScore = score
        saveHighScore(highScore)

    # Draw everything on the screen
    screen.fill(white)
    allSprites.draw(screen)
    drawText(screen, f"Score: {score}", 18, 50, 10)
    drawText(screen, f"High Score: {highScore}", 18, 50, 30)
    drawText(screen, f"Hits: {hitCounter}", 18, 50, 50)

    pygame.display.update()

pygame.quit()
