import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

load_dotenv()

chatgpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
auditor = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.set_page_config(page_title="FrameLens", page_icon="📚", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "landing"

# ── Landing Page ──────────────────────────────────────────────────────────────
if st.session_state.page == "landing":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2347 40%, #1a3a6b 70%, #0d2347 100%);
        background-size: 400% 400%;
        animation: gradientFlow 8s ease infinite;
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
    }
    .landing-title {
        font-size: 5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(100, 160, 255, 0.5);
    }
    .landing-subtitle {
        font-size: 1.6rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.5rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-family: 'Georgia', serif;
    }
    .landing-desc {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.55);
        margin-bottom: 3rem;
        max-width: 500px;
        font-family: 'Georgia', serif;
        font-style: italic;
        line-height: 1.8;
    }
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #2a78d6, #1a5aaa) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        box-shadow: 0 0 30px rgba(42, 120, 214, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        box-shadow: 0 0 50px rgba(42, 120, 214, 0.7) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="landing-container">
        <div class="landing-title">📚 FrameLens</div>
        <div class="landing-subtitle">Cross-Cultural Literary Analysis</div>
        <div class="landing-desc">
            Discover how ChatGPT and DeepSeek interpret the same literary work through different cultural lenses.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Enter →", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()

# ── App Page ──────────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <style>
    .stApp { background: #f8f9fb; }
    .translation-box {
        background: #e8f0fe;
        border-left: 4px solid #2a78d6;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.95rem;
        color: #1a3a6b;
    }
    .syn-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        overflow: hidden;
        font-family: sans-serif;
    }
    .syn-table th {
        background: #0d2347;
        color: #a8c8ff;
        padding: 14px 20px;
        text-align: left;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
    }
    .syn-table td {
        padding: 16px 20px;
        vertical-align: top;
        font-size: 0.95rem;
        line-height: 1.7;
        border-bottom: 1px solid #e8edf5;
    }
    .syn-table tr:last-child td { border-bottom: none; }
    .syn-table td:first-child {
        background: #f0f4fb;
        font-weight: 700;
        color: #0d2347;
        width: 160px;
        white-space: nowrap;
    }
    .syn-table td:nth-child(2) { background: #ffffff; color: #1a1a1a; }
    .syn-table td:nth-child(3) { background: #f8f9fb; color: #1a1a1a; }
    .agree-badge {
        display: inline-block;
        background: #d4edda;
        color: #155724;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 8px;
    }
    .key-divergence {
        background: linear-gradient(135deg, #0d2347, #1a3a6b);
        color: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        font-size: 1rem;
        line-height: 1.7;
        margin-top: 0.5rem;
        font-family: sans-serif;
    }
    .key-divergence-label {
        color: #a8c8ff;
        font-weight: 700;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()
    with col_title:
        st.markdown("## 📚 FrameLens")

    st.markdown("Compare how **ChatGPT** (English) and **DeepSeek** (Chinese) interpret the same literary work.")
    st.divider()

    work = st.text_input("Literary Work", placeholder="e.g. Dream of the Red Chamber")
    question_en = st.text_area("Question (in English)", placeholder="e.g. What is the core conflict in this work?", height=100)
    st.caption("Your question will be automatically translated into Chinese for DeepSeek.")
    run = st.button("Analyze", type="primary", use_container_width=True)

    if run:
        if not work or not question_en:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Translating question to Chinese..."):
                question_zh = chatgpt.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Translate the following literary analysis question into natural, idiomatic Chinese. Return only the translation, nothing else.\n\n{question_en}"}]
                ).choices[0].message.content

            st.markdown(f'<div class="translation-box">🈶 Auto-translated: {question_zh}</div>', unsafe_allow_html=True)
            with st.spinner("Querying ChatGPT and DeepSeek..."):
                chatgpt_answer = chatgpt.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": question_en}]
                ).choices[0].message.content

                deepseek_answer = deepseek.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": question_zh}]
                ).choices[0].message.content

            with st.spinner("Auditing framing divergence..."):
                audit_prompt = f"""You are an impartial literary analyst. Two AI models were asked the same question about a literary work, one in English and one in Chinese. Your task is to compare their answers using Entman's four framing dimensions and score the DIVERGENCE between them.

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer (in English):
{chatgpt_answer}

DeepSeek's answer (in Chinese):
{deepseek_answer}

Score the divergence between the two answers on each dimension:

1. Problem Definition (0-3):
   0 = identical framing
   1 = same framework, different emphasis
   2 = different frameworks, same direction
   3 = fundamentally different or opposing frameworks

2. Causal Attribution (0-3):
   0 = identical cause identified
   1 = same cause, different weight
   2 = different causes, compatible
   3 = opposite causal attribution

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

Score 0 when two answers use identical conceptual frameworks and reach the same conclusion.
When in doubt between a 2 and a 3, choose 3.
IMPORTANT: Focus on DIVERGENCE in underlying frameworks, not surface similarity.

Respond ONLY in this exact JSON format:
{{
  "problem_definition": <score>,
  "causal_attribution": <score>,
  "moral_evaluation": <score>,
  "suggested_lesson": <score>,
  "total": <sum>,
  "reasoning": "<one sentence>",
  "divergence_type": "<surface / moderate / fundamental>"
}}"""

                message = auditor.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    temperature=0,
                    messages=[{"role": "user", "content": audit_prompt}]
                )
                result_text = message.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
                scores = json.loads(result_text)

            with st.spinner("Generating attributed synthesis..."):
                syn_prompt = f"""You are a literary synthesis assistant. Two AI models were asked the same question about a literary work, one in English (ChatGPT) and one in Chinese (DeepSeek).

Work: {work}
Question (EN): {question_en}
Question (ZH): {question_zh}

ChatGPT's answer: {chatgpt_answer}
DeepSeek's answer: {deepseek_answer}

Framing divergence scores:
- Problem Definition: {scores['problem_definition']}/3
- Causal Attribution: {scores['causal_attribution']}/3
- Moral Evaluation: {scores['moral_evaluation']}/3
- Suggested Lesson: {scores['suggested_lesson']}/3

For each of the four Entman dimensions, extract the key view from each model in 1-2 sentences. If both models agree on a dimension, set agree to true.

Respond ONLY in this exact JSON format, no other text:
{{
  "problem_definition": {{
    "chatgpt": "ChatGPT view here",
    "deepseek": "DeepSeek view here",
    "agree": false
  }},
  "causal_attribution": {{
    "chatgpt": "ChatGPT view here",
    "deepseek": "DeepSeek view here",
    "agree": false
  }},
  "moral_evaluation": {{
    "chatgpt": "ChatGPT view here",
    "deepseek": "DeepSeek view here",
    "agree": false
  }},
  "suggested_lesson": {{
    "chatgpt": "ChatGPT view here",
    "deepseek": "DeepSeek view here",
    "agree": false
  }},
  "key_divergence": "one sentence here"
}}"""

                syn_message = auditor.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    temperature=0,
                    messages=[{"role": "user", "content": syn_prompt}]
                )
                syn_text = syn_message.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
                synthesis = json.loads(syn_text)

            # scores
            st.divider()
            st.subheader("📊 Framing Divergence")
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Problem Definition", f"{scores['problem_definition']}/3")
            col2.metric("Causal Attribution", f"{scores['causal_attribution']}/3")
            col3.metric("Moral Evaluation", f"{scores['moral_evaluation']}/3")
            col4.metric("Suggested Lesson", f"{scores['suggested_lesson']}/3")
            col5.metric("Total Score", f"{scores['total']}/12")

            divergence_color = {
                "surface": "🟢 Surface",
                "moderate": "🟡 Moderate",
                "fundamental": "🔴 Fundamental"
            }
            st.caption(f"**Divergence Type:** {divergence_color.get(scores['divergence_type'], scores['divergence_type'])}　　**Reasoning:** {scores['reasoning']}")

            # synthesis table
            st.divider()
            st.subheader("🔀 Attributed Synthesis")

            dims = [
                ("Problem Definition", "problem_definition"),
                ("Causal Attribution", "causal_attribution"),
                ("Moral Evaluation", "moral_evaluation"),
                ("Suggested Lesson", "suggested_lesson"),
            ]

            rows_html = ""
            for label, key in dims:
                d = synthesis[key]
                agree_badge = '<span class="agree-badge">✓ Agree</span>' if d["agree"] else ""
                chatgpt_text = d["chatgpt"].replace('"', '&quot;').replace("'", "&#39;")
                deepseek_text = d["deepseek"].replace('"', '&quot;').replace("'", "&#39;")
                rows_html += (
                    "<tr>"
                    f"<td>{label}{agree_badge}</td>"
                    f"<td>{chatgpt_text}</td>"
                    f"<td>{deepseek_text}</td>"
                    "</tr>"
                )

            key_div_text = synthesis["key_divergence"].replace('"', '&quot;').replace("'", "&#39;")

            table_html = (
                '<table class="syn-table">'
                "<thead><tr>"
                "<th>Dimension</th>"
                "<th>🤖 ChatGPT</th>"
                "<th>🤖 DeepSeek</th>"
                "</tr></thead>"
                f"<tbody>{rows_html}</tbody>"
                "</table>"
                '<div class="key-divergence">'
                '<span class="key-divergence-label">Key Divergence:</span>'
                f"{key_div_text}"
                "</div>"
            )

            st.markdown(table_html, unsafe_allow_html=True)

            # original answers collapsed
            st.divider()
            with st.expander("📄 View Original Answers (Reference)"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### 🤖 ChatGPT (English)")
                    st.markdown(chatgpt_answer)
                with col_b:
                    st.markdown("### 🤖 DeepSeek (Chinese)")
                    st.markdown(deepseek_answer)