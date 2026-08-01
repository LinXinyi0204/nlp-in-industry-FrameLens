from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()


chatgpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def ask_chatgpt(question_en):
    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question_en}]
    )
    return response.choices[0].message.content

def ask_deepseek(question_zh):
    response = deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question_zh}]
    )
    return response.choices[0].message.content

def run_question(work, question_en, question_zh):
    print(f"working on：{work}")
    
    answer_en = ask_chatgpt(question_en)
    answer_zh = ask_deepseek(question_zh)
    
    result = {
        "work": work,
        "question_en": question_en,
        "question_zh": question_zh,
        "chatgpt_answer": answer_en,
        "deepseek_answer": answer_zh
    }
    
    return result


result = run_question(
    work="Journey to the West",
    question_en="What is the core conflict in Journey to the West?",
    question_zh="《西游记》的核心冲突是什么？"
)


print("\n--- ChatGPT 回答 ---")
print(result["chatgpt_answer"])
print("\n--- DeepSeek 回答 ---")
print(result["deepseek_answer"])


with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("output has been saved in output.json")