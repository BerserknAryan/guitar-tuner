import sounddevice as sd
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from tunings import TUNINGS


def set_tuning(self, category, tuning):
    self.current_tuning = category
    self.notes = TUNINGS[category][tuning]
    self.display_chord_buttons()


def display_chord_buttons(self):
    layout = BoxLayout(orientation='vertical')

    # Create buttons for each chord in the selected tuning
    for note in self.notes:
        btn = Button(text=note, size_hint_y=None, height=40)
        btn.bind(on_press=lambda x, n=note: self.play_chord(n))
        layout.add_widget(btn)

    # Create a Stop Tone button
    stop_btn = Button(text='Stop Tone', size_hint_y=None, height=40)
    stop_btn.bind(on_press=self.stop_tone)
    layout.add_widget(stop_btn)

    # Create a Back to Main Menu button
    back_btn = Button(text='Back to Main Menu', size_hint_y=None, height=40)
    back_btn.bind(on_press=self.return_to_main_menu)
    layout.add_widget(back_btn)

    # Clear the current widgets and add the new layout
    self.root.clear_widgets()
    self.root.add_widget(layout)


current_stream = None  # Global variable to keep track of the current sound stream


def play_tone(frequency, duration=1.0):
    global current_stream
    tone = generate_tone(frequency, duration)
    current_stream = sd.play(tone, samplerate=44100)  # Play the sound
    sd.wait()  # Wait until the sound has finished playing


def stop_tone():
    global current_stream
    if current_stream is not None:
        sd.stop()  # Stop the currently playing sound
        current_stream = None  # Reset the current stream


def return_to_main_menu(self):
    self.root.clear_widgets()  # Clear the current widgets
    self.root.add_widget(self.main_menu())  # Add the main menu back
