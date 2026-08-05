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

def ask_chatgpt(question_en, question_type="general"):
    if question_type == "fact":
        question_en = "Answer factually and concisely. Do not add any analysis, evaluation, or personal commentary. Stick to the facts only.\n\n" + question_en
    response = chatgpt.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question_en}]
    )
    return response.choices[0].message.content

def ask_deepseek(question_zh, question_type="general"):
    if question_type == "fact":
        question_zh = "请只回答事实，简洁准确，不要添加任何分析、评价或个人评论。\n\n" + question_zh
    response = deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question_zh}]
    )
    return response.choices[0].message.content

def audit(work, question_en, question_zh, chatgpt_answer, deepseek_answer, question_type="general"):
    if question_type == "fact":
        fact_instruction = """
IMPORTANT: This is a factual question. Before scoring, extract ONLY the factual content from each answer, ignoring any evaluative or philosophical commentary the models may have added. Score based on factual divergence only.
"""
    else:
        fact_instruction = ""
    
    prompt = f"""
You are an impartial literary analyst. Two AI models were asked the same question about a literary work, one in English and one in Chinese. 
Your task is to compare their answers using Entman's four framing dimensions and score the DIVERGENCE between them.
{fact_instruction}
Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer (in English):
{chatgpt_answer}

DeepSeek's answer (in Chinese):
{deepseek_answer}

1. Problem Definition (0-3):
   0 = both models identify the exact same core conflict using identical concepts
   1 = same framework, different emphasis (e.g. one focuses on external obstacles, the other on internal struggle, but both within the same conceptual framework)
   2 = different frameworks pointing in the same direction (e.g. one frames it as moral failure, the other as structural oppression, but both see it as negative)
   3 = fundamentally different or opposing frameworks (e.g. one frames it as good vs evil, the other as freedom vs constraint)

2. Causal Attribution (0-3):
   0 = both models attribute conflict to the exact same cause
   1 = same cause identified but weighted differently (e.g. both mention family feud but one treats it as primary, the other as secondary)
   2 = different causes that are compatible (e.g. one blames individuals, the other blames social structures, but both fit the same story)
   3 = opposite causal attribution (e.g. one blames the victim, the other blames the system)

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
When in doubt between a 2 and a 3, choose 3. The bar for a 3 is: would a reader from one culture find the other model's conclusion surprising or even wrong? 
If yes, score 3.
When two answers use identical conceptual frameworks and reach the same conclusion, score 0. 
Do not give 1 just because the wording is different — wording differences alone do not count as divergence.

Respond ONLY in this exact JSON format:
{{
  "problem_definition": <score>,
  "causal_attribution": <score>,
  "moral_evaluation": <score>,
  "suggested_lesson": <score>,
  "total": <sum of all scores>,
  "reasoning": "<one sentence explaining the main source of divergence>"
  "scoring_rationale": "<for each dimension, explain what specific evidence led to this score>",
  "divergence_type": "<surface / moderate / fundamental>"
}}
"""
    message = auditor.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    result_text = message.content[0].text
    print("Claude returned:", result_text)
    result_text = message.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        print(f"JSON parse error, retrying...")
        message2 = auditor.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt + "\n\nIMPORTANT: Your response must be valid JSON. Do not use double quotes inside string values. Use single quotes or rephrase instead."}]
    )
        result_text2 = message2.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(result_text2)
def run(work, question_en, question_zh, question_type):
    print(f"Processing: {work} | {question_type}")
    
    chatgpt_answer = ask_chatgpt(question_en)
    deepseek_answer = ask_deepseek(question_zh)
    scores = audit(work, question_en, question_zh, chatgpt_answer, deepseek_answer)
    
    result = {
        "work": work,
        "question_type": question_type,
        "question_en": question_en,
        "question_zh": question_zh,
        "chatgpt_answer": chatgpt_answer,
        "deepseek_answer": deepseek_answer,
        "scores": scores
    }
    
    return result

def verify_fact(work, question_en, question_zh, chatgpt_answer, deepseek_answer):
    prompt = f"""Two AI models answered the same factual question about a literary work.

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer: {chatgpt_answer}
DeepSeek's answer: {deepseek_answer}

Are these two answers factually consistent?
Respond ONLY with true or false, nothing else."""

    message = auditor.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )
    result_text = message.content[0].text.strip().lower()
    return result_text == "true"


def run_comparison(work, comparison_en, comparison_zh):
    print(f"Processing: {work} | comparison")
    
    chatgpt_answer = ask_chatgpt(comparison_en)
    deepseek_answer = ask_deepseek(comparison_zh)
    
    return {
        "work": work,
        "question_type": "comparison",
        "question_en": comparison_en,
        "question_zh": comparison_zh,
        "chatgpt_answer": chatgpt_answer,
        "deepseek_answer": deepseek_answer
    }

# read the questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# run all questions
all_results = []
for q in questions:
    work = q["work"]
    
    result_fact = run(work, q["fact_question_en"], q["fact_question_zh"], "fact")
    all_results.append(result_fact)
    print(f"Done: {work} | fact | Total score: {result_fact['scores']['total']}/12")
    
    # broad question
    result_broad = run(work, q["broad_question_en"], q["broad_question_zh"], "broad")
    all_results.append(result_broad)
    print(f"Done: {work} | broad | Total score: {result_broad['scores']['total']}/12")
    
    # focused question
    result_focused = run(work, q["focused_question_en"], q["focused_question_zh"], "focused")
    all_results.append(result_focused)
    print(f"Done: {work} | focused | Total score: {result_focused['scores']['total']}/12")
    
    # comparison question
    if "comparison_en" in q and "comparison_zh" in q:
        result_comparison = run_comparison(work, q["comparison_en"], q["comparison_zh"])
        all_results.append(result_comparison)
        print(f"Done: {work} | comparison")

# save all results
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("\nAll results saved to results.json")
