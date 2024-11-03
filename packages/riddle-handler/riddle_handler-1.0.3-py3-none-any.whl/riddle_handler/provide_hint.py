from src.riddle_handler.read_file import read_file

def provide_hint(riddle_id) -> str:
    try:
        if not isinstance(riddle_id, int) or riddle_id < 0:
            return "Error: Invalid input. Please enter a non-negative integer for the riddle ID."

        riddles = read_file("riddleLibrary.json")

        if not riddles:
            return "Error: Riddle library is empty or could not be loaded."

        for riddle in riddles:
            if riddle.get("id") == riddle_id:
                return f"Hint: {riddle.get('hint')} (Topic: {riddle.get('topic')})"

        return "Error: Riddle ID not found in the library."

    except Exception as e:
        return f"Unexpected error: {e}"