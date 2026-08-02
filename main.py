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
You are an impartial literary analyst. Two AI models were asked the same question about a literary work, one in English and one in Chinese. 
Your task is to compare their answers using Entman's four framing dimensions and score the DIVERGENCE between them.

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer (in English):
{chatgpt_answer}

DeepSeek's answer (in Chinese):
{deepseek_answer}

1. Problem Definition (0-2):
   0 = both models identify the exact same core conflict using similar concepts
   1 = both identify conflict but emphasize different aspects (e.g. one focuses on external obstacles, the other on internal struggle)
   2 = models identify fundamentally different types of conflict (e.g. one frames it as good vs evil, the other as freedom vs constraint)

2. Causal Attribution (0-2):
   0 = both models attribute the conflict to the same cause
   1 = both identify causes but at different levels (e.g. one blames individuals, the other blames social structures)
   2 = models attribute the conflict to completely opposite sources

3. Moral Evaluation (0-3):
   0 = both models make the same moral judgment about characters or events
   1 = both make positive/negative judgments but with different emphasis
   2 = one model is clearly more critical or sympathetic than the other
   3 = models reach opposite moral conclusions (e.g. one sees a character as heroic, the other as problematic)

4. Suggested Lesson (0-3):
   0 = both models draw the same takeaway
   1 = takeaways are similar but phrased differently
   2 = takeaways focus on different values (e.g. one emphasizes cooperation, the other emphasizes individual growth)
   3 = takeaways are contradictory (e.g. one says "submit to authority", the other says "resist authority")

IMPORTANT: Focus on DIVERGENCE, not similarity. 
Even if both answers share some common ground, score based on how differently they frame the issue. 
A surface similarity (both mention "struggle") does not reduce the score if the underlying frameworks are fundamentally different.

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

# read the questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

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