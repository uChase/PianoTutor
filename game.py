import pygame
import sys
import threading
import time
import midi
import fallingnotes
import loadsong


# Initialize Pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (237, 41, 57)
PINK = (131,56,236)

KEYBOARD_IMAGE_PATH = "imgs/keyboard.jpg"
font = pygame.font.Font(None, 36)



MIDI_POSITIONS = {
    36: 0,  38: 1,  40: 2, 41: 3, 43: 4, 45: 5, 47: 6,
    48: 7,  50: 8,  52: 9, 53: 10, 55: 11, 57: 12, 59: 13,
    60: 14, 62: 15, 64: 16, 65: 17, 67: 18, 69: 19, 71: 20,
    72: 21, 74: 22, 76: 23, 77: 24, 79: 25, 81: 26, 83: 27,
    84: 28, 86: 29, 88: 30, 89: 31, 91: 32, 93: 33, 95: 34,
    96: 35
}

FLATS_POSITIONS = {
    36: 0, 38: 1, 40: 2, 41: 0, 43: 1, 45: 1, 47: 2,
    48: 0, 50: 1, 52: 2, 53: 0, 55: 1, 57: 1, 59: 2,
    60: 0, 62: 1, 64: 2, 65: 0, 67: 1, 69: 1, 71: 2,
    72: 0, 74: 1, 76: 2, 77: 0, 79: 1, 81: 1, 83: 2,
    84: 0, 86: 1, 88: 2, 89: 0, 91: 1, 93: 1, 95: 2,
    96: 0
}



# Set up the display to windowed mode
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Piano Tutor")

FPS = 60
TIME_TO_HIT = 4
BEATS_PER_MINUTE = 60

# Load keyboard image
keyboard_image = pygame.image.load(KEYBOARD_IMAGE_PATH)
keyboard_image_height = screen_height // 4
keyboard_image = pygame.transform.scale(keyboard_image, (screen_width, keyboard_image_height))

note_speed = (screen_height - keyboard_image_height) / (TIME_TO_HIT)


def get_key_x_position(note, key_width):
    if note in MIDI_POSITIONS:
        key_index = MIDI_POSITIONS[note]
        key_x = key_index * key_width
    else:
        key_index = MIDI_POSITIONS[note + 1]
        key_x = (key_index * key_width) - key_width / 5
    return key_x




def hit_keys(notes):
    if len(notes) > 0:
            # Calculate the key width based on the current screen width
            key_width = screen_width / 35
            # Calculate the x position of the pressed key
            for note in notes:
                if note in MIDI_POSITIONS:
                    key_x = get_key_x_position(note, key_width)
                    pygame.draw.rect(screen, RED, (key_x + key_width * .05, screen_height - keyboard_image_height / 2.9, key_width - key_width * .05, keyboard_image_height / 2))
                    if FLATS_POSITIONS[note] == 0:
                        pygame.draw.rect(screen, RED, (key_x + key_width * .05, screen_height - keyboard_image_height, key_width - key_width * .05 - key_width * .42 , keyboard_image_height))
                    elif FLATS_POSITIONS[note] == 1:
                        if FLATS_POSITIONS[note + 2] == 1:
                            pygame.draw.rect(screen, RED, (key_x + key_width * .05 + key_width * .14, screen_height - keyboard_image_height, key_width - key_width * .05 - key_width * .32 , keyboard_image_height))
                        elif FLATS_POSITIONS[note - 2] == 1:
                            pygame.draw.rect(screen, RED, (key_x + key_width * .05 + key_width * .25, screen_height - keyboard_image_height, key_width - key_width * .05 - key_width * .38 , keyboard_image_height))
                        else:
                            pygame.draw.rect(screen, RED, (key_x + key_width * .05 + key_width * .16, screen_height - keyboard_image_height, key_width - key_width * .05 - key_width * .26 , keyboard_image_height))
                    elif FLATS_POSITIONS[note] == 2:
                        pygame.draw.rect(screen, RED, (key_x + key_width * .48, screen_height - keyboard_image_height, key_width - key_width * .05 - key_width * .42 , keyboard_image_height))
                   
                else:
                    #it is a flat
                    key_x = get_key_x_position(note, key_width)
                    if FLATS_POSITIONS[note + 1] == 1 and FLATS_POSITIONS[note - 1] == 1:
                        #middle
                        pygame.draw.rect(screen, PINK, (key_x - key_width * 0.05, screen_height - keyboard_image_height, key_width / 1.7, keyboard_image_height / 1.55))
                    elif FLATS_POSITIONS[note + 1] == 1:
                        #right
                        pygame.draw.rect(screen, PINK, (key_x - key_width * 0.2, screen_height - keyboard_image_height, key_width / 1.7, keyboard_image_height / 1.55))
                    else:
                        pygame.draw.rect(screen, PINK, (key_x + key_width * 0.12, screen_height - keyboard_image_height, key_width / 1.7, keyboard_image_height / 1.55))

                    # pygame.draw.rect(screen, PINK, (key_x, screen_height - keyboard_image_height, key_width / 3, keyboard_image_height / 2))

song_path = "music/test.json"
song_data = loadsong.load_song(song_path)

falling_notes = []

