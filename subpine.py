import pygame, sys, time, datetime, obd
from pygame.locals import *
from obd import OBDStatus

port = ""
baud = 115200
protocol = "5"

connection = None

rpmString = "N/A"

def new_rpm(r):
    global rpmString
    rpmString = str(r.value.magnitude)

def connect(p, b, pr):
    global connection
    s = "Unknown"

    try:
        connection = obd.Async(p, b, pr)
        connection.watch(obd.commands.RPM, callback=new_rpm)
        connection.start()

        s = "Connected"
    except:
        s = "Not connected"

    return s

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    doConnect = True
    lastDoConnect = time.time()

    # Set up the screen

    DISPLAYSURF = pygame.display.set_mode((800, 480), 0, 16)
    pygame.mouse.set_visible(0)
    pygame.display.set_caption('SubPINE')

    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)

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

        if (time.time() - lastDoConnect) > 2:
            doConnect = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        currentime = datetime.datetime.time(datetime.datetime.now())

        # Draw the title
        black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
        black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
        DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

        font = pygame.font.Font(None, 60)
        text = font.render("RPM: " + str(rpmString), 1, RED)

        DISPLAYSURF.blit(text, (0, 0))

        # textstring = "N/A"
        # if connection is not None:
        #     try:
        #         obdvalue1 = connection.query(obd.commands.O2_S1_WR_VOLTAGE)
        #         textstring = obdvalue1.value.magnitude / 14.7
        #     except:
        #         connection.close()
        # font = pygame.font.Font(None, 60)
        # text = font.render("AFR: " + str(textstring), 1, RED)
        # DISPLAYSURF.blit(text, (0, 60))

        # Draw Lines

        # pygame.draw.line(DISPLAYSURF, GREEN, [5, 140], [DISPLAYSURF.get_width()-5, 140], 1)

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
