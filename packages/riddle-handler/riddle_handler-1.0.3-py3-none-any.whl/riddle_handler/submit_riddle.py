import json
from src.riddle_handler.read_file import read_file

def submit_riddle(riddle: dict) -> str:
    try:
        if not isinstance(riddle, dict):
            return "Error: Invalid input. Please enter a dictionary for the riddle."
        
        required_keys = {"question", "answer", "hint", "difficulty", "topic"}
        if not all(key in riddle for key in required_keys):
            return "Error: Riddle format is incorrect. The correct format is: {\"question\": \"...\", \"answer\": [\"...\"], \"hint\": \"...\", \"difficulty\": \"...\", \"topic\": \"...\"}."
        if not isinstance(riddle["answer"], list):
            return "Error: Riddle format is incorrect. The answer should be a list."
        if not isinstance(riddle["difficulty"], int):
            return "Error: Riddle format is incorrect. The difficulty should be an integer."
        
        riddles = read_file("riddleLibrary.json")

        for existing_riddle in riddles:
            if riddle["question"] == existing_riddle["question"]:
                return "Error: This riddle already exists in the library."
        
        riddle["id"] = len(riddles) + 1
        riddles.append(riddle)
        
        with open("riddleLibrary.json", 'w') as file:
            json.dump(riddles, file)
        
        return "Riddle submitted successfully!"
    
    except Exception as e:
        return f"Unexpected error: {e}"