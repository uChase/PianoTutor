import mido

# Mapping of MIDI note numbers to note names
NOTE_NAMES = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

def get_note_name(note_number):
    """Convert MIDI note number to note name."""
    octave = (note_number // 12) - 1
    note_name = NOTE_NAMES[note_number % 12]
    return f"{note_name}{octave}"

def midi_input_callback(message):
    """Callback function to handle incoming MIDI messages."""
    if message.type == 'note_on' or message.type == 'note_off':
        note_name = get_note_name(message.note)
        if message.type == 'note_on' and message.velocity > 0:
            print(f"Note on: {note_name} (velocity: {message.velocity})")
        else:
            print(f"Note off: {note_name}")

def list_midi_ports():
    """List all available MIDI input ports."""
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(f"  - {port}")

def main():
    list_midi_ports()
    
    # Replace 'YOUR_MIDI_DEVICE_NAME' with your actual MIDI device name
    port_name = 'USB MIDI Interface'
    try:
        with mido.open_input(port_name) as inport:
            print(f"Listening on {port_name}...")
            for message in inport:
                midi_input_callback(message)
    except IOError as e:
        print(f"Could not open port {port_name}: {e}")

if __name__ == "__main__":
    main()
