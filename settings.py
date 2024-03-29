# game options/settings
TITLE = "Jumpy!"
WIDTH = 900
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


TILESIZE = 64

NOTES = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 79]
LABELS = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5']
idxs_to_labels = {
    i:LABELS[i] for i in range(len(LABELS))
}