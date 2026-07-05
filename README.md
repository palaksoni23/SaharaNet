# 🫂 SaharaNet
### Multilingual AI Emergency Response for India's Street Children & Homeless Families

---

## 🎯 The Problem

India has over **1.8 million street children** and millions of homeless families. When a bystander sees someone in distress on the road, there is no simple, multilingual way to:
- Report the situation quickly
- Find the **nearest shelter, hospital, or food center**
- Get the **right emergency helpline** for the situation
- Ensure NGOs are **automatically alerted** when crises cluster in one area

Language is a massive barrier — most emergency apps work only in English, while the people who need help (and those reporting) often speak Hindi, Hinglish, or regional languages.

---

## 💡 Our Solution — SaharaNet

SaharaNet is a **6-agent AI pipeline** that lets anyone — in any language — report an emergency and instantly receive:

✅ Situation classification (medical / shelter / food / child safety)  
✅ Real-time nearest resources via **OpenStreetMap API**  
✅ Contextually correct emergency helpline numbers  
✅ Automatic NGO escalation at 3+ reports from same location  
✅ **Voice input** in Hindi/English via Web Speech API  

---

## 🤖 Agent Pipeline

```
🎤 Reporter Agent  →  🌐 Language Agent  →  🔍 Verify Agent
        →  🛡️ Safety Agent  →  🗺️ Resource Agent  →  🧠 Memory Agent
```

| Agent | Role |
|-------|------|
| 🎤 **Reporter** | Accepts voice or text in Hindi, English, Hinglish |
| 🌐 **Language** | Detects language, extracts location + situation |
| 🔍 **Verify** | Validates report, classifies urgency level |
| 🛡️ **Safety** | Flags medical emergencies & child safety concerns |
| 🗺️ **Resource** | Finds nearest hospital/shelter/food via live OSM API |
| 🧠 **Memory** | Logs reports, triggers NGO escalation at threshold |

---

## 🗺️ Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Hero, stats, agent pipeline overview |
| 🚨 **Report** | Submit emergency via text or voice |
| 📊 **Dashboard** | Live report tracker, urgency metrics, escalation alerts |
| 📖 **Guide** | Step-by-step "Kya Karein?" for each emergency type |
| ℹ️ **About** | Project info, tech stack, builder details |

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| **Streamlit** | Web app framework |
| **Groq LLaMA 3.1-8b** | AI report analysis & extraction |
| **Google ADK** | Multi-agent orchestration |
| **Web Speech API** | Voice input (Hindi/English) |
| **OpenStreetMap (Overpass API)** | Live nearby resource lookup |
| **Nominatim** | Free geocoding for any Indian city |
| **Python** | Backend logic |

---

## 🚀 How to Run

### Prerequisites
```bash
pip install streamlit groq python-dotenv requests
```

### Setup
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/SaharaNet.git
cd SaharaNet

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run
streamlit run app.py
```

### Get Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up → API Keys → Create Key
3. Paste in `.env` file

---

## 📞 Emergency Helplines Integrated

| Number | Service |
|--------|---------|
| **108** | Ambulance / Emergency |
| **1098** | Childline (children in distress) |
| **100** | Police |
| **181** | Women Helpline |
| **14567** | Elder Line (senior citizens) |
| **1077** | Disaster Management / Shelter |

---

## 🌍 Cities Supported

**50+ Indian cities** with verified government hospital data including:
Jaipur, Delhi, Mumbai, Pune, Bangalore, Chennai, Hyderabad, Kolkata, Ahmedabad, Lucknow, Patna, Nagpur, Indore, Bhopal, Chandigarh, Surat, Goa, Udaipur, Alwar, Kota, Jodhpur and more.

For any city not in the database, **live OpenStreetMap search** automatically finds nearby resources.

---

## 🏆 Kaggle — Agents for Good 2026

This project was built for the **Kaggle Agents for Good 2026** competition, which challenges developers to build AI agent systems that create real social impact.

SaharaNet addresses **UN SDG Goal 1 (No Poverty)**, **Goal 3 (Good Health)**, and **Goal 10 (Reduced Inequalities)** by connecting India's most vulnerable populations to emergency resources through accessible, multilingual AI.

---

## 👩‍💻 Builder

**Palak Soni**  
B.Tech CSE · MITRC Alwar, Rajasthan  
Full Stack Developer & AI Builder  

---

## 📁 Project Structure

```
SaharaNet/
├── app.py              # Main Streamlit app (5 pages)
├── .env                # API keys (not committed)
├── .gitignore          # Ignores .env, venv, pycache
├── requirements.txt    # Dependencies
└── README.md           # This file
```

---

## 📋 Requirements

```
streamlit
python-dotenv
requests
```
## 🚀 Live Demo

https://saharanet-nz2ny3zep8796j368ckmln.streamlit.app/

---

*Built with ❤️ for India's 1.8 million street children and homeless families.*
