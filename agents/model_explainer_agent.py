from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ModelExplainerAgent:
    def __init__(self, prompt: str, model_summary: dict):
        self.prompt = prompt
        self.model_summary = model_summary

    def run(self) -> str:
        explanation_prompt = f"""
        User Prompt: {self.prompt}
        Model Summary:
        {json.dumps(self.model_summary, indent=2)}

        Explain what the model learned, why it was chosen, and answer the prompt directly.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a model explanation assistant."},
                {"role": "user", "content": explanation_prompt}
            ]
        )
        return response.choices[0].message.content
