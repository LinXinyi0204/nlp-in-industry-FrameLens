from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import anthropic

load_dotenv()

# initialize three clients
chatgpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
auditor = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

def audit(work, question_en, question_zh, chatgpt_answer, deepseek_answer):
    prompt = f"""
You are an impartial literary analyst. Two AI models were asked the same question about a literary work, one in English and one in Chinese. Your task is to compare their answers using Entman's four framing dimensions and score the DIVERGENCE between them.

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer (in English):
{chatgpt_answer}

DeepSeek's answer (in Chinese):
{deepseek_answer}

Score the divergence between the two answers on each dimension:

1. Problem Definition (0-2):
   0 = both identify the same core conflict
   1 = partially different
   2 = entirely different core conflict

2. Causal Attribution (0-2):
   0 = same cause identified
   1 = partially different
   2 = attribution in opposite directions

3. Moral Evaluation (0-3):
   0 = same evaluative direction
   1 = slightly different
   2 = noticeably different
   3 = opposite moral direction

4. Suggested Lesson (0-3):
   0 = same takeaway
   1 = slightly different
   2 = noticeably different
   3 = contradictory takeaway

Respond ONLY in this exact JSON format:
{{
  "problem_definition": <score>,
  "causal_attribution": <score>,
  "moral_evaluation": <score>,
  "suggested_lesson": <score>,
  "total": <sum of all scores>,
  "reasoning": "<one sentence explaining the main source of divergence>"
}}
"""
    message = auditor.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    result_text = message.content[0].text
    print("Claude returned:", result_text)
    result_text = result_text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(result_text)
    
def run(work, question_en, question_zh):
    print(f"Processing: {work}")
    
    chatgpt_answer = ask_chatgpt(question_en)
    deepseek_answer = ask_deepseek(question_zh)
    scores = audit(work, question_en, question_zh, chatgpt_answer, deepseek_answer)
    
    result = {
        "work": work,
        "question_en": question_en,
        "question_zh": question_zh,
        "chatgpt_answer": chatgpt_answer,
        "deepseek_answer": deepseek_answer,
        "scores": scores
    }
    
    return result

# add more questions here once B finishes designing them
questions = [
    {
        "work": "Journey to the West",
        "question_en": "What is the core conflict in Journey to the West?",
        "question_zh": "《西游记》的核心冲突是什么？"
    },
]

# run all questions
all_results = []
for q in questions:
    result = run(q["work"], q["question_en"], q["question_zh"])
    all_results.append(result)
    print(f"Done: {q['work']} | Total score: {result['scores']['total']}/10")

# save all results
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("\nAll results saved to results.json")