import pygame, random, time, sys

# Initialisierung von Pygame
pygame.init()

# Musik einrichten
pygame.mixer.music.load("assets/music.mp3")
# -1 besagt dass Song sich ständig wiederholt, 0.0 ist der zeitliche Startpunkt der Musik
pygame.mixer.music.play(-1, 0.0)

# Bildschirmdaten
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
bg_color = (233, 150, 122)
fps = 60
clock = pygame.time.Clock()

# Titel, Icon und Startbildschirm Bilder
pygame.display.set_caption("Hide from the Bride")
icon = pygame.image.load("assets/loveicon.png")
start_img = pygame.image.load("assets/bridestart.png")
start_img2 = pygame.image.load("assets/groomstart.png")
pygame.display.set_icon(icon)

# Font Match durchsucht Anwendersystem auf größte Übereinstimmung zum Font Namen
# Dies verhindert, dass fonts im Spiel festgelegt werden, die der Anwender nicht
# besitzt
font_name = pygame.font.match_font("arial")


# Character Class als Spielerklasse
class Character:
    # Konstruktor
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("assets/player.png")
        self.speed = speed
        # Kreiert eine rechteckige Begrenzung um img Koordinaten
        # Wird später für Bewegung und Kollisionserkennung benötigt
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # Funktion für Bewegung
    def move(self):

        # Zuweisung der Bewegungsvariablen, wie sehr sich Rectangle auf x und y Achse bewegt
        # Change Variablen helfen Bewegung vorherzusehen für Kollisionserkennung
        # Die rectangle Position wird verändert, da diese an das image gebunden ist
        change_x = 0
        change_y = 0

        # if Abfragen zur Bewegungsermittlung
        if moving_left:
            change_x = -self.speed
        if moving_right:
            change_x = self.speed
        if moving_up:
            change_y = -self.speed
        if moving_down:
            change_y = self.speed

        # Update der rectangle Koordinaten und somit der Character Position
        self.rect.x += change_x
        self.rect.y += change_y

        # Bildschirmbegrenzung für den Spieler
        # Positive Werte abzüglich Icon Breite
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 536:
            self.rect.x = 536

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= 536:
            self.rect.y = 536

    def draw(self):
        # Zeichnen eines Objekts der Klasse Character auf der Bildschirmfläche
        screen.blit(self.image, self.rect)


# Gegnerklasse
class Enemy:

    # Konstruktor
    def __init__(self, x, y):
        self.x = random.randint(0, 300)
        self.y = random.randint(32, 300)
        self.image = pygame.image.load("assets/bride.png")
        self.enemy_change_x = 0
        self.enemy_change_y = 0
        # Kreiert eine rechteckige Begrenzung um img Koordinaten
        # Wird später für Bewegung und Kollisionserkennung benötigt
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        # Anpassung von Gegner change Parametern zur Bewegung
        self.enemy_change_x += random.uniform(-1.5, 1.5)
        self.enemy_change_y += random.uniform(-1.5, 1.5)
        # Update der rectangle Koordinaten und somit der Character Position
        self.rect.x += self.enemy_change_x
        self.rect.y += self.enemy_change_y

        # Bildschirmbegrenzung für den Gegner
        # Positive Werte abzüglich Icon Breite
        if self.rect.x <= 0:
            self.enemy_change_x = 0.2
        elif self.rect.x >= 536:
            self.enemy_change_x = -0.2

        if self.rect.y <= 0:
            self.enemy_change_y = 0.2
        elif self.rect.y >= 536:
            self.enemy_change_y = -0.2

    def draw(self):
        # Zeichnen eines Objekts der Klasse Enemy auf den Bildschirm
        screen.blit(self.image, self.rect)


# surf = Oberfläche, text = font, size = fontsize, x und y Koordindaten des Textes
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # True "schaltet" Anti Aliasing an, sodass Schrift weniger "pixelig" aussieht
    text_surface = font.render(text, True, (255, 255, 255))
    # Bilden eines "unsichtbaren" Rechtecks zur Positionierung des Textes
    text_rect = text_surface.get_rect()
    # Mitte des Rechtecks bilden die x y Koordinaten
    text_rect.center = (x, y)
    # Zeichnen der Textfläche an Koordinaten des text_rect auf Bildschirm
    surf.blit(text_surface, text_rect)


# -------- Start Funktion ----------
def start():
    while True:
        # Zeichne den Titelbildschirm
        draw_title()
        if not mouse_wait():  # Warten auf den Mausklick
            break  # Beendet das Spiel, wenn der Spieler die Escape-Taste drückt
            # Da Loop unterbrochen wird

        # führe das Spiel aus
        # Wenn main_game True zurückgibt, wird der Endscreen gezeichnet
        # Gibt main_game False zurück, wird der Startscreen gezeichnet
        if not main_game():
            # Continue lässt while loop von oben starten
            continue

        # Zeichnet den Endbildschirm
        draw_end_screen()
        if not mouse_wait():  # Warten auf den Mausklick
            break  # Beendet das Spiel, wenn der Spieler die Escape-Taste drückt


