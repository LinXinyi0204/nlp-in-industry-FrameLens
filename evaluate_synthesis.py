from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

evaluator = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_attribution(synthesis_text):
    prompt = f"""Read the following synthesis text carefully.

Synthesis:
{synthesis_text}

Count every distinct claim or insight in the text.
For each one, check if it has an explicit attribution label ([ChatGPT] or [DeepSeek]) or says "Both models agree".

Respond ONLY in this exact JSON format:
{{
  "total_claims": <total number of claims>,
  "attributed_claims": <number with explicit [ChatGPT] or [DeepSeek] label>,
  "both_models_claims": <number with "Both models agree">,
  "attribution_rate": <attributed_claims divided by total_claims, as a decimal>
}}"""

    response = evaluator.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(result)


def check_coverage(chatgpt_answer, deepseek_answer, synthesis_text):
    prompt = f"""You are evaluating a synthesis of two AI model answers.

ChatGPT's original answer:
{chatgpt_answer}

DeepSeek's original answer:
{deepseek_answer}

Synthesis text:
{synthesis_text}

Step 1: Extract the 3-5 most important claims from ChatGPT's answer.
Step 2: Extract the 3-5 most important claims from DeepSeek's answer.
Step 3: For each claim, check whether it is covered in the synthesis text.

Respond ONLY in this exact JSON format:
{{
  "chatgpt_claims": [
    {{"claim": "<claim text>", "covered": true or false}}
  ],
  "deepseek_claims": [
    {{"claim": "<claim text>", "covered": true or false}}
  ],
  "chatgpt_coverage_rate": <covered chatgpt claims divided by total chatgpt claims>,
  "deepseek_coverage_rate": <covered deepseek claims divided by total deepseek claims>,
  "overall_coverage_rate": <all covered claims divided by all claims>
}}"""

    response = evaluator.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(result)


# read syntheses and results
with open("syntheses.json", "r", encoding="utf-8") as f:
    syntheses = json.load(f)

with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# build lookup for original answers
lookup = {}
for item in results:
    if item["question_type"] in ["broad", "focused"]:
        key = f"{item['work']}_{item['question_type']}"
        lookup[key] = {
            "chatgpt_answer": item["chatgpt_answer"],
            "deepseek_answer": item["deepseek_answer"]
        }

# evaluate each synthesis
all_evaluations = []

for s in syntheses:
    key = f"{s['work']}_{s['question_type']}"
    if key not in lookup:
        continue

    print(f"Evaluating: {s['work']} | {s['question_type']}")

    original = lookup[key]

    attribution = check_attribution(s["synthesis"])
    coverage = check_coverage(
        original["chatgpt_answer"],
        original["deepseek_answer"],
        s["synthesis"]
    )

    all_evaluations.append({
        "work": s["work"],
        "question_type": s["question_type"],
        "attribution": attribution,
        "coverage": coverage
    })

    print(f"Done: {s['work']} | attribution: {attribution['attribution_rate']:.0%} | coverage: {coverage['overall_coverage_rate']:.0%}")

# save
with open("evaluations.json", "w", encoding="utf-8") as f:
    json.dump(all_evaluations, f, ensure_ascii=False, indent=2)

print("\nAll evaluations saved to evaluations.json")