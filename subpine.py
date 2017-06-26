import pygame, sys, time, datetime, obd, math
from pygame.locals import *
from obd import OBDStatus

PI = 3.141592653

port = ""
baud = 115200
protocol = "5"

connection = None

afrString = "N/A"
lpkString = "N/A"

curRpm = 0
curMaxRpm = 0
maxRpm = 7000.0
redRpm = 6300.0

curAfr = 0
maxAfr = 18.0
redAfr = 16.0

sumLps = 0.0

firstKm = True
firstKmReading = 0.0
lastKmReading = 0.0

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

def new_rpm(r):
    global curRpm
    global curMaxRpm

    curRpm = r.value.magnitude
    if curRpm > curMaxRpm:
        curMaxRpm = curRpm

def new_lambda(r):
    global curAfr

    curAfr = r.value.magnitude / 14.7

def new_distancetraveled(r):
    global firstKm
    global firstKmReading
    global lastKmReading

    if firstKm:
        firstKmReading = r.value.magnitude
        firstKm = False
    else:
        lastKmReading = r.value.magnitude

def new_fuelrate(r):
    global lpkString
    global sumLps

    sumLps += r.value.magnitude / 3600  # (lph to lps)
    deltakm = lastKmReading - firstKmReading
    lpkString = str(sumLps / deltakm * 100)

def connect(p, b, pr):
    global connection

    s = "Unknown"

    try:
        connection = obd.Async(p, b, pr)
        connection.watch(obd.commands.RPM, callback=new_rpm)
        connection.watch(obd.commands.O2_S1_WR_VOLTAGE, callback=new_lambda)
        connection.watch(obd.commands.FUEL_RATE, callback=new_fuelrate)
        connection.watch(obd.commands.DISTANCE_SINCE_DTC_CLEAR, callback=new_distancetraveled)
        connection.start()

        s = "Connected"
    except:
        s = "Not connected"

    return s

def valueToRadians(cur, max):
    perc = cur / max
    gauge_move = 270 * perc
    return math.radians(gauge_move)

def drawGauge(maxv, redv, curv, title, curm=None):
    surface = pygame.Surface((200, 200))
    surface.fill((0, 0, 0))
    surface.set_colorkey((0, 0, 0))

    pygame.draw.arc(surface, WHITE, (0, 0, 200, 200), math.radians(0), valueToRadians(redv, maxv), 2)
    pygame.draw.arc(surface, RED, (0, 0, 200, 200), valueToRadians(redv, maxv), math.radians(270), 2)
    pygame.draw.arc(surface, GREEN, (0, 0, 200, 200), math.radians(0), valueToRadians(curv, maxv), 2)

    surface = pygame.transform.rotozoom(surface, -45, 1)
    surface = pygame.transform.flip(surface, True, False)

    curcolor = RED if curv >= redv else WHITE
    largefont = pygame.font.Font(None, 60)
    largetext = largefont.render(str(curv), 1, curcolor)
    surface.blit(largetext, (surface.get_width() / 2 - largetext.get_width() / 2,
                             (surface.get_height() / 2 - largetext.get_height() / 2) - 10))
    largetext = largefont.render(title, 1, curcolor)
    surface.blit(largetext, (surface.get_width() / 2 - largetext.get_width() / 2,
                             (surface.get_height() / 2 - largetext.get_height() / 2) + 60))

    if curm is not None:
        smallerfont = pygame.font.Font(None, 25)
        smallertext = smallerfont.render("Max: " + str(int(curm)), 1, (255, 255, 255))
        surface.blit(smallertext, (surface.get_width() / 2 - smallertext.get_width() / 2,
                             (surface.get_height() / 2 - smallertext.get_height() / 2) + 25))

    return surface

def main():
    pygame.init()
    clock = pygame.time.Clock()

    doConnect = True
    lastDoConnect = time.time()

    # Set up the screen
    displayInfo = pygame.display.Info()
    windowWidth = displayInfo.current_w
    windowHeight = displayInfo.current_h

    DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN, 16)
    pygame.mouse.set_visible(0)
    pygame.display.set_caption('SubPINE')

    # Main loop
    while True:
        status = "Not connected"
        if doConnect:
            doConnect = False
            lastDoConnect = time.time()
            if connection is None:
                status = connect(port, baud, protocol)
            elif connection.status() == OBDStatus.NOT_CONNECTED:
                status = connect(port, baud, protocol)

        if (time.time() - lastDoConnect) > 5:
            doConnect = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_x:
                return

        # Draw the title
        black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
        black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
        DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

        curHeight = 0

        # RPM
        DISPLAYSURF.blit(drawGauge(maxRpm, redRpm, curRpm, "RPM", curMaxRpm), (0, 0))

        # AFR
        DISPLAYSURF.blit(drawGauge(maxAfr, redAfr, curAfr, "AFR", None), (0, 200))

        font = pygame.font.Font(None, 60)
        afrText = font.render("AFR: " + str(afrString), 1, RED)
        DISPLAYSURF.blit(afrText, (0, curHeight))
        curHeight += afrText.get_height()

        # Fuel rate
        font = pygame.font.Font(None, 60)
        lpkText = font.render("L/100km: " + str(lpkString), 1, RED)
        DISPLAYSURF.blit(lpkText, (0, curHeight))
        curHeight += lpkText.get_height()

        # Status
        font = pygame.font.Font(None, 40)
        text = font.render(status, 1, CYAN)
        pygame.draw.line(DISPLAYSURF, GREEN, [1, DISPLAYSURF.get_height() - text.get_height()],
                         [DISPLAYSURF.get_width(), DISPLAYSURF.get_height() - text.get_height()], 1)
        DISPLAYSURF.blit(text, (1, DISPLAYSURF.get_height() - text.get_height()))

        # FPS
        clock.tick()
        font = pygame.font.Font(None, 40)
        text = font.render("{0:.2f} fps".format(clock.get_fps()), 1, CYAN)
        DISPLAYSURF.blit(text, (DISPLAYSURF.get_width() - text.get_width(),
                                DISPLAYSURF.get_height() - text.get_height()))

        pygame.display.update()

    if connection is not None:
        connection.close()
    sys.exit()

if __name__ == "__main__":
    main()
