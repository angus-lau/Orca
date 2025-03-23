from openai import OpenAI
import os
from dotenv import load_dotenv
import json


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TaskClassifierAgent:
    def __init__(self, prompt: str, dataset_columns: list):
        self.prompt = prompt
        self.dataset_columns = dataset_columns

    def run(self) -> dict:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You classify ML tasks into classification, regression, NLP, or time series ONLY."},
                {"role": "user", "content": f"Prompt: {self.prompt}\nColumns: {self.dataset_columns}"}
            ],
            functions=[{
                "name": "classify_task",
                "description": "Classify ML task and specify target column.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_type": {"type": "string"},
                        "target_column": {"type": "string"}
                    },
                    "required": ["task_type", "target_column"]
                }
            }],
            function_call="auto"
        )
        return json.loads(response.choices[0].message.function_call.arguments)


if __name__ == "__main__":
    # Example test case
    prompt = "How much will a 20 year old middle class female pay for the titanic?"
    columns = ["Age", "Sex", "Pclass", "Fare", "Survived"]

    agent = TaskClassifierAgent(prompt, columns)
    result = agent.run()

    print("🧪 Test Result:")
    print(result)