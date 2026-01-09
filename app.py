import pandas as pd
import gradio as gr
from sklearn.ensemble import RandomForestClassifier

# -------------------------
# Load Data & Train Model
# -------------------------
df = pd.read_csv("casino_risk_feature_data.csv")

features = [
    "session_length",
    "bets_placed",
    "avg_bet_amount",
    "total_loss",
    "deposit_frequency",
    "loss_chasing_score",
    "bet_escalation_risk",
    "session_intensity",
    "deposit_stress",
    "emotional_tilt"
]

df["high_risk_flag"] = (df["responsible_gambling_risk_score"] >= 4).astype(int)

X = df[features]
y = df["high_risk_flag"]

model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
model.fit(X, y)

# -------------------------
# Prediction Function
# -------------------------
def predict_risk(
    session_length, bets_placed, avg_bet_amount, total_loss,
    deposit_frequency, chasing_losses, rapid_bet_increase,
    long_session, frequent_deposits, emotional_tilt
):
    chasing_losses = 1 if chasing_losses == "Yes" else 0
    rapid_bet_increase = 1 if rapid_bet_increase == "Yes" else 0
    long_session = 1 if long_session == "Yes" else 0
    frequent_deposits = 1 if frequent_deposits == "Yes" else 0
    emotional_tilt = 1 if emotional_tilt == "Yes" else 0

    loss_chasing_score = chasing_losses
    bet_escalation_risk = rapid_bet_increase
    session_intensity = long_session
    deposit_stress = frequent_deposits

    risk_score = loss_chasing_score + bet_escalation_risk + session_intensity + deposit_stress + emotional_tilt

    input_df = pd.DataFrame([[
        session_length, bets_placed, avg_bet_amount, total_loss,
        deposit_frequency, loss_chasing_score, bet_escalation_risk,
        session_intensity, deposit_stress, emotional_tilt
    ]], columns=features)

    _ = model.predict(input_df)[0]

    if risk_score >= 6:
        risk_level = "🚨 SEVERE RISK"
        action = "Temporary account suspension + counseling recommended."
    elif risk_score >= 4:
        risk_level = "⚠️ HIGH RISK"
        action = "Cooling-off period + responsible gambling messages."
    else:
        risk_level = "✅ LOW RISK"
        action = "No action required."

    reasons = []
    if loss_chasing_score: reasons.append("chasing losses")
    if bet_escalation_risk: reasons.append("rapid bet escalation")
    if session_intensity: reasons.append("long sessions")
    if deposit_stress: reasons.append("frequent deposits")
    if emotional_tilt: reasons.append("emotional tilt behavior")

    explanation = ", ".join(reasons) if reasons else "No risky behavior detected."

    return risk_level, action, explanation

# -------------------------
# Gradio UI – Card-style with proper visibility handling
# -------------------------
with gr.Blocks(css="""
body {background-color: #1e1e2f; color: white; font-family: 'Segoe UI', sans-serif;}
h1 {color: gold; text-align: center; margin-bottom: 0.2em;}
h3 {color: #ffd700; text-align: center; margin-top: 0; margin-bottom: 1em;}
.gradio-container {max-width: 100% !important; margin:0 auto; padding: 20px;}
.gr-group {background-color: #2b2b3d; border-radius: 15px; padding: 25px; margin-bottom: 15px; border: 1px solid #444; transition: all 0.5s ease;}
.gr-button {background-color: gold; color: black; font-weight:bold; border-radius: 12px; font-size: 18px; transition: transform 0.2s;}
.gr-button:hover {transform: scale(1.05);}
input[type=number], .svelte-select {background-color: #1f1f2b; color:white; border: 1px solid #555; border-radius:10px; padding: 5px;}
.gr-slider {color: gold;}
""") as demo:

    gr.Markdown("<h1>🎰 Responsible Gambling Risk Detector</h1>")
    gr.Markdown("<h3>Analyze player behavior and detect gambling risk levels</h3>")

    # --- Input Card ---
    with gr.Group(visible=True, elem_id="input_card") as input_card:
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    session_length = gr.Slider(minimum=0, maximum=360, step=5, value=60, label="Session Length (minutes)")
                    bets_placed = gr.Slider(minimum=0, maximum=100, step=1, value=10, label="Bets Placed")
                    avg_bet_amount = gr.Slider(minimum=0, maximum=1000, step=10, value=50, label="Average Bet Amount ($)")
                    total_loss = gr.Slider(minimum=0, maximum=5000, step=50, value=0, label="Total Loss ($)")
                    deposit_frequency = gr.Slider(minimum=0, maximum=20, step=1, value=1, label="Deposit Frequency (per day)")
            with gr.Column(scale=1):
                with gr.Group():
                    chasing_losses = gr.Dropdown(label="Chasing Losses?", choices=["No","Yes"], value="No")
                    rapid_bet_increase = gr.Dropdown(label="Rapid Bet Increase?", choices=["No","Yes"], value="No")
                    long_session = gr.Dropdown(label="Long Session (>3 hours)?", choices=["No","Yes"], value="No")
                    frequent_deposits = gr.Dropdown(label="Frequent Deposits?", choices=["No","Yes"], value="No")
                    emotional_tilt = gr.Dropdown(label="Emotional Tilt?", choices=["No","Yes"], value="No")

        analyze_btn = gr.Button("🔍 Analyze Risk", variant="primary")

    # --- Result Card ---
    with gr.Group(visible=False, elem_id="result_card") as result_card:
        risk_output = gr.Textbox(label="Risk Level", interactive=False)
        action_output = gr.Textbox(label="Recommended Action", interactive=False)
        explanation_output = gr.Textbox(label="Explanation", interactive=False)
        back_btn = gr.Button("⬅️ Back to Inputs")

    # --- Functions to switch cards ---
    def show_result(*args):
        risk, action, explanation = predict_risk(*args)
        return gr.update(visible=False), gr.update(visible=True), risk, action, explanation

    def show_inputs():
        return gr.update(visible=True), gr.update(visible=False)

    # --- Connect Buttons ---
    analyze_btn.click(
        fn=show_result,
        inputs=[
            session_length, bets_placed, avg_bet_amount, total_loss,
            deposit_frequency, chasing_losses, rapid_bet_increase,
            long_session, frequent_deposits, emotional_tilt
        ],
        outputs=[input_card, result_card, risk_output, action_output, explanation_output]
    )

    back_btn.click(
        fn=show_inputs,
        inputs=[],
        outputs=[input_card, result_card]
    )

demo.launch()
