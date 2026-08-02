from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result_text = message.content[0].text
    result = json.loads(result_text)
    return result

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

scores = audit(
    work=data["work"],
    question_en=data["question_en"],
    question_zh=data["question_zh"],
    chatgpt_answer=data["chatgpt_answer"],
    deepseek_answer=data["deepseek_answer"]
)

print(json.dumps(scores, ensure_ascii=False, indent=2))