# -------- Maustasten Funktion ----------
def mouse_wait():
    # gibt FALSE zurück, wenn der Spieler das Spiel verlassen möchte

    # Warten auf einen Mausklick
    while True:
        # Erkennung Tastatur-Maus-Ereignisse
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 1 entspricht der linken Maustaste
                    return True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# -------- Startscreen Funktion ----------
def draw_title():
    global screen, bg_color, start_img, start_img2

    screen.fill((bg_color))
    draw_text(screen, "Hide from the Bride", 72, 300, 228)
    draw_text(screen, "-a case of wedding cold feet-", 48, 300, 300)
    draw_text(screen, "Use Arrow Keys to move", 24, 300, 400)
    draw_text(screen, "Click anywhere to start", 24, 300, 448)
    draw_text(screen, "A game with love by Dennis Schallenberg 2022", 18, 300, 580)
    screen.blit(start_img, (178, 56))
    screen.blit(start_img2, (306, 56))

    pygame.display.update()


# -------- Endscreen Funktion ----------
def draw_end_screen():
    global screen, start_img, start_img2

    screen.fill((bg_color))
    draw_text(screen, "Game Over", 72, 300, 228)
    draw_text(screen, "Try again?", 48, 300, 300)
    draw_text(screen, "Click anywhere to return to main menu", 24, 300, 400)
    screen.blit(start_img, (178, 56))
    screen.blit(start_img2, (306, 56))

    pygame.display.update()


# -------- Main Game -----------
def main_game():
    global moving_left, moving_right, moving_up, moving_down, new_time
    # Score Variablen müssen hier bestimmt werden, da ansonst ab Start Bildschirm gezählt wird
    f = open("score/score.txt", "r")
    high_scores = [float(score) for score in f.read().split(",")]
    f.close()
    now = time.time()
    new_time = 0

    # Bewegungsvariablen
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    # Erzeugung eines Objekts Player der Klasse Character
    # 300, 500 = x und y Koordinaten, 5 = Geschwindigkeit, die sich der Spieler bei jeder Iteration per Testendruck bewegt
    player = Character(300, 500, 5)
    # Erzeugung eines Objekts bride der Klasse Enemy
    bride = Enemy((random.randint(0, 600)), (random.randint(0, 600)))

    while True:
        # Limitierung der Bildwiederholungsrate
        clock.tick(fps)
        # Festlegung der Hintergrundfarbe mittels RGB Code
        screen.fill((bg_color))

        # Zeichnen eines Objekts der Klasse Character auf die Bildschirmfläche
        # Spieler
        player.draw()
        player.move()

        bride.draw()
        bride.move()

        now_time = time.time() - now
        draw_text(screen, ("Score: ") + str(int(now_time)), 32, 300, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Beendet das Spiel, nachdem die X-Taste gedrückt wurde
                pygame.quit()
                sys.exit()

            # Wenn Taste gedrückt wird, überprüfe Richtung
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_DOWN:
                    moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_UP:
                    moving_up = False
                if event.key == pygame.K_DOWN:
                    moving_down = False
                # Weitere Spielabbruchbedingung
                if event.key == pygame.K_ESCAPE:
                    return False  # zurück zum Start(). Sagt start(), dass der Spieler das Spiel verlassen hat

        # Kollisionserkennung
        # Zu Spieler- und Gegnerkoordinaten wird je ein Vektor gelegt a und b
        # Ist der Abstand beider Objekte kleiner als der Kollisionsradius r
        # Wird Kollision erkannt
        r = 64
        a = pygame.math.Vector2(player.rect.x, player.rect.y)
        b = pygame.math.Vector2(bride.rect.x, bride.rect.y)

        # distance_to berechnet euklidische Distanz zwischen den Vektoren
        if b.distance_to(a) < r:
            score = time.time() - now

            for index in range(len(high_scores)):
                if score > high_scores[index]:
                    # Wenn der neue score höher als einer der Listen Scores ist
                    # Nimmt er dessen index ein
                    # andernfalls wird er an die Liste angehangen
                    high_scores.insert(index, score)
                    break  # exit for loop

            # Speichert den Score in die txt Datei
            f = open("score/score.txt", "w")

            # "{},{},{}".format(high_scores[0], high_scores[1], high_scores[2]) erstellt einen String
            # der folgendermaßen ausssieht "300.0,200.0,130.0"
            # Schreibe den String in die txt Datei und schließe die Datei
            f.write("{},{},{}".format(high_scores[0], high_scores[1], high_scores[2]))
            f.close()

            # Teilt start() mit, dass der Spieler das Spiel beendet hat und der Endbildschirm gezeichnet werden muss
            return True  # zurück zum Start()

        pygame.display.update()


start()
