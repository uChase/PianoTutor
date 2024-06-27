import pygame
import sys
import random
import threading
import midi

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 150
STAFF_SPACING = 20
NOTE_RADIUS = 10

# Staff line positions
TREBLE_CLEF_Y = MARGIN
BASS_CLEF_Y = TREBLE_CLEF_Y + 200

score = 0

# MIDI note numbers for C2 to C7
NOTE_RANGE = list(range(36, 96))
MIDI_POSITIONS = {
    36: 'C2', 37: 'D2b', 38: 'D2', 39: 'E2b', 40: 'E2', 41: 'F2', 42: 'G2b', 43: 'G2', 44: 'A2b', 45: 'A2', 46: 'B2b', 47: 'B2',
    48: 'C3', 49: 'D3b', 50: 'D3', 51: 'E3b', 52: 'E3', 53: 'F3', 54: 'G3b', 55: 'G3', 56: 'A3b', 57: 'A3', 58: 'B3b', 59: 'B3',
    60: 'C4', 61: 'D4b', 62: 'D4', 63: 'E4b', 64: 'E4', 65: 'F4', 66: 'G4b', 67: 'G4', 68: 'A4b', 69: 'A4', 70: 'B4b', 71: 'B4',
    72: 'C5', 73: 'D5b', 74: 'D5', 75: 'E5b', 76: 'E5', 77: 'F5', 78: 'G5b', 79: 'G5', 80: 'A5b', 81: 'A5', 82: 'B5b', 83: 'B5',
    84: 'C6', 85: 'D6b', 86: 'D6', 87: 'E6b', 88: 'E6', 89: 'F6', 90: 'G6b', 91: 'G6', 92: 'A6b', 93: 'A6', 94: 'B6b', 95: 'B6',
    96: 'C7'
}


# Note positions on the staves
NOTE_POSITIONS = {
    'C2': BASS_CLEF_Y + 4 * STAFF_SPACING + 10,
    'D2': BASS_CLEF_Y + 4 * STAFF_SPACING,
    'E2': BASS_CLEF_Y + 3 * STAFF_SPACING + 10,
    'F2': BASS_CLEF_Y + 3 * STAFF_SPACING,
    'G2': BASS_CLEF_Y + 2 * STAFF_SPACING + 10,
    'A2': BASS_CLEF_Y + 2 * STAFF_SPACING,
    'B2': BASS_CLEF_Y + STAFF_SPACING + 10,
    'C3': BASS_CLEF_Y + STAFF_SPACING,
    'D3': BASS_CLEF_Y + 10,
    'E3': BASS_CLEF_Y,
    'F3': BASS_CLEF_Y - STAFF_SPACING + 10,
    'G3': BASS_CLEF_Y - STAFF_SPACING,
    'A3': BASS_CLEF_Y - 2 * STAFF_SPACING + 10,
    'B3': BASS_CLEF_Y - 2 * STAFF_SPACING,
    'C4': TREBLE_CLEF_Y + 4 * STAFF_SPACING + 10,
    'D4': TREBLE_CLEF_Y + 4 * STAFF_SPACING,
    'E4': TREBLE_CLEF_Y + 3 * STAFF_SPACING + 10,
    'F4': TREBLE_CLEF_Y + 3 * STAFF_SPACING,
    'G4': TREBLE_CLEF_Y + 2 * STAFF_SPACING + 10,
    'A4': TREBLE_CLEF_Y + 2 * STAFF_SPACING,
    'B4': TREBLE_CLEF_Y + STAFF_SPACING + 10,
    'C5': TREBLE_CLEF_Y + STAFF_SPACING,
    'D5': TREBLE_CLEF_Y + 10,
    'E5': TREBLE_CLEF_Y,
    'F5': TREBLE_CLEF_Y - STAFF_SPACING + 10,
    'G5': TREBLE_CLEF_Y - STAFF_SPACING,
    'A5': TREBLE_CLEF_Y - 2 * STAFF_SPACING + 10,
    'B5': TREBLE_CLEF_Y - 2 * STAFF_SPACING,
    'C6': TREBLE_CLEF_Y - 3 * STAFF_SPACING + 10,
    'D6': TREBLE_CLEF_Y - 3 * STAFF_SPACING,
    'E6': TREBLE_CLEF_Y - 4 * STAFF_SPACING + 10,
    'F6': TREBLE_CLEF_Y - 4 * STAFF_SPACING,
    'G6': TREBLE_CLEF_Y - 5 * STAFF_SPACING + 10,
    'A6': TREBLE_CLEF_Y - 5 * STAFF_SPACING,
    'B6': TREBLE_CLEF_Y - 6 * STAFF_SPACING + 10,
    'C7': TREBLE_CLEF_Y - 6 * STAFF_SPACING
}




# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Piano Sheet Music")

