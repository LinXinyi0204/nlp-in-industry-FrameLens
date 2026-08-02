from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

print("OpenAI key loaded:", openai_key is not None)
print("DeepSeek key loaded:", deepseek_key is not None)