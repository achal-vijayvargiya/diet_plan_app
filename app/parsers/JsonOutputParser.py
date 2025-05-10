from langchain.schema import BaseOutputParser
import json
import re

class DietParser(BaseOutputParser):
    def parse(self, text: str) -> dict:
        print(text)
        try:
            # Extract JSON part using regex
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if not match:
                raise ValueError("No JSON found in the response.")
            json_str = match.group(1)
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("❌ JSON decoding error:", e)
        except Exception as e:
            print("❌ Other error:", e)
        
    

JsonOutputDietParser = DietParser()