def spawn_notes(song_data):
    for hand in ['left_hand', 'right_hand']:
        for beat_index, beat in enumerate(song_data[hand]):

            key_width = screen_width / 35
            for note, duration, start_time in beat:
                note_x = get_key_x_position(note, key_width)
                note_y = - fallingnotes.calculateHeight(duration, note_speed, BEATS_PER_MINUTE) # Start at the top based on start time
                if note in MIDI_POSITIONS:
                    falling_note = fallingnotes.FallingNote(note, note_x, note_y, key_width, fallingnotes.calculateHeight(duration, note_speed, BEATS_PER_MINUTE), screen, hand)
                    falling_notes.append((falling_note, (beat_index + start_time) * 60 / BEATS_PER_MINUTE, duration * 60 / BEATS_PER_MINUTE))
                else:
                    falling_note = fallingnotes.FallingNote(note, note_x, note_y, key_width / 3, fallingnotes.calculateHeight(duration, note_speed, BEATS_PER_MINUTE), screen, hand)
                    falling_notes.append((falling_note, (beat_index + start_time) * 60 / BEATS_PER_MINUTE, duration * 60 / BEATS_PER_MINUTE))


    



def main():
    global screen, keyboard_image, keyboard_image_height, screen_width, screen_height, note_speed, falling_notes
    clock = pygame.time.Clock()
    
    start_ticks = pygame.time.get_ticks()

    started_song = False

    current_time = 0
    
    # Start the MIDI input thread
    midi_thread = threading.Thread(target=midi.getInput)
    midi_thread.daemon = True
    midi_thread.start()
    score = 0
    prev_midi_notes = []

    # Main loop
    while True:
        is_flash_pressed = False
        if len(midi.flash_pressed) != 0:
            is_flash_pressed = True

        delta_time = clock.get_time() / 1000.0  # Convert milliseconds to seconds

        if started_song:
            current_time = (pygame.time.get_ticks() - start_ticks) / 1000.0  # Convert to seconds


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                keyboard_image_height = screen_height // 4
                keyboard_image = pygame.transform.scale(keyboard_image, (screen_width, keyboard_image_height))
                note_speed = (screen_height - keyboard_image_height) / (TIME_TO_HIT)


        if not started_song and len(midi.current_midi_note) != 0 and midi.current_midi_note[0] == 60:
            spawn_notes(song_data)
            start_ticks = pygame.time.get_ticks()
            started_song = True
            midi.flash_pressed.clear()

        if started_song and 36 in midi.current_midi_note and 96 in midi.current_midi_note:
            started_song = False
            current_time = 0
            score = 0
            falling_notes = []

        # Fill the background
        screen.fill(WHITE)

        # Draw the keyboard image at the bottom fourth of the screen
        screen.blit(keyboard_image, (0, screen_height - keyboard_image_height))

                    

        # Draw the keys that are being pressed
        hit_keys(midi.current_midi_note)

        if prev_midi_notes != midi.current_midi_note:
            print(midi.current_midi_note)
            print(prev_midi_notes)

        for falling_note, start_time, duration in falling_notes:
            if current_time > start_time + duration + TIME_TO_HIT + 1.5:
                continue
            if start_time <= current_time:
                falling_note.fall(delta_time, note_speed)
                falling_note.draw()
                falling_note.decrease_and_delete(screen_height - keyboard_image_height)
                if (current_time ) + .3 > start_time + TIME_TO_HIT and current_time - .3 < start_time + TIME_TO_HIT and not falling_note.isHitCorrect:
                    #checks if note is hit on time
                    if falling_note.note in midi.flash_pressed:
                        falling_note.setIsHitCorrect()
                        score += 1
                        midi.flash_pressed.remove(falling_note.note)
                        falling_note.correctEffect()
                elif current_time  < start_time + duration + TIME_TO_HIT - .4 and current_time > start_time + TIME_TO_HIT and falling_note.isHitCorrect and falling_note.isReleasedCorrect:
                    #checks if released too early
                    if falling_note.note not in midi.current_midi_note:
                        score -= 1
                        falling_note.setIsReleasedIncorrect()
                        falling_note.released = True
                        falling_note.stopCorrectEffect()
                elif current_time < start_time + duration + TIME_TO_HIT + .3 and current_time - .4 < start_time + duration + TIME_TO_HIT and not falling_note.released and falling_note.isHitCorrect:
                    #checks if released on time
                    if falling_note.note not in midi.current_midi_note:
                        falling_note.released = True
                        falling_note.stopCorrectEffectGood()
                elif current_time > start_time + duration + TIME_TO_HIT + .3 and not falling_note.released and falling_note.isHitCorrect:
                    #checks if released too late
                    falling_note.stopCorrectEffect()
                    falling_note.released = True
                    score -= 1
                falling_note.update_particles(delta_time)
        if is_flash_pressed and midi.flash_pressed != [] and started_song:
            score -= len(midi.flash_pressed)
                


        
        time_text = font.render(f"Time: {current_time:.2f}s", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(time_text, (screen_width - time_text.get_width() - 10, 10))
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 50))

        


        # Update the display
        pygame.display.flip()
        clock.tick(FPS)
        prev_midi_notes = (midi.current_midi_note)
        if is_flash_pressed:
            midi.flash_pressed = []

if __name__ == "__main__":
    main()
