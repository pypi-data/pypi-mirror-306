import pytest
from PIL import Image
from src.tamagotchi import tamagotchi
import os

# Mock data
test_image_path = "test_image.png"

@pytest.fixture
def tamagotchi_instance():
    """Fixture to create a Tamagotchi instance."""
    return tamagotchi.Tamagotchi()

@pytest.fixture
def create_test_image():
    """Fixture to create a temporary grayscale image for testing."""
    image = Image.new("L", (50, 50), color=128)  
    image.save(test_image_path)
    yield test_image_path
    os.remove(test_image_path)  

def test_get_ascii_art_valid_image(tamagotchi_instance, create_test_image):
    """Test get_ascii_art with a valid image."""
    ascii_art = tamagotchi_instance.get_ascii_art(create_test_image, scale=0.1, character_map=tamagotchi.Tamagotchi.G_SCALE_1)
    assert ascii_art is not None
    assert isinstance(ascii_art, str)
    assert len(ascii_art) > 0

def test_get_ascii_art_invalid_path(tamagotchi_instance):
    """Test get_ascii_art with an invalid image path."""
    ascii_art = tamagotchi_instance.get_ascii_art("non_existent_image.png", scale=0.1, character_map=tamagotchi.Tamagotchi.G_SCALE_1)
    assert ascii_art is None

def test_get_ascii_art_different_character_map(tamagotchi_instance, create_test_image):
    """Test get_ascii_art with a different character map."""
    ascii_art = tamagotchi_instance.get_ascii_art(create_test_image, scale=0.1, character_map=tamagotchi.Tamagotchi.G_SCALE_2)
    assert ascii_art is not None
    assert isinstance(ascii_art, str)
    assert len(ascii_art) > 0

def test_getpet_valid_file(tamagotchi_instance, tmp_path):
    """Test getpet with a valid pet file."""
    # Create a temporary pet file
    pet_number = 1
    pet_content = "Sample Pet ASCII Art"
    pet_file = tmp_path / f"tama-{pet_number}.txt"
    pet_file.write_text(pet_content)

    # Mock the base_dir to tmp_path
    original_dir = tamagotchi_instance.getpet.__globals__['os'].path.dirname
    tamagotchi_instance.getpet.__globals__['os'].path.dirname = lambda _: tmp_path

    try:
        pet_art = tamagotchi_instance.getpet(pet_number)
        assert pet_art == pet_content
    finally:
        # Restore the original dirname function
        tamagotchi_instance.getpet.__globals__['os'].path.dirname = original_dir

def test_getpet_invalid_file(tamagotchi_instance, tmp_path):
    """Test getpet with an invalid file number."""
    # Ensure no such file exists
    pet_number = 999
    pet_art = tamagotchi_instance.getpet(pet_number)
    assert pet_art is None

def test_getpet_non_numeric_input(tamagotchi_instance):
    """Test getpet with a non-numeric input to check error handling."""
    with pytest.raises(TypeError):
        tamagotchi_instance.getpet("not_a_number")