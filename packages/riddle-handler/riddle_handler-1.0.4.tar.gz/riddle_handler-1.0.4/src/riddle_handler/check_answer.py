from .read_file import read_file

def check_answer(riddle_id: int, user_answer: str) -> str:
    try:
        if not isinstance(riddle_id, int) or riddle_id < 0:
            return "Error: Invalid input. Please enter a non-negative integer for the riddle ID."
        
        riddles = read_file("riddleLibrary.json")
        
        if not riddles:
            return "Error: Riddle library is empty or could not be loaded."
        for riddle in riddles:
            if riddle.get("id") == riddle_id:
                normalized_user_answer = user_answer.strip().replace(" ", "").lower()
                correct_answers = [ans.replace(" ", "").lower() for ans in riddle.get("answer", [])]
                if normalized_user_answer in correct_answers:
                    return "Correct answer!"
                else:
                    return "Incorrect answer. Try again!"
        
        return "Error: Riddle ID not found in the library."

    except Exception as e:
        return f"Unexpected error: {e}"