# Load clef images
treble_clef = pygame.image.load("imgs/treble.png")
bass_clef = pygame.image.load("imgs/base.png")
flat = pygame.image.load("imgs/flat.png")

def draw_staff(y_pos):
    """Draws a five-line staff at the given y position."""
    for i in range(5):
        pygame.draw.line(screen, BLACK, (MARGIN, y_pos + i * STAFF_SPACING), 
                         (SCREEN_WIDTH - MARGIN, y_pos + i * STAFF_SPACING), 2)

def draw_clefs():
    """Draws the treble and bass clefs."""
    screen.blit(treble_clef, (MARGIN - 30, TREBLE_CLEF_Y - 20))
    screen.blit(bass_clef, (MARGIN - 30, BASS_CLEF_Y + 10))

def draw_note_with_ledger_lines(note_number=60, player_note=False):
    """Draws a note and ledger lines if the note is outside the staff."""
    note_name = MIDI_POSITIONS[note_number]
    note_y = NOTE_POSITIONS[note_name.split('b')[0]]
    note_x = MARGIN + 100

    if note_number >= 60:
        note_y += 10
    else:
        note_y += 30

    # Draw the note
    if player_note:
        pygame.draw.circle(screen, (255, 0, 0), (note_x, note_y), NOTE_RADIUS)
    else:
        pygame.draw.circle(screen, BLACK, (note_x, note_y), NOTE_RADIUS)
    if 'b' in note_name:
        screen.blit(flat, (note_x - 25, note_y - 5 ))

    # Draw ledger lines if necessary
    if note_number <= 59:  # Notes in bass clef
        if note_y < BASS_CLEF_Y or note_y > BASS_CLEF_Y + 4 * STAFF_SPACING:
            if note_y < BASS_CLEF_Y:
                # Draw ledger lines above the bass staff
                for y in range(note_y, BASS_CLEF_Y, STAFF_SPACING):
                    pygame.draw.line(screen, BLACK, (note_x - 15, y - 10), (note_x + 15, y - 10), 2)
            else:
                # Draw ledger lines below the bass staff
                for y in range(BASS_CLEF_Y + 4 * STAFF_SPACING, note_y + STAFF_SPACING, STAFF_SPACING):
                    pygame.draw.line(screen, BLACK, (note_x - 15, y), (note_x + 15, y), 2)
    else:  # Notes in treble clef
        if note_y < TREBLE_CLEF_Y or note_y > TREBLE_CLEF_Y + 4 * STAFF_SPACING:
            if note_y < TREBLE_CLEF_Y:
                # Draw ledger lines above the treble staff
                if (note_y / 10) % 2 == 0:
                    for y in range(note_y, TREBLE_CLEF_Y, STAFF_SPACING):
                        pygame.draw.line(screen, BLACK, (note_x - 15, y - 10 ), (note_x + 15, y - 10 ), 2)
                else:
                    for y in range(note_y + 10, TREBLE_CLEF_Y, STAFF_SPACING):
                        pygame.draw.line(screen, BLACK, (note_x - 15, y - 10 ), (note_x + 15, y - 10 ), 2)
            else:
                # Draw ledger lines below the treble staff
                for y in range(TREBLE_CLEF_Y + 4 * STAFF_SPACING, note_y + STAFF_SPACING, STAFF_SPACING):
                    pygame.draw.line(screen, BLACK, (note_x - 15, y), (note_x + 15, y), 2)

def genRandomNote():
    return random.choice(NOTE_RANGE)

def main():
    # Load clef images (scaled for the sheet music)
    global treble_clef, bass_clef, flat, score
    treble_clef = pygame.transform.scale(treble_clef, (60, 120))
    bass_clef = pygame.transform.scale(bass_clef, (60, 60))
    flat = pygame.transform.scale(flat, (14, 14))
    
    font = pygame.font.Font(None, 36)
    randNote = genRandomNote()



    # Start the MIDI input thread
    midi_thread = threading.Thread(target=midi.getInput)
    midi_thread.daemon = True
    midi_thread.start()
    already_subtracted = False
    resetPoints = False

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the background
        screen.fill(WHITE)

        # Draw the staves
        draw_staff(TREBLE_CLEF_Y)
        draw_staff(BASS_CLEF_Y)

        # Draw the clefs
        draw_clefs()
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 10))


        if randNote in midi.current_midi_note:
            if not already_subtracted:
                score += 1
            randNote = genRandomNote()
            already_subtracted = False
            resetPoints = True
        elif len(midi.current_midi_note) > 0 and not already_subtracted and not resetPoints:
            score -= 1
            already_subtracted = True
        elif len(midi.current_midi_note) == 0:
            resetPoints = False

        if midi.current_midi_note is not None and len(midi.current_midi_note) > 0:
            for note in midi.current_midi_note:
                draw_note_with_ledger_lines(note, True)
        
        draw_note_with_ledger_lines(randNote)

        

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
