import pytest
from unittest.mock import patch
from petpy.src import petpy
from petpy.src.petpy import pets

@pytest.fixture
def reset_pets():
    pets.clear() 

@pytest.fixture
def sample_pet():
    return petpy.Pet(name="Buddy", pet_type="dog")

def test_pet_initialization(sample_pet):
    assert sample_pet.name == "Buddy"
    assert sample_pet.type == "dog"
    assert sample_pet.emoji == '🐕'
    assert sample_pet.level == 1
    assert sample_pet.experience == 0
    assert 15 <= sample_pet.health <= 20  
    assert sample_pet.mood == 5

def test_pet_initialization_with_unknown_type():
    pet = petpy.Pet(name="Unknown", pet_type="dragon")
    assert pet.name == "Unknown"
    assert pet.type == "dragon"
    assert pet.emoji == '🐾' 


# Feed tests
def test_feed_valid_food(sample_pet):
    petpy.feed(sample_pet, "kfc")
    # assert "Buddy ate 🍗 and their mood changed to happy 🤗" in result
    assert 1 <= sample_pet.mood <= 10
    assert 0 <= sample_pet.health <= 20

def test_feed_different_foods(sample_pet):
    result_salad = petpy.feed(sample_pet, "salad")
    result_candy = petpy.feed(sample_pet, "candy")
    assert "Buddy ate 🥗 and their mood changed" in result_salad
    assert "Buddy ate 🍬 and their mood changed" in result_candy

def test_feed_invalid_food(sample_pet):
    result = petpy.feed(sample_pet, "pizza")
    assert result == "pizza is not on the menu!"


# Mood checks
def test_check_pet_mood(sample_pet):
    mood_result = petpy.get_pet_mood(sample_pet)
    assert f"{sample_pet.name}'s current mood is" in mood_result

def test_check_pet_mood_after_feeding(sample_pet):
    petpy.feed(sample_pet, "sake")
    mood_result = petpy.get_pet_mood(sample_pet)
    assert f"{sample_pet.name}'s current mood is" in mood_result

def test_check_pet_mood_limits(sample_pet):
    sample_pet.mood = 1  # lowest mood
    result = petpy.get_pet_mood(sample_pet)
    assert "crying 😭" in result
    sample_pet.mood = 10  # highest mood
    result = petpy.get_pet_mood(sample_pet)
    assert "ecstatic 🤩" in result


# Level checks
def test_check_pet_level(sample_pet):
    level_result = petpy.get_pet_level(sample_pet)
    assert level_result == f"{sample_pet.name} is Level {sample_pet.level} with {sample_pet.experience} XP."

def test_check_pet_level_after_experience(sample_pet):
    sample_pet.level = 2
    sample_pet.experience = 30
    level_result = petpy.get_pet_level(sample_pet)
    assert "Level 2" in level_result
    assert "30 XP" in level_result

def test_check_pet_level_no_experience(sample_pet):
    sample_pet.experience = 0
    result = petpy.get_pet_level(sample_pet)
    assert "0 XP" in result


# Health checks
def test_check_pet_health(sample_pet):
    health_result = petpy.get_pet_health(sample_pet)
    assert f"{sample_pet.name}'s current health is {sample_pet.health}." in health_result

def test_check_pet_health_after_feeding(sample_pet):
    petpy.feed(sample_pet, "carrot")
    health_result = petpy.get_pet_health(sample_pet)
    assert "current health is" in health_result

def test_check_pet_health_limits(sample_pet):
    sample_pet.health = 0  # lowest health
    health_result = petpy.get_pet_health(sample_pet)
    assert "current health is 0" in health_result
    sample_pet.health = 20  # highest health
    health_result = petpy.get_pet_health(sample_pet)
    assert "current health is 20" in health_result


# Stats checks
def test_check_pet_stats_correct_name(sample_pet):
    stats_result = petpy.get_pet_stats(sample_pet, "Buddy")
    assert "Pet: Buddy 🐕" in stats_result
    assert "Type: Dog" in stats_result
    assert f"Health: {sample_pet.health}/20" in stats_result
    assert f"Mood: {sample_pet.MOOD_LEVELS.get(sample_pet.mood)}" in stats_result

def test_check_pet_stats_wrong_name(sample_pet):
    stats_result = petpy.get_pet_stats(sample_pet, "Charlie")
    assert stats_result == "Pet not found."

def test_check_pet_stats_different_pet():
    pet = petpy.Pet(name="Whiskers", pet_type="cat")
    stats_result = petpy.get_pet_stats(pet, "Whiskers")
    assert "Pet: Whiskers 🐈" in stats_result


# Create pet tests
def test_create_pet(reset_pets):
    pet = petpy.create_pet("Fluffy", "cat")
    assert isinstance(pet, petpy.Pet)  
    assert pet.name == "Fluffy"  
    assert pet.type == "cat"     
    assert pet.emoji == '🐈'    
    assert pet.level == 1        
    assert 15 <= pet.health <= 20  
    assert pet.mood == 5      
    print(pets)
    assert "Fluffy" in pets  

def test_create_pet_invalid_type(reset_pets):
    pet = petpy.create_pet("Unknown", "dragon")
    assert pet.emoji == '🐾'  
    assert pet.type == "dragon" 

def test_create_duplicate_pet(reset_pets):
    petpy.create_pet("Fluffy", "cat")
    result = petpy.create_pet("Fluffy", "dog")
    assert result == "A pet named Fluffy already exists."


# Release pet tests
def test_release_pet(reset_pets):
    petpy.create_pet("Buddy", "dog")
    petpy.release_pet("Buddy")
    #assert result == "Buddy has been released :("
    assert "Buddy" not in pets  

def test_release_pet_not_found(reset_pets):
    result = petpy.release_pet("NonExistentPet")
    assert result == "NonExistentPet not found!"

def test_release_multiple_pets(reset_pets):
    petpy.create_pet("Buddy", "dog")
    petpy.create_pet("Fluffy", "cat")

    petpy.release_pet("Buddy")
    petpy.release_pet("Fluffy")
    
    # assert release_result_buddy == "Buddy has been released :("
    # assert release_result_fluffy == "Fluffy has been released :("
    assert "Buddy" not in pets
    assert "Fluffy" not in pets

# Fight tests
def test_fight_win(sample_pet):
    base_stats = [sample_pet.health, sample_pet.experience]

    with patch("random.randint") as mock_randint:
        mock_randint.side_effect = [10, 17, 3]
        petpy.fight(sample_pet)
        
        assert base_stats == [sample_pet.health + 3, sample_pet.experience - 17] 

def test_fight_loss(sample_pet):
    base_stats = [sample_pet.health, sample_pet.mood]

    with patch("random.randint") as mock_randint:
        mock_randint.side_effect = [0, 3]
        petpy.fight(sample_pet)
        
        assert base_stats == [sample_pet.health + 3, sample_pet.mood + 2]

def test_fight_win_loss_win(sample_pet):
    base_stats = [sample_pet.health, sample_pet.experience, sample_pet.mood]

    with patch("random.randint") as mock_randint:
        mock_randint.side_effect = [10, 17, 3, 0, 3, 10, 17, 3]
        petpy.fight(sample_pet)
        petpy.fight(sample_pet)
        petpy.fight(sample_pet)
        
        assert base_stats == [sample_pet.health + 9, sample_pet.experience - 34, sample_pet.mood + 2]

# Training tests
def test_training(sample_pet):
    base_stats = [sample_pet.mood, sample_pet.experience]

    with patch("random.randint") as mock_randint:
        mock_randint.return_value = 3
        petpy.train_pet(sample_pet)

        assert base_stats == [sample_pet.mood + 3, sample_pet.experience - 21]

def test_training_level_up(sample_pet):
    sample_pet.experience = 90
    base_stats = sample_pet.level

    with patch("random.randint") as mock_randint:
        mock_randint.return_value = 3
        petpy.train_pet(sample_pet)

        assert base_stats == sample_pet.level - 1
        assert sample_pet.experience == 11

def test_training_release(sample_pet):
    sample_pet.mood = 1

    with patch("random.randint") as mock_randint:
        mock_randint.return_value = 3
        petpy.train_pet(sample_pet)

        assert sample_pet.name not in pets
                              

