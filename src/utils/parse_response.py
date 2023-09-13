import re
import json

def extract_json_from_response(response: str) -> dict:
    # Use regex to find JSON-like substring
    match = re.search(r'(?=\{).*(?<=\})', response, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    return {}
