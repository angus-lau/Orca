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
        # Enhanced instruction with clearer distinctions for LLM
        system_prompt = (
            "You classify ML tasks into one of the following strictly: \n"
            "- classification: if the target column is a category or label (e.g. 0/1, High/Low, Yes/No) however check if it could be NLP too\n"
            "- regression: if the target column is numeric and continuous (e.g. price, weight, score)\n"
            "- NLP: if the input features include text (e.g. messages, reviews, tickets) or the query includes this\n"
            "- time series: if the data involves a datetime column and you want to predict future values\n\n"
            "Use the prompt AND the column names to choose.\n"
            "Do NOT classify NLP or sentiment prediction as classification.\n"
            "Do NOT classify time-based predictions without a datetime column as time series."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
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

        except Exception as e:
            print("Failed to classify task:", str(e))
            return {"task_type": "unknown", "target_column": None}


if __name__ == "__main__":
    # Example test case for sentiment
    prompt = "How urgent is this support ticket: 'My server has been down for 6 hours'?"
    columns = ["TicketText", "Priority"]

    agent = TaskClassifierAgent(prompt, columns)
    result = agent.run()

    print("🧪 Test Result:")
    print(result)
