import tamagotchi.tamagotchi as t
from PIL import Image

def main():
    print('')
    print('Welcome to Tamagotchipy!')
    print('')
    print('Here you can:')
    print('')
    print(' ' * 5 + '☆ Get your very own Tamagotchi')
    print(' ' * 5 + '☆ Or create your own Tamagotchi')
    print(' ' * 5 + '☆ And name + interact with your Tamagotchi')
    print('')

    # Create an instance of Tamagotchi
    tamagotchi_game = t.Tamagotchi()

    # Choose the type of pet
    try:
        pet = int(input('Do you want to generate a pet [1] or make your own using an image [2]? Please input 1 for option 1 and 2 for option 2: '))
        while pet != 1 and pet != 2:
            print('Please input 1 or 2 	(╥﹏╥)')
            pet = int(input('Do you want to generate a pet [1] or make your own using an image [2]? Please input 1 for option 1 and 2 for option 2: '))
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        return  # Exit if input is not valid

    if pet == 1:
        # Generate a predefined pet
        try:
            num = int(input('Please input any number from 1 to 11... Your new pet is waiting for you!: '))
            while not (1 <= num <= 11):
                print('Your pet is waiting for you... please put in a valid number! (╥﹏╥)')
                num = int(input('Please input any number from 1 to 11... Your new pet is waiting for you!: '))
            tamagotchi_game.ascii_art_label = tamagotchi_game.getpet(num)  # Explicitly set ascii_art_label
            
            if not tamagotchi_game.ascii_art_label:
                print("Error: Predefined pet text could not be loaded.")
                return  # Exit if no pet content
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 11.")
            return  # Exit if input is not valid
    else:
        # Generate ASCII art from an image
        image_path = str(input('Please provide the file path to your image!: '))
        print('Generating your pet...')

        tamagotchi_game.ascii_art_label = tamagotchi_game.get_ascii_art(image_path, scale=0.1, character_map=t.Tamagotchi.G_SCALE_1)

        while tamagotchi_game.ascii_art_label is None:
            print("Failed to generate ASCII art. Please check the file path and try again.")
            image_path = str(input('Please provide a correct file path to your image!: '))
            print('Generating your pet...')
            tamagotchi_game.ascii_art_label = tamagotchi_game.get_ascii_art(image_path, scale=0.1, character_map=t.Tamagotchi.G_SCALE_1)

    # Display the ASCII art or pet text in the terminal only once
    print("ASCII Art or Predefined Pet Text:")
    print(tamagotchi_game.ascii_art_label)  # Print final result

    print('Done!')

    # Start the GUI with the generated pet
    tamagotchi_game.run_game()

if __name__ == "__main__":
    main()
