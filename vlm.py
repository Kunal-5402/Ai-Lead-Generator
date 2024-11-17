import os
import base64
import openai
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.environ.get("SAMBANOVA_API_KEY"),
            base_url=os.environ.get("SAMBANOVA_ENDPOINT"),
        )
    
    def generate(self, image_path: str = "assets/captured_photo.jpg", system_prompt: str = "You are a helpful assistant"):
        print(image_path)
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            raise RuntimeError(f"Image file not found: {image_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the image: {e}")

        try:
            response = self.client.chat.completions.create(
                model="Llama-3.2-11B-Vision-Instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", "text": system_prompt
                            },
                            {
                                "type": "image_url", 
                                "image_url": 
                                {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"}
                                },
                        ],
                    }
                ],
                temperature=1e-12,
                top_p=1,
            )
            # print(response)
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"An error occurred during generation: {e}")