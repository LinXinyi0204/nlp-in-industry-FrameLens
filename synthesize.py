from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def synthesize(work, question_en, question_zh, chatgpt_answer, deepseek_answer, scores):

    prompt = f"""You are a literary synthesis assistant. Two AI models were asked the same question about a literary work, one in English (ChatGPT) and one in Chinese (DeepSeek). Your task is to produce an attributed synthesis that clearly labels which model contributed which insight.

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer (in English):
{chatgpt_answer}

DeepSeek's answer (in Chinese):
{deepseek_answer}

Framing divergence scores:
- Problem Definition: {scores['problem_definition']}/3
- Causal Attribution: {scores['causal_attribution']}/3
- Moral Evaluation: {scores['moral_evaluation']}/3
- Suggested Lesson: {scores['suggested_lesson']}/3
- Total: {scores['total']}/12
- Divergence type: {scores.get('divergence_type', 'moderate')}

RULES for synthesis:
1. NEVER blend the two perspectives into a neutral average. Keep each model's voice distinct.
2. ALWAYS label every insight with [ChatGPT] or [DeepSeek].
3. When the two models AGREE, say so explicitly: "Both models agree that..."
4. When the two models DISAGREE, present both views side by side without resolving the tension.
5. End with a one-sentence "Key Divergence" summary that captures the most important difference.
6. Write in English. Keep it under 300 words.

Format your response exactly like this:

**Synthesis: {work}**

**On Problem Definition:**
[your synthesis here, with [ChatGPT] and [DeepSeek] labels]

**On Causal Attribution:**
[your synthesis here]

**On Moral Evaluation:**
[your synthesis here]

**On Suggested Lesson:**
[your synthesis here]

**Key Divergence:** [one sentence]
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

# read results
with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

all_syntheses = []

for item in results:
    if item["question_type"] in ["broad", "focused"]:
        print(f"Synthesizing: {item['work']} | {item['question_type']}")

        synthesis = synthesize(
            work=item["work"],
            question_en=item["question_en"],
            question_zh=item["question_zh"],
            chatgpt_answer=item["chatgpt_answer"],
            deepseek_answer=item["deepseek_answer"],
            scores=item["scores"]
        )

        all_syntheses.append({
            "work": item["work"],
            "question_type": item["question_type"],
            "question_en": item["question_en"],
            "synthesis": synthesis,
            "scores": item["scores"]
        })

        print(f"Done: {item['work']} | {item['question_type']}")

# save
with open("syntheses.json", "w", encoding="utf-8") as f:
    json.dump(all_syntheses, f, ensure_ascii=False, indent=2)

print("\nAll syntheses saved to syntheses.json")