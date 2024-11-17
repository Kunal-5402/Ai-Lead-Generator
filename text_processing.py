import json
import re

def extract_json(response: str):
    try:
        pattern = r'```json(.*?)```'
        match = re.search(pattern, response, flags=re.DOTALL)
        if match:
            json_data = match.group(1)
            data = json.loads(json_data)
            return data
        else:
            raise ValueError("No JSON code block found in the response.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during extracting JSON: {e}")