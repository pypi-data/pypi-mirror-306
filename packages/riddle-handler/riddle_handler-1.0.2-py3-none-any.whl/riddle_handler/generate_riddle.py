import json
import random
from src.riddle_handler.read_file import read_file

def generate_riddle(difficulty: int) -> str:
    if type(difficulty) is not int:
        raise TypeError("Difficulty should be an integer.")
    if difficulty < 1 or difficulty > 4:
        raise ValueError("Difficulty should be between 1 and 4.")

    riddle_lib = read_file("riddleLibrary.json")

    riddles = []
    for riddle in riddle_lib:
        if riddle['difficulty'] == difficulty:
            riddles.append(riddle)
            
    random_element = random.choice(riddles)
    return random_element['question']

