import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import os
from datetime import datetime

class NumerologyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerology Calculator")
        self.root.geometry("320x410")  # Adjusted for the additional row of buttons
        self.root.resizable(width=False, height=False)

        self.DEFAULT_THEME = {
            "bg": "#121212",
            "button_bg": "#363636",
            "button_fg": "#000000",
            "text_fg": "#000000",
            "label_fg": "#FFFFFF",
        }

        self.current_theme = {
            "bg": "#FFFFFF",
            "button_bg": "#E0E0E0",
            "button_fg": "#000000",
            "text_fg": "#000000",
            "label_fg": "#000000",
        }

        self.create_widgets()
        self.create_styles()
        self.theme_colors()

    def create_widgets(self):
        self.label_birth_date = ttk.Label(self.root, text="Birth Date (YYYY-MM-DD):")
        self.entry_birth_date = ttk.Entry(self.root, font=('Arial', 10, 'bold'), justify='center')
        self.label_full_name = ttk.Label(self.root, text="Full Name:")
        self.entry_full_name = ttk.Entry(self.root, font=('Arial', 10, 'bold'), justify='center')
        self.calculate_button = ttk.Button(self.root, text="Calculate", command=self.calculate_numerology)
        
        self.entry_full_name.bind('<Return>', self.calculate_numerology)
        self.entry_birth_date.bind('<Return>', self.calculate_numerology)
        
        self.results_text = tk.Text(self.root, height=10, width=50, borderwidth=2, relief="groove")
        self.results_text.config(state=tk.DISABLED, wrap=tk.WORD)
        
        # Button frame for original buttons
        self.buttons_frame = tk.Frame(self.root)
        self.copy_button = ttk.Button(self.buttons_frame, text="Copy", command=self.copy_to_clipboard)
        self.color_button = ttk.Button(self.buttons_frame, text="Change Color", command=self.change_color_scheme)
        self.reset_button = ttk.Button(self.buttons_frame, text="Reset Color", command=self.reset_color_scheme)
        self.dark_mode_button = ttk.Button(self.buttons_frame, text="Dark Mode", command=self.toggle_dark_mode)
        
        # Button frame for new buttons
        self.extra_buttons_frame = tk.Frame(self.root)
        self.about_button = ttk.Button(self.extra_buttons_frame, text="About", command=self.show_about)
        self.help_button = ttk.Button(self.extra_buttons_frame, text="Help", command=self.show_help)  # New Help button
        self.save_button = ttk.Button(self.extra_buttons_frame, text="Save Results", command=self.save_results)  # New Save button
        self.exit_button = ttk.Button(self.extra_buttons_frame, text="Exit", command=self.root.quit)
        
        
        # Packing widgets
        self.label_birth_date.pack(pady=5)
        self.entry_birth_date.pack(pady=5)
        self.label_full_name.pack(pady=5)
        self.entry_full_name.pack(pady=5)
        self.calculate_button.pack(pady=5)
        self.results_text.pack(pady=5)
        self.buttons_frame.pack(pady=5)
        self.copy_button.pack(side=tk.LEFT)
        self.color_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.dark_mode_button.pack(side=tk.LEFT)
        self.extra_buttons_frame.pack(pady=5)
        self.about_button.pack(side=tk.LEFT)
        self.help_button.pack(side=tk.LEFT)  # Pack Help button
        self.save_button.pack(side=tk.LEFT)  # Pack Save button
        self.exit_button.pack(side=tk.LEFT)
        
    def show_help(self):
        help_message = """
    Welcome to the Numerology Calculator Help:

    1. Enter your birth date in the format YYYY-MM-DD.
    2. Enter your full name (no spaces or special characters).
    3. Click the 'Calculate' button to generate numerology results.
    4. The results will be displayed below.
    5. You can copy the results to your clipboard using the 'Copy' button.
    6. Change the color scheme with the 'Change Color' button.
    7. Reset the color scheme to default with the 'Reset Color' button.
    8. Switch between light and dark modes using the 'Dark Mode' button.
    9. Use the 'Save Results' button to save the results to a text file.

    For additional assistance or information, please contact LaryGaryMods.
    """

        # Create a new top-level window for the help message
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("400x300")  # Set the window size
        help_window.resizable(False, False)

        # Create a text widget for the help message
        text_widget = tk.Text(help_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)

        # Configure the text widget
        text_widget.insert(tk.END, help_message)
        text_widget.config(state=tk.NORMAL, font=("Arial", 8, "bold"), padx=10, pady=10)
        text_widget.tag_configure("center", justify="center")

        # Center the text in the text widget
        text_widget.tag_add("center", "1.0", "end")

        # Disable text editing
        text_widget.config(state=tk.DISABLED)




    def calculate_chinese_zodiac(self, birth_date):
        year = int(birth_date.split('-')[0])
    # The start year for the Chinese Zodiac cycle is 1924, which corresponds to the Rat.
        start_year = 1924
        animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
        zodiac_index = (year - start_year) % 12
        return animals[zodiac_index]




    def calculate_zodiac_sign(self, birth_date):
        month, day = (int(x) for x in birth_date.split('-')[1:3])
        zodiac_signs = [(3, 21, "Aries"), (4, 20, "Taurus"), (5, 21, "Gemini"), (6, 21, "Cancer"), (7, 23, "Leo"), 
                        (8, 23, "Virgo"), (9, 23, "Libra"), (10, 23, "Scorpio"), (11, 22, "Sagittarius"), 
                        (12, 22, "Capricorn"), (1, 20, "Aquarius"), (2, 19, "Pisces")]
        for i, (month_start, day_start, sign) in enumerate(zodiac_signs):
            if (month == month_start and day >= day_start) or (month == month_start + 1 and day < day_start):
                return sign
        return "Aries"  # Default to Aries if date is not in the range

    def calculate_numerology(self, event=None):
        birth_date = self.entry_birth_date.get()
        full_name = self.entry_full_name.get().replace(" ", "")

        if not birth_date or not full_name:
            messagebox.showerror("Error", "Please enter both a birth date and a full name.")
            return

        try:
            life_path_number = self.calculate_life_path(birth_date)
            birthday_number = self.calculate_birthday(birth_date)
            destiny_number = self.calculate_destiny(full_name)
            soul_urge_number = self.calculate_soul_urge(full_name)
            personality_number = self.calculate_personality(full_name)
            chinese_zodiac = self.calculate_chinese_zodiac(birth_date)
            zodiac_sign = self.calculate_zodiac_sign(birth_date)

            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, f"Life Path: {life_path_number}\n"
                                        f"Birthday: {birthday_number}\n"
                                        f"Destiny: {destiny_number}\n"
                                        f"Soul Urge: {soul_urge_number}\n"
                                        f"Personality: {personality_number}\n"
                                        f"Chinese Zodiac: {chinese_zodiac}\n"
                                        f"Zodiac Sign: {zodiac_sign}")
            self.results_text.update_idletasks()
            self.results_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_results(self):
        # Get the current text from the results_text widget
        results = self.results_text.get("1.0", tk.END).strip()
        # Check if there is something to save
        if results:
            # Logic to save the results to a file
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                     filetypes=[("Text Documents", "*.txt")])
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(results)
                    messagebox.showinfo("Save Successful", "The numerology results have been saved.")
                except Exception as e:
                    messagebox.showerror("Save Error", str(e))
        else:
            messagebox.showinfo("No Results", "There are no results to save.")

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure('TLabel', background=self.current_theme["bg"], foreground=self.current_theme["label_fg"])
        self.style.configure('TButton', background=self.current_theme["button_bg"], foreground=self.current_theme["button_fg"])
        self.style.configure('TEntry', background=self.current_theme["button_bg"], foreground=self.current_theme["text_fg"])

    def letter_to_number(self, letter):
        return (ord(letter.lower()) - 96) % 9 or 9

    def calculate_life_path(self, birth_date):
        return sum(int(digit) for digit in birth_date if digit.isdigit()) % 9 or 9

    def calculate_birthday(self, birth_date):
        return int(birth_date.split('-')[2])

    def calculate_destiny(self, full_name):
        return sum(self.letter_to_number(char) for char in full_name if char.isalpha()) % 9 or 9

    def calculate_soul_urge(self, full_name):
        vowels = 'aeiou'
        return sum(self.letter_to_number(char) for char in full_name if char.lower() in vowels) % 9 or 9

    def calculate_personality(self, full_name):
        vowels = 'aeiou'
        consonants = ''.join([char for char in full_name if char.lower() not in vowels and char.isalpha()])
        return sum(self.letter_to_number(char) for char in consonants) % 9 or 9

    def copy_to_clipboard(self):
        results = self.results_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(results.strip())
        self.copy_button.config(state=tk.DISABLED)
        self.root.after(200, self.enable_copy_button)

    def enable_copy_button(self):
        self.copy_button.config(state=tk.NORMAL)

    def change_color_scheme(self):
        # Specify a default color (white) for the color chooser dialog
        initial_color = self.current_theme["bg"] if self.current_theme == self.DEFAULT_THEME else None

        # Open a color chooser dialog and get the selected color
        result = colorchooser.askcolor(initialcolor=initial_color)

    # Check if a color was selected
        if result[1] is not None:
            self.current_theme["bg"] = result[1]

        # Apply the new color scheme
            self.theme_colors()




    def reset_color_scheme(self):
        self.current_theme = self.DEFAULT_THEME
        self.theme_colors()

    def theme_colors(self):
        self.root.configure(bg=self.current_theme["bg"])
        self.style.configure('TLabel', background=self.current_theme["bg"], foreground=self.current_theme["label_fg"])
        self.style.configure('TButton', background=self.current_theme["button_bg"], foreground=self.current_theme["button_fg"])
        self.style.configure('TEntry', background=self.current_theme["button_bg"], foreground=self.current_theme["text_fg"])
        self.results_text.configure(bg=self.current_theme["button_bg"], fg=self.current_theme["text_fg"])
        self.label_birth_date.configure(foreground=self.current_theme["label_fg"])
        self.label_full_name.configure(foreground=self.current_theme["label_fg"])

    def toggle_dark_mode(self):
        if self.current_theme == self.DEFAULT_THEME:
            self.current_theme = {
                "bg": "#FFFFFF",
                "button_bg": "#E0E0E0",
                "button_fg": "#000000",
                "text_fg": "#000000",
                "label_fg": "#000000",
            }
            self.dark_mode_button.config(text="Dark")
        else:
            self.current_theme = self.DEFAULT_THEME
            self.dark_mode_button.config(text="Light")
        self.theme_colors()

    def show_about(self):
        messagebox.showinfo("About", "Numerology Calculator\nVersion 1.0\nDeveloped by LaryGaryMods")


if __name__ == "__main__":
    root = tk.Tk()
    app = NumerologyCalculator(root)
    root.mainloop()
