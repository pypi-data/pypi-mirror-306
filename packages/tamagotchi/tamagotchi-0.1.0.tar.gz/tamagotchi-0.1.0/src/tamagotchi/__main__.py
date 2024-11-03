import tamagotchi.tamagotchi as t
from PIL import Image

def main():
    print('')
    print('welcome to tamagotchipy!')
    print('')
    print('here you can:')
    print('')
    print(' ' * 5 + '☆ get your very own tamagotchi')
    print(' ' * 5 + '☆ or create your very own tamagotchi')
    print(' ' * 5 + '☆ and name + interact with your tamagotchi')
    print('')

    newpet = ''

    pet = int(input('do you want to generate a pet [1] or make your own using an image [2]? please input 1 for option 1 and 2 for option 2: '))
    
    while pet != 1 and pet != 2:
        print('please input 1 or 2 	(╥﹏╥)')
        pet = int(input('do you want to generate a pet [1] or make your own using an image [2]? please input 1 for option 1 and 2 for option 2: '))
    
    if pet == 1:
        num = int(input('please input any number from 1 to 11... your new pet is waiting for you!: '))
        newpet = t.getpet(num)
        while not(num >= 1 and num <= 11):
            print('your pet is waiting for you... please put in a valid number! (╥﹏╥): ')
            num = int(input('please input any number from 1 to 11... your new pet is waiting for you!: '))
            newpet = t.getpet(num)
        print(newpet)
    else:
        image_path = str(input('please give a correct file path to your image!: '))
        print('generating your pet...')
        print('☆')
        print('☆')
        print('☆')
        print('☆')
        print('☆')
        print('')
        result = t.get_ascii_art(image_path, scale=0.1, character_map=t.G_SCALE_1)
        while result is None:
            image_path = str(input('please give a correct file path to your image!: '))
            print('generating your pet...')
            print('☆')
            print('☆')
            print('☆')
            print('☆')
            print('☆')
            print('')
            result = t.get_ascii_art(image_path, scale=0.1, character_map=t.G_SCALE_1)
        newpet = result

    print('done')
if __name__ == "__main__":
    main()