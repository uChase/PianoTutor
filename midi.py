import mido
import threading

# Shared state for MIDI notes
current_midi_note = []
flash_pressed = []

NOTE_NAMES = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

def list_midi_ports():
    """List all available MIDI input ports."""
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(f"  - {port}")
    return port


def get_note_name(note_number):
    """Convert MIDI note number to note name."""
    octave = (note_number // 12) - 1
    note_name = NOTE_NAMES[note_number % 12]
    return f"{note_name}{octave}"


def midi_input_callback(message):
    global current_midi_note, flash_pressed
    if message.type == 'note_on' and message.velocity > 0:
        print(f"Received MIDI note: {get_note_name(message.note)}")
        current_midi_note.append(message.note)
        flash_pressed.append(message.note)
    elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
        current_midi_note.remove(message.note)

def getInput():

    port_name = list_midi_ports()


    try:
        with mido.open_input(port_name) as inport:
            print(f"Listening on {port_name}...")
            for message in inport:
                midi_input_callback(message)
    except IOError as e:
        print(f"Could not open port {port_name}: {e}")
