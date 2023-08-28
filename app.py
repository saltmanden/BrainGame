import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import random

kivy.require('1.11.1')

class BrainGameApp(App):
    def build(self):
        self.streak_count = 0
        self.layout = BoxLayout(orientation='vertical')
        self.current_page = None  # To track the current page
        
        self.input_box = BoxLayout(orientation='horizontal')
        self.input_field = TextInput(hint_text='Enter number of digits', multiline=False, input_filter='int')
        numeric_keypad = self.create_numeric_keypad()
        go_button = Button(text='Go', on_press=self.show_sequence)
        
        self.input_box.add_widget(self.input_field)
        self.input_box.add_widget(numeric_keypad)
        
        input_controls_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        input_controls_box.add_widget(go_button)
        self.input_box.add_widget(input_controls_box)
        
        self.layout.add_widget(self.input_box)
        self.display_area = BoxLayout()
        self.layout.add_widget(self.display_area)
        
        return self.layout
    
    def generate_sequence(self, length):
        # Generate a random sequence of digits (for example, 1-9)
        return [random.randint(1, 9) for _ in range(length)]
        
    def display_sequence(self):
        self.display_area.clear_widgets()
        
        seq_label = Label(text=','.join(map(str, self.sequence)))
        self.display_area.add_widget(seq_label)

            
    def show_sequence(self, instance):
        try:
            self.num_digits = int(self.input_field.text)
            self.sequence = self.generate_sequence(self.num_digits)
            self.layout.remove_widget(self.input_box)  # Remove input box
            self.display_sequence()
            
            ready_button = Button(text="I'm ready", on_press=self.show_input_page)
            self.layout.add_widget(ready_button)
        except ValueError:
            pass  # Handle invalid input
        
    def show_input_page(self, instance):
        self.layout.clear_widgets()  # Clear the layout
        input_page = BoxLayout(orientation='vertical')
        
        self.input_field = TextInput(hint_text='Enter the sequence you remember', multiline=False)
        numeric_keypad = self.create_numeric_keypad_input()
        submit_button = Button(text='Submit', on_press=self.check_sequence)
        
        input_page.add_widget(self.input_field)
        input_page.add_widget(numeric_keypad)
        input_page.add_widget(submit_button)
        
        self.layout.add_widget(input_page)
        self.current_page = input_page
    
    def create_numeric_keypad_common(self, on_digit_press, input_field=None):
        keypad = GridLayout(cols=3, spacing=10, size_hint=(None, None), size=(300, 300))
        for i in range(1, 10):
            button = Button(text=str(i), on_press=on_digit_press)
            keypad.add_widget(button)
        
        # Add the delete button
        delete_button = Button(text='DEL', on_press=self.delete_digit_input)
        keypad.add_widget(delete_button)
        
        return keypad

    
    def create_numeric_keypad(self):
        return self.create_numeric_keypad_common(self.add_digit)

        
    def create_numeric_keypad_input(self):
        return self.create_numeric_keypad_common(self.add_digit_input)
    
    def delete_digit_input(self, instance):
        self.input_field.text = self.input_field.text[:-1]

    
    def delete_digit(self, instance):
        print(2)
        if self.current_page == 'sequence':
            if self.sequence:
                self.sequence.pop()  # Remove the last digit
                self.display_sequence()  # Update the displayed sequence

        
    def add_digit(self, instance):
        if self.current_page == 'input':
            self.input_field.text += instance.text
        else:
            self.input_field.text += instance.text
        
    def add_digit_input(self, instance):
        
        self.input_field.text += instance.text
        
    def show_result_page(self, result_text, show_try_again=True, show_add_digit=False):
        self.layout.clear_widgets()  # Clear the layout
        result_page = BoxLayout(orientation='vertical')
        
        result_label = Label(text=result_text)
        result_page.add_widget(result_label)
        
        streak_label = Label(text=f"Streak: {self.streak_count}")  # Display the streak count
        result_page.add_widget(streak_label)
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        if show_try_again:
            try_again_button = Button(text='Try Again', on_press=self.try_again)
            buttons_layout.add_widget(try_again_button)
        
        if show_add_digit:
            add_digit_button = Button(text='Add a Digit', on_press=self.add_digit_to_sequence)
            buttons_layout.add_widget(add_digit_button)
            
        if not self.player_won:  # Check if the player lost
            remove_digit_button = Button(text='Remove a Digit', on_press=self.remove_digit_from_sequence)
            buttons_layout.add_widget(remove_digit_button)
        
        result_page.add_widget(buttons_layout)
        self.layout.add_widget(result_page)

        
    def check_sequence(self, instance):
        player_input = self.input_field.text
        if player_input == ''.join(map(str, self.sequence)):
            self.player_won = True  # Set player_won to True
            self.streak_count += 1  # Increment the streak count
            self.show_result_page("Congratulations! You got it right!", show_add_digit=True)
        else:
            self.player_won = False  # Set player_won to False
            self.streak_count = 0  # Reset the streak count
            self.show_result_page("Sorry, try again.", show_try_again=True)

            
    def add_digit_to_sequence(self, instance):
        self.layout.clear_widgets()

        self.num_digits += 1  # Increase the number of digits
        self.sequence = self.generate_sequence(self.num_digits)  # Generate a new sequence
        self.display_sequence()  # Display the new sequence
        
        ready_button = Button(text="I'm ready", on_press=self.show_input_page)
        self.layout.add_widget(self.display_area)
        self.layout.add_widget(ready_button)
    
    def remove_digit_from_sequence(self, instance):
        self.layout.clear_widgets()

        if self.num_digits > 1:
            self.num_digits -= 1  # Decrease the number of digits
            self.sequence = self.generate_sequence(self.num_digits)  # Generate a new sequence
            self.display_sequence()  # Display the new sequence
            
            ready_button = Button(text="I'm ready", on_press=self.show_input_page)
            self.layout.add_widget(self.display_area)
            self.layout.add_widget(ready_button)

      
    def try_again(self, instance):
        self.layout.clear_widgets()  # Clear the layout
        
        if self.player_won:  # Check if the player won
            self.sequence = self.generate_sequence(self.num_digits)  # Generate a new sequence
            self.display_sequence()  # Display the new sequence
        else:
            self.display_sequence()  # Display the same sequence again
            
        ready_button = Button(text="I'm ready", on_press=self.show_input_page)
        self.layout.add_widget(self.display_area)
        self.layout.add_widget(ready_button)


        
if __name__ == '__main__':
    BrainGameApp().run()
