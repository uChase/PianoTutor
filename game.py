import pygame
import sys
import threading
import midi

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
KEYBOARD_IMAGE_PATH = "imgs/keyboard.jpg"

MIDI_POSITIONS = {
    36: 0,  38: 1,  40: 2, 41: 3, 43: 4, 45: 5, 47: 6,
    48: 7,  50: 8,  52: 9, 53: 10, 55: 11, 57: 12, 59: 13,
    60: 14, 62: 15, 64: 16, 65: 17, 67: 18, 69: 19, 71: 20,
    72: 21, 74: 22, 76: 23, 77: 24, 79: 25, 81: 26, 83: 27,
    84: 28, 86: 29, 88: 30, 89: 31, 91: 32, 93: 33, 95: 34,
    96: 35
}


# Set up the display to windowed mode
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Load keyboard image
keyboard_image = pygame.image.load(KEYBOARD_IMAGE_PATH)
keyboard_image_height = screen_height // 4
keyboard_image = pygame.transform.scale(keyboard_image, (screen_width, keyboard_image_height))



def main():
    global screen, keyboard_image, keyboard_image_height, screen_width, screen_height 
    
    # Start the MIDI input thread
    midi_thread = threading.Thread(target=midi.getInput)
    midi_thread.daemon = True
    midi_thread.start()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                keyboard_image_height = screen_height // 4
                keyboard_image = pygame.transform.scale(keyboard_image, (screen_width, keyboard_image_height))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # print(f"Y coordinate: {y}")
                print(f"X coordinate: {x}")

        # Fill the background
        screen.fill(WHITE)

        # Draw the keyboard image at the bottom fourth of the screen
        screen.blit(keyboard_image, (0, screen_height - keyboard_image_height))

        # Highlight the pressed key if any
        if len(midi.current_midi_note) > 0:
            # Calculate the key width based on the current screen width
            key_width = screen_width / 35
            # Calculate the x position of the pressed key
            for note in midi.current_midi_note:
                if note in MIDI_POSITIONS:
                    key_index = MIDI_POSITIONS[note]
                    key_x = key_index * key_width 
                    pygame.draw.rect(screen, RED, (key_x + key_width * .05, screen_height - keyboard_image_height / 3, key_width - key_width * .05, keyboard_image_height / 2))
                else:
                    #it is a flat
                    key_index = MIDI_POSITIONS[note + 1]
                    key_x = (key_index * key_width) - key_width / 5
                    pygame.draw.rect(screen, RED, (key_x, screen_height - keyboard_image_height, key_width / 3, keyboard_image_height / 2))

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
