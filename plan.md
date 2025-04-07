# 📊 AI-Powered Data Insight Platform

**Project Lead:** Vaibhav Mahindru  
**Start Date:** April 05, 2025  
**Goal:** Build a Streamlit-based AI web app where users can upload Excel files and receive detailed AI-generated summaries, insights, and dynamic, interactive graphs — with user authentication.

---

## 🧭 Master Roadmap

| Phase | Title | Description | Tools |
|-------|-------|-------------|-------|
| 1 | **Basic Project Setup + MVP UI** | Upload Excel/CSV, preview file, basic data summary | `streamlit`, `pandas` |
| 2 | **AI Summary with DeepSeek** | Call DeepSeek API to generate detailed natural-language summary | `requests`, DeepSeek API |
| 3 | **AI-Generated Graph Code** | Ask AI to generate Python code to visualize data | `json`, prompt design |
| 4 | **Run AI Graph Code** | Execute AI-generated code to render visuals dynamically | `exec()`, `matplotlib`, `plotly` |
| 5 | **Interactive Dashboard** | Add filters, dropdowns, and interactive graphs | `plotly`, `streamlit widgets` |
| 6 | **Advanced AI Insights** | AI points out anomalies, trends, suggestions | Gemini prompts, NLP |
| 6.5 | **Modularity** | Making code more odular and clean. Deploying the MVP | Streamlit |
| 7 | **User Authentication System** | Register/Login, private workspaces | `streamlit-authenticator`, `session_state` |
| 8 | **Chat with Your Data** | Users can ask questions about their uploaded data | DeepSeek LLM, `pandas` |
| 9 | **User History + Logging** | Track uploads & results by user | `uuid`, `yaml`, `logging` |
| 10 | **Deployment** | Deploy to Streamlit Cloud or Render | `requirements.txt`, `GitHub` |
| 11 | **Bonus Features** | Export to PDF, download dashboard, voice replies | `pdfkit`, TTS APIs |

---

## ✅ To-Do List

### Phase 1: Project Setup
- [✅] Set up Python virtual environment
- [✅] Install Streamlit and Pandas
- [✅] Create `main.py` and basic Streamlit layout
- [✅] Add file upload and data preview

### Phase 2: AI Summary via DeepSeek
- [✅] Set up DeepSeek API key
- [✅] Create prompt to analyze uploaded data
- [✅] Display AI-generated summary in UI
- [✅] Downloadable summary
- [✅] Reset Button

### Phase 3: Graph Code Generation
- [ ] Prompt DeepSeek to generate graph code
- [ ] Validate Python code from AI

### Phase 4: Execute & Render Graphs
- [ ] Run AI-generated code using `exec()`
- [ ] Display static or interactive graphs

### Phase 5: Interactive Dashboard
- [ ] Add dropdowns/filters
- [ ] Use `plotly` for interactivity

### Phase 6: AI Advanced Insights
- [ ] Prompt AI for insights, anomalies
- [ ] Structure and highlight key findings

### Phase 6.5: Modularity
- [ ] Make code modular
- [ ] MVP Deployment

### Phase 7: User Authentication
- [ ] Add `streamlit-authenticator`
- [ ] Create login/register UI
- [ ] Associate user data with uploads

### Phase 8: Chat with Data
- [ ] Input question → AI interprets and answers from data
- [ ] Display relevant response & code

### Phase 9: History & Logging
- [ ] Store files per user
- [ ] Log uploads, errors, timestamps

### Phase 10: Deployment
- [ ] Push to GitHub
- [ ] Deploy on Streamlit Cloud or Render

### Phase 11: Bonus Features
- [ ] Export AI summary to PDF
- [ ] Download dashboard as report
- [ ] Add TTS for audio reply

---

## 🛠 Tech Stack

- Python, Pandas, Streamlit
- Gemini API (AI model)
- Plotly, Matplotlib (Graphs)
- streamlit-authenticator (Login)
- GitHub + Streamlit Cloud (Deployment)
- Optional: Firebase/Supabase for storage

---

_Logged and maintained by Vaibhav Mahindru_