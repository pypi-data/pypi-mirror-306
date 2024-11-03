import os
from PIL import Image
import tkinter as tk

# create your own tamagotchi



class Tamagotchi:
    G_SCALE_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    G_SCALE_2 = '@%#*+=-:. '
    
    def __init__(self):
        self.name = ""
        self.background = "white"
        self.food = "apple"
        self.root = None
        self.ascii_art_label = ""  # pet image store
        self.name_entry = None
        self.game_win = None

    def start_game(self):
        pet_name = self.name_entry.get()  # Get the pet name from the input field
        if pet_name:
            self.name = pet_name
            self.game_window()
            
    def game_window(self):
        """Creates the game window after entering the pet's name."""
        # Destroy the main entry window
        self.root.destroy()

        self.game_win = tk.Tk()
        self.game_win.title(f"{self.name}'s Tamagotchi")

        # pet display
        ascii_art_display = tk.Text(
            self.game_win, 
            font=("Courier", 8), 
            bg=self.background, 
            fg="black",  # Changed from "white" to "black"
            height=20,  # Adjust based on ASCII art size
            width=60,   # Adjust based on ASCII art size
            wrap="none"  # Prevent line wrapping
        )
        ascii_art_display.insert("1.0", self.ascii_art_label)
        ascii_art_display.config(state="disabled")  
        ascii_art_display.pack()  

        # Feed button
        feed_button = tk.Button(self.game_win, text="Feed", command=lambda: self.feed(self.food))
        feed_button.pack()

        # Pat button
        pat_button = tk.Button(self.game_win, text="Pat", command=lambda: self.pat(1))
        pat_button.pack()

        self.game_win.mainloop()
                   
            
    def get_ascii_art(self, image_path, scale=0.1, character_map=G_SCALE_1):
        """Converts an image to ASCII art using the specified character map."""
        try:
            image = Image.open(image_path)

            image = image.convert("L")


            width, height = image.size
            aspect_ratio = height / width
            new_width = int(width * scale)
            new_height = int(new_width * aspect_ratio * 0.55)  
            image = image.resize((new_width, new_height))

            ascii_art = ""
            for y in range(new_height):
                for x in range(new_width):
                    gray_value = image.getpixel((x, y))
                    ascii_char = character_map[int((gray_value / 255) * (len(character_map) - 1))]
                    ascii_art += ascii_char
                ascii_art += "\n"
            
            print(ascii_art)  
            return ascii_art

        except FileNotFoundError:
            print(f"Image file '{image_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getpet(self, number):
        """Returns the pet associated with the number input"""
        if not isinstance(number, int):
            raise TypeError("The input must be an integer representing the pet number.")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, f'tama-{number}.txt')
        try:
            with open(filename, 'r') as f:
                pet = f.read()
                self.ascii_art_label = pet
                return pet
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def change_background_color(self, color):
        self.background = color

    def feed(self, food):
        """Handle the feeding action."""
        self.food = food
        print(f"You feed {self.name} a {self.food}!")

    def pat(self, times):
        """Handle the patting action."""
        print(f"You pat {self.name} {times} times!")
        
    def run_game(self):
        """Main method to run the game."""
        # Main window to enter pet's name
        self.root = tk.Tk()
        self.root.title("Tamagotchi")
        self.root.configure(bg='white')

        # Label and entry field for pet's name
        name_label = tk.Label(self.root, text="Enter your pet's name:")
        name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # Start game button
        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.pack()

        self.root.mainloop()
        
# Run the game
if __name__ == "__main__":
    # example usage of the pet
    tamagotchi_game = Tamagotchi()
    tamagotchi_game.getpet(1)  
    tamagotchi_game.feed("banana")
    tamagotchi_game.run_game()