# 📚 FrameLens

Course project repository for the NLP in Industry (SS26) project "FrameLens" at Heidelberg University.

**Cross-Cultural Literary Analysis Tool** ｜ Xinyi Lin · Jiaran Li · Yiming Li


---


## 🔍 What This Is

FrameLens is an interactive tool for exploring how large language models frame literary interpretation differently across languages and cultures. Enter any literary work and a question, and the system asks ChatGPT in English and DeepSeek in Chinese in parallel (your English question is automatically translated into Chinese for DeepSeek). Their answers are scored on four dimensions from Entman's framing theory (problem definition, causal attribution, moral evaluation, suggested lesson), and combined into an attributed synthesis that clearly shows what each model contributed and where they agree or disagree.


---


## 🚀 Quick Start

**Requirements**: Python 3.10 or above. No conda or venv required.

**Install dependencies**:
```
pip install openai anthropic python-dotenv streamlit
```

**Configure API keys**: Create a `.env` file in the project root and add:
```
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```
Keys can be obtained from platform.openai.com, platform.deepseek.com, and console.anthropic.com respectively. `.env` is listed in `.gitignore` and will not be uploaded to the repository.

**Launch the web interface**:
```
streamlit run app.py
```
Opens the interface in your browser at `localhost:8501`. Enter any literary work and question for a live analysis.

**Reproduce the experiment data** (optional, run in order):
```
python main.py                  # Query both models + audit scoring → results.json
python synthesize.py            # Generate attributed synthesis → syntheses.json
python evaluate_synthesis.py    # Evaluate synthesis quality → evaluations.json
```
💡 `main.py` is the main pipeline and the only script you need to run to collect data; it combines the querying and auditing steps.


---


## 🗂️ File Structure

| File | Purpose |
|---|---|
| `app.py` | 🖥️ Streamlit web interface (primary way to use FrameLens) |
| `main.py` | ⚙️ Full pipeline: query both models + audit scoring |
| `synthesize.py` | 🧬 Generates the attributed synthesis |
| `evaluate_synthesis.py` | ✅ Evaluates attribution clarity and information coverage |
| `questions.json` | 📋 Question set for six literary works (fact / broad / focused / comparison) |
| `results.json` | 📊 Model answers and divergence scores |
| `syntheses.json` | 📝 Attributed synthesis texts |
| `evaluations.json` | 📈 Synthesis quality evaluation results |
| `pipeline.py` / `audit.py` | 🕰️ Early test scripts; functionality now integrated into `main.py` |


---


## 🧪 Experiment: Six Classic Works Across Languages

Beyond serving as a general-purpose tool, this project systematically tested six literary works (Romeo and Juliet, Journey to the West, Dream of the Red Chamber, Wuthering Heights, Don Quixote, and The Tale of the Bamboo Cutter, the last two serving as third-party comparison texts), with four question types per work, for **24 paired comparisons** in total, to check whether FrameLens can detect stable, explainable cross-lingual framing differences.

**Key findings**:
- 📉 Fact questions show much lower divergence than interpretive questions (fact: 0-2, broad: 5-7, focused: 5-9, out of a maximum of 12)
- ⚖️ Divergence concentrates most in Moral Evaluation and Suggested Lesson, rather than in how the core problem itself is defined

**Synthesis quality**: across 12 synthesis outputs, attribution clarity averages 79% and information coverage averages 96%, cross-checked by manual review (six complete texts inspected, with results matching the automated evaluation).

The project also includes a self-validation check comparing each model's self-reported understanding of its own interpretive tendencies against its actual behavior, which supports the choice to rely on direct paired responses rather than self-report as the primary evidence for framing divergence.

📄 Full methodology, experimental design, and limitations are in the report.


---


## ⚠️ Limitations

The sample size is limited, and the findings have not yet been validated at a larger scale. The experimental design does not fully separate "model effects" from "language effects" (ChatGPT is tested in English, DeepSeek in Chinese), so the observed differences cannot be directly equated with cultural differences themselves. Part of the evaluation relies on judgments made by language models, which carries some risk of evaluator bias. See Section 5.4 of the report for the full discussion.


---


## 🎬 Demo Video

[[YouTube link]
](https://youtu.be/nnz9SM4K9Vw?is=Ofko0c_22vTnyLcJ)

---


## 🤖 AI Tool Usage Disclosure

All algorithmic and design decisions were made independently, including pipeline architecture, model selection, prompt engineering, and evaluation design. AI tools (Claude) were used to assist with code writing, debugging, and optimization.


---


## 📖 Citation

Entman, R. M. (1993). Framing: Toward Clarification of a Fractured Paradigm. *Journal of Communication*, 43(4), 51-58.
