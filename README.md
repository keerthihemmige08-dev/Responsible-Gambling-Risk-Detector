# 🎰 Responsible Gambling Risk Detector

**AI-powered tool to detect gambling risk levels in casino players.**  
Built using **Python**, **Scikit-learn**, and **Gradio**. Features an **interactive dashboard** with animated outputs and risk visualization.

---

## 🚀 Project Overview

Responsible gambling is critical for casinos and players alike. This project uses **player behavior data** to predict whether a player is at **Low, High, or Severe risk** of problematic gambling. It also explains **why** the player is flagged with an easy-to-read interactive interface.

**Key Features:**
- Predicts **risk level**: Low ✅, High ⚠️, Severe 🚨
- Highlights **risky behaviors** like chasing losses, rapid bet escalation, long sessions, frequent deposits, and emotional tilt.
- **Animated dashboard** using Gradio for a professional, user-friendly experience.
- Fully interactive: sliders for numeric inputs, dropdowns for behavioral indicators.

---

## 🛠 Technology Stack

- **Python 3.11+**
- **Pandas** – for data handling
- **Scikit-learn** – Random Forest Classifier for AI predictions
- **Gradio** – interactive web interface
- **CSS** – custom styling and animations

---

## 📊 How It Works

1. **Data Input:** User enters session length, bets placed, average bet amount, total loss, deposit frequency, and selects behavioral indicators.  
2. **AI Model:** A trained Random Forest Classifier predicts whether the player is at high risk.  
3. **Output:** The dashboard shows:
   - **Risk Level** (Low / High / Severe) with color-coded animation
   - **Recommended Action**
   - **Explanation** for the risk detected

---

## 💻 Live Demo

Try it online here: [Hugging Face Space](https://huggingface.co/spaces/YKeerthiHemmige08/responsible_gambling)  
 