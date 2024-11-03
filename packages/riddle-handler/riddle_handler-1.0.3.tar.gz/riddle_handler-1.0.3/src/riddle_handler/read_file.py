import json

def read_file(filename: str) -> list:
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: File not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON file.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []