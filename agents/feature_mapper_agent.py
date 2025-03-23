from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FeatureMapperAgent:
    def __init__(self, prompt: str, dataset_columns: list, target_column: str = None):
        self.prompt = prompt
        self.dataset_columns = dataset_columns
        self.target_column = target_column

    def run(self) -> dict:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You select relevant feature columns based on user queries."},
                {"role": "user", "content": f"Prompt: {self.prompt}\nAvailable Columns: {self.dataset_columns}"}
            ],
            functions=[{
                "name": "map_features",
                "description": "Select relevant dataset columns for ML model input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["features"]
                }
            }],
            function_call="auto"
        )

        # Parse the stringified JSON
        result = json.loads(response.choices[0].message.function_call.arguments)

        # Exclude target column if it's in the returned features
        if self.target_column:
            result["features"] = [f for f in result["features"] if f != self.target_column]

        return result




if __name__ == "__main__":
    # Assume Task Classifer is already run and we have "target"
    prompt = "Predict if a 70-year-old man from 1st class will survive the Titanic."
    columns = ["Age", "Sex", "Pclass", "Fare", "Survived", "Name", "Cabin"]
    target = "Survived"

    agent = FeatureMapperAgent(prompt, columns, target_column=target)
    result = agent.run()

    print(result)

