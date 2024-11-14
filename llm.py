import os
import openai
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key = os.environ.get("SAMBANOVA_API_KEY"),
            base_url = os.environ.get("SAMBANOVA_ENDPOINT"),
        )
    
    def generate(self, user_query: str, system_prompt: str = "You are a helpful assistant"):

        try:
            response = self.client.chat.completions.create(
                model = os.environ.get("MODEL"),
                messages = [
                    {"role" : "system" , "content" : system_prompt},
                    {"role" : "user", "content" : user_query}
                ],
                temperature = 1e-12,
                top_p = 1,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"An error occurred during generation: {e}")