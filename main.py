from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform
from plyer import vibrator
from tunings import TUNINGS
from pitch import PITCH
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# Define the constant
BACK_TO_MAIN_MENU_TEXT = "Back to Main Menu"


class GuitarTunerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pitch = PITCH["default"]
        self.current_tuning = "Standard_tuning"
        self.notes = TUNINGS[self.current_tuning]["E-A-D-G-B-E"]

    def build(self):
        return self.main_menu()

    def main_menu(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Tuning', on_press=self.select_tuning))
        layout.add_widget(Button(text='Pitch', on_press=self.adjust_pitch))
        layout.add_widget(Button(text='More Info', on_press=self.show_info))
        layout.add_widget(Button(text='Exit', on_press=self.stop))
        return layout

    def select_tuning(self, instance):
        content = BoxLayout(orientation='vertical')
        for category in TUNINGS.keys():
            btn = Button(text=category, size_hint_y=None, height=40)
            btn.bind(on_press=self.show_tuning_options)
            content.add_widget(btn)
        popup = Popup(title='Select Tuning', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def show_tuning_options(self, instance):
        tuning_category = instance.text
        content = GridLayout(cols=1, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))  # Allow the layout to grow

        for tuning, notes in TUNINGS[tuning_category].items():
            btn = Button(text=tuning, size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, tuning=tuning: self.set_tuning(tuning_category, tuning))
            content.add_widget(btn)

        # Create a ScrollView to allow scrolling through the tuning options
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))  # Adjust size as needed
        scroll_view.add_widget(content)

        # Add a back button to return to the main menu
        back_btn = Button(text=BACK_TO_MAIN_MENU_TEXT, size_hint_y=None, height=40)
        back_btn.bind(on_press=lambda x: self.return_to_main_menu())

        # Create a vertical layout to hold the scroll view and back button
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(scroll_view)
        layout.add_widget(back_btn)

        popup = Popup(title=f'Select {tuning_category} Tuning', content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def set_tuning(self, category, tuning):
        self.current_tuning = category
        self.notes = TUNINGS[category][tuning]
        self.tuning_screen()
        self.update_chord_buttons()

    def adjust_pitch(self, instance):
        content = BoxLayout(orientation='vertical')
        up_btn = Button(text='Increase', on_press=self.increase_pitch, on_release=self.stop_vibration)
        down_btn = Button(text='Decrease', on_press=self.decrease_pitch, on_release=self.stop_vibration)
        current_pitch_label = Label(text=f'Current Pitch: {self.pitch}Hz')

        # Add a back button to return to the main menu
        back_btn = Button(text='Back to Main Menu', on_press=lambda x: self.return_to_main_menu())

        content.add_widget(up_btn)
        content.add_widget(current_pitch_label)
        content.add_widget(down_btn)
        content.add_widget(back_btn)  # Add the back button
        popup = Popup(title='Adjust Pitch', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def increase_pitch(self, instance):
        if self.pitch < 528:
            self.pitch += 1
        self.update_pitch_label()  # Update the label to show the new pitch
        self.vibrate()

    def decrease_pitch(self, instance):
        if self.pitch > 285:
            self.pitch -= 1
        self.update_pitch_label()  # Update the label to show the new pitch
        self.vibrate()

    def update_pitch_label(self):
        # This method should update the label in the popup to reflect the current pitch
        # You may need to store a reference to the label when creating it in adjust_pitch
        self.update_pitch_label = self(text=f'Current Pitch: {self.pitch}Hz')

    def return_to_main_menu(self):
        self.root.clear_widgets()  # Clear the current widgets
        self.root.add_widget(self.main_menu())  # Add the main menu back

    @staticmethod
    def vibrate():
        if platform == 'android':
            vibrator.vibrate(0.1)

    def stop_vibration(self, instance):
        pass

    def tuning_screen(self):
        layout = BoxLayout(orientation='vertical')
        for note in self.notes:
            btn = Button(text=note, on_press=lambda x, n=note: self.play_tone(n))
            layout.add_widget(btn)
        layout.add_widget(Button(text='Stop', on_press=lambda x: self.stop_tone()))
        layout.add_widget(Button(text=BACK_TO_MAIN_MENU_TEXT,
                                 on_press=lambda x: self.root.clear_widgets() or self.root.add_widget(
                                     self.main_menu())))
        self.root.clear_widgets()
        self.root.add_widget(layout)

    @staticmethod
    def show_info():
        popup = Popup(title='Info', content=Label(text='Simple Guitar Tuner App'), size_hint=(0.6, 0.4))
        popup.open()

    def stop(self, instance=None):
        App.get_running_app().stop()


if __name__ == '__main__':
    GuitarTunerApp().run